from collections import defaultdict

from django.db.models import Case, Count, F, FloatField, Q, Value, When
from django.db.models.functions import Cast
from ninja import Router
from ninja_jwt.authentication import JWTAuth

from usuarios.models import Usuario
from usuarios.roles import requiere_rol_minimo
from vehiculos.models import Vehiculo

from .schemas import (
    AnioItem,
    ChartsResponse,
    EstadoDashboardItem,
    EstadoResumen,
    EstatusKPI,
    KPIsResponse,
    MarcaItem,
    NacionalResponse,
)

router = Router()

OPTIONAL_FIELDS = [
    ("numero_unidad", Q(numero_unidad__isnull=False)),
    ("placa", Q(placa__isnull=False)),
    ("color_placa", Q(color_placa__isnull=False)),
    ("placa_intt", ~Q(placa_intt__exact="")),
    ("serial_motor", ~Q(serial_motor__exact="")),
    ("tipo_uso", Q(tipo_uso__isnull=False)),
    ("color", Q(color__isnull=False)),
    ("unidad_usuaria", Q(unidad_usuaria__isnull=False)),
]


def _scoped_qs(request):
    qs = Vehiculo.objects.all()
    user = request.auth
    if user.estado_id:
        qs = qs.filter(estado_id=user.estado_id)
    return qs


def _completitud_promedio(qs):
    # Each vehicle starts with 12 base points (for always-required fields).
    # Up to 8 optional fields can add 1 point each → max 20 points per vehicle.
    # Formula: (12*total + filled_sum) / (20*total) * 100 → percentage.
    stats = qs.aggregate(
        total=Count("id"),
        **{f"cnt_{f}": Count("pk", filter=filtro) for f, filtro in OPTIONAL_FIELDS},
    )
    total = stats["total"]
    if not total:
        return 0.0
    filled_sum = sum(stats[f"cnt_{f}"] for f, _ in OPTIONAL_FIELDS)
    return round(((12 * total) + filled_sum) / (20 * total) * 100, 1)


@router.get("/kpis", response=KPIsResponse, auth=JWTAuth())
@requiere_rol_minimo(Usuario.Rol.MECANICO)
def kpis(request):
    qs = _scoped_qs(request)

    total = qs.count()
    operativos = qs.filter(estatus__es_operativo=True, estatus_activo=True).count()
    pct = round(operativos / total * 100, 1) if total else 0.0

    estatus_qs = (
        qs.values("estatus_id", "estatus__nombre")
        .annotate(cantidad=Count("id"))
        .order_by("-cantidad")
    )

    inactivos = total - operativos

    return KPIsResponse(
        total_vehiculos=total,
        porcentaje_operatividad=pct,
        operativos=operativos,
        inactivos=inactivos,
        completitud_promedio=_completitud_promedio(qs),
        estatus=[
            EstatusKPI(id=e["estatus_id"], nombre=e["estatus__nombre"], cantidad=e["cantidad"])
            for e in estatus_qs
        ],
    )


@router.get("/charts", response=ChartsResponse, auth=JWTAuth())
@requiere_rol_minimo(Usuario.Rol.MECANICO)
def charts(request):
    qs = _scoped_qs(request)

    por_estado = (
        qs.values("estado_id", "estado__nombre")
        .annotate(
            total=Count("id"),
            activos=Count("id", filter=Q(estatus__es_operativo=True, estatus_activo=True)),
        )
        .annotate(
            inactivos=F("total") - F("activos"),
            operatividad=Case(
                When(total=0, then=Value(0.0)),
                default=Cast(F("activos"), FloatField()) / Cast(F("total"), FloatField()) * 100.0,
                output_field=FloatField(),
            ),
        )
        .order_by("-total")
    )

    por_marca = (
        qs.values("marca_id", "marca__nombre")
        .annotate(cantidad=Count("id"))
        .order_by("-cantidad")[:10]
    )

    por_anio = qs.values("anio").annotate(cantidad=Count("id")).order_by("anio")

    return ChartsResponse(
        por_estado=[
            EstadoDashboardItem(
                estado_nombre=e["estado__nombre"],
                total=e["total"],
                operatividad=round(e["operatividad"], 1),
                activos=e["activos"],
                inactivos=e["inactivos"],
            )
            for e in por_estado
        ],
        por_marca=[
            MarcaItem(id=e["marca_id"], nombre=e["marca__nombre"], cantidad=e["cantidad"])
            for e in por_marca
        ],
        por_anio=[AnioItem(anio=e["anio"], cantidad=e["cantidad"]) for e in por_anio],
    )


@router.get("/nacional", response=NacionalResponse, auth=JWTAuth())
@requiere_rol_minimo(Usuario.Rol.NACIONAL)
def nacional(request):
    # 1) Per-state totals and operatividad
    estado_stats = (
        Vehiculo.objects.values("estado_id", "estado__nombre")
        .annotate(
            total=Count("id"),
            activos=Count("id", filter=Q(estatus__es_operativo=True, estatus_activo=True)),
        )
        .annotate(
            inactivos=F("total") - F("activos"),
            operatividad=Case(
                When(total=0, then=Value(0.0)),
                default=Cast(F("activos"), FloatField()) / Cast(F("total"), FloatField()) * 100.0,
                output_field=FloatField(),
            ),
        )
        .order_by("-total")
    )

    stats_map = {}
    for row in estado_stats:
        stats_map[row["estado_id"]] = row

    # 2) Per-state + per-status breakdown
    estado_estatus = (
        Vehiculo.objects.values("estado_id", "estado__nombre", "estatus_id", "estatus__nombre")
        .annotate(cantidad=Count("id"))
        .order_by("estado__nombre", "-cantidad")
    )

    estatus_map = defaultdict(list)
    for row in estado_estatus:
        estatus_map[row["estado_id"]].append(
            EstatusKPI(
                id=row["estatus_id"],
                nombre=row["estatus__nombre"],
                cantidad=row["cantidad"],
            )
        )

    resumen = []
    for estado_id, s in stats_map.items():
        resumen.append(
            EstadoResumen(
                estado_nombre=s["estado__nombre"],
                total=s["total"],
                operatividad=round(s["operatividad"], 1),
                activos=s["activos"],
                inactivos=s["inactivos"],
                estatus=estatus_map.get(estado_id, []),
            )
        )

    total_v = sum(r.total for r in resumen)
    total_est = len(resumen)

    mejor = max(resumen, key=lambda r: r.operatividad) if resumen else None
    peor = min(resumen, key=lambda r: r.operatividad) if resumen else None

    return NacionalResponse(
        resumen_estados=resumen,
        total_vehiculos=total_v,
        total_estados_con_vehiculos=total_est,
        mejor_operatividad=mejor,
        peor_operatividad=peor,
    )
