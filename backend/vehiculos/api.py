import base64
from io import BytesIO

import qrcode
from ninja import Router
from ninja.errors import HttpError
from ninja_jwt.authentication import JWTAuth

from usuarios.models import Usuario
from usuarios.roles import requiere_rol_minimo

from .models import Vehiculo
from .schemas import VehiculoCreate, VehiculoSchema, VehiculoUpdate

router = Router()


def _filter_activos(queryset, request):
    incluir_inactivos = request.GET.get("incluir_inactivos") == "true"
    if not incluir_inactivos:
        return queryset.filter(estatus_activo=True)
    return queryset


def _get_object_or_404(model, id):
    try:
        return model.objects.get(id=id)
    except model.DoesNotExist:
        raise HttpError(404, f"{model._meta.verbose_name} no encontrado")


def _build_vehiculo_schema(v):
    return VehiculoSchema(
        id=v.id,
        numero_economico=v.numero_economico,
        numero_unidad=v.numero_unidad,
        anio=v.anio,
        vin=v.vin,
        placa=v.placa,
        placa_intt=v.placa_intt,
        serial_motor=v.serial_motor,
        codigo_qr=v.codigo_qr,
        estatus_activo=v.estatus_activo,
        gerencia=v.gerencia_id,
        gerencia_nombre=v.gerencia.nombre,
        categoria=v.categoria_id,
        categoria_nombre=v.categoria.nombre,
        marca=v.marca_id,
        marca_nombre=v.marca.nombre,
        modelo=v.modelo_id,
        modelo_nombre=v.modelo.nombre,
        estado=v.estado_id,
        estado_nombre=v.estado.nombre,
        emplazamiento=v.emplazamiento_id,
        emplazamiento_nombre=v.emplazamiento.nombre,
        estatus=v.estatus_id,
        estatus_nombre=v.estatus.nombre,
        color=v.color_id,
        color_nombre=v.color.nombre,
        color_placa=v.color_placa_id,
        color_placa_nombre=v.color_placa.nombre,
    )


def _generate_qr(vehicle_id):
    content = f"/vehiculos/{vehicle_id}"
    img = qrcode.make(content)
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    qr_b64 = base64.b64encode(buffer.getvalue()).decode()
    return f"data:image/png;base64,{qr_b64}"


# ─── CRUD ────────────────────────────────────────────────────────────────


@router.get("/", response=list[VehiculoSchema], auth=JWTAuth())
@requiere_rol_minimo(Usuario.Rol.MECANICO)
def list_vehiculos(request):
    qs = Vehiculo.objects.select_related(
        "gerencia", "categoria", "marca", "modelo",
        "estado", "emplazamiento", "estatus", "color", "color_placa",
    )
    qs = _filter_activos(qs, request)
    return [_build_vehiculo_schema(v) for v in qs]


@router.get("/{vehiculo_id}", response=VehiculoSchema, auth=JWTAuth())
@requiere_rol_minimo(Usuario.Rol.MECANICO)
def get_vehiculo(request, vehiculo_id: int):
    try:
        v = Vehiculo.objects.select_related(
            "gerencia", "categoria", "marca", "modelo",
            "estado", "emplazamiento", "estatus", "color", "color_placa",
        ).get(id=vehiculo_id)
    except Vehiculo.DoesNotExist:
        raise HttpError(404, "Vehículo no encontrado")
    return _build_vehiculo_schema(v)


@router.post("/", response=VehiculoSchema, auth=JWTAuth())
@requiere_rol_minimo(Usuario.Rol.NACIONAL)
def create_vehiculo(request, data: VehiculoCreate):
    if Vehiculo.objects.filter(numero_economico=data.numero_economico).exists():
        raise HttpError(409, "Ya existe un vehículo con ese número económico")
    if data.numero_unidad and Vehiculo.objects.filter(numero_unidad=data.numero_unidad).exists():
        raise HttpError(409, "Ya existe un vehículo con ese número de unidad")
    if Vehiculo.objects.filter(vin=data.vin).exists():
        raise HttpError(409, "Ya existe un vehículo con ese VIN")
    if Vehiculo.objects.filter(placa=data.placa, color_placa_id=data.color_placa_id).exists():
        raise HttpError(409, "Ya existe un vehículo con esa placa para el mismo color de placa")

    v = Vehiculo.objects.create(**data.dict())
    v.codigo_qr = _generate_qr(v.id)
    v.save(update_fields=["codigo_qr"])

    v.refresh_from_db()
    v = Vehiculo.objects.select_related(
        "gerencia", "categoria", "marca", "modelo",
        "estado", "emplazamiento", "estatus", "color", "color_placa",
    ).get(id=v.id)
    return _build_vehiculo_schema(v)


@router.put("/{vehiculo_id}", response=VehiculoSchema, auth=JWTAuth())
@requiere_rol_minimo(Usuario.Rol.NACIONAL)
def update_vehiculo(request, vehiculo_id: int, data: VehiculoUpdate):
    v = _get_object_or_404(Vehiculo, vehiculo_id)
    payload = data.dict(exclude_unset=True)

    if "numero_economico" in payload and payload["numero_economico"] != v.numero_economico:
        if Vehiculo.objects.filter(numero_economico=payload["numero_economico"]).exists():
            raise HttpError(409, "Ya existe un vehículo con ese número económico")
    if "numero_unidad" in payload and payload["numero_unidad"] != v.numero_unidad:
        if Vehiculo.objects.filter(numero_unidad=payload["numero_unidad"]).exists():
            raise HttpError(409, "Ya existe un vehículo con ese número de unidad")
    if "vin" in payload and payload["vin"] != v.vin:
        if Vehiculo.objects.filter(vin=payload["vin"]).exists():
            raise HttpError(409, "Ya existe un vehículo con ese VIN")

    for attr, value in payload.items():
        setattr(v, attr, value)
    v.save()

    v.refresh_from_db()
    v = Vehiculo.objects.select_related(
        "gerencia", "categoria", "marca", "modelo",
        "estado", "emplazamiento", "estatus", "color", "color_placa",
    ).get(id=vehiculo_id)
    return _build_vehiculo_schema(v)


@router.delete("/{vehiculo_id}", response={204: None}, auth=JWTAuth())
@requiere_rol_minimo(Usuario.Rol.NACIONAL)
def deactivate_vehiculo(request, vehiculo_id: int):
    v = _get_object_or_404(Vehiculo, vehiculo_id)
    v.estatus_activo = False
    v.save()
    return 204, None
