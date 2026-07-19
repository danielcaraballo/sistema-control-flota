import base64
from io import BytesIO

import qrcode
from django.db.models import Q
from ninja import Field, Router
from ninja.errors import HttpError
from ninja_jwt.authentication import JWTAuth

from usuarios.models import Usuario
from usuarios.roles import requiere_rol_minimo
from utils.api_helpers import (
    check_duplicate,
    check_duplicate_composite,
    filter_activos,
    get_object_or_404,
)

from .models import Vehiculo
from .schemas import (
    VehiculoCreate,
    VehiculoListItemSchema,
    VehiculoListResponse,
    VehiculoSchema,
    VehiculoUpdate,
)

router = Router()

SELECT_RELATED = [
    "gerencia",
    "unidad_usuaria",
    "categoria",
    "marca",
    "modelo",
    "estado",
    "emplazamiento",
    "estatus",
    "color",
    "color_placa",
    "tipo_uso",
    "clase",
    "tipo_combustible",
]

SORT_FIELD_MAP = {
    "id": "id",
    "numero_economico": "numero_economico",
    "placa": "placa",
    "anio": "anio",
    "vin": "vin",
    "estatus_activo": "estatus_activo",
    "marca_nombre": "marca__nombre",
    "estatus_nombre": "estatus__nombre",
    "estado_nombre": "estado__nombre",
    "gerencia_nombre": "gerencia__nombre",
    "clase_nombre": "clase__nombre",
    "tipo_combustible_nombre": "tipo_combustible__nombre",
}


def _build_vehiculo_schema(v, include_qr=True):
    def _name_or_none(related):
        return related.nombre if related else None

    kw = dict(
        id=v.id,
        numero_economico=v.numero_economico,
        numero_unidad=v.numero_unidad,
        anio=v.anio,
        vin=v.vin,
        placa=v.placa,
        placa_intt=v.placa_intt,
        serial_motor=v.serial_motor,
        estatus_activo=v.estatus_activo,
        gerencia=v.gerencia_id,
        gerencia_nombre=v.gerencia.nombre,
        unidad_usuaria=v.unidad_usuaria_id,
        unidad_usuaria_nombre=_name_or_none(v.unidad_usuaria),
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
        color_nombre=_name_or_none(v.color),
        color_placa=v.color_placa_id,
        color_placa_nombre=_name_or_none(v.color_placa),
        tipo_uso=v.tipo_uso_id,
        tipo_uso_nombre=_name_or_none(v.tipo_uso),
        clase=v.clase_id,
        clase_nombre=v.clase.nombre,
        tipo_combustible=v.tipo_combustible_id,
        tipo_combustible_nombre=v.tipo_combustible.nombre,
    )
    if include_qr:
        kw["codigo_qr"] = v.codigo_qr
    return kw


def _make_qr_data_uri(url: str) -> str:
    img = qrcode.make(url)
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    qr_b64 = base64.b64encode(buffer.getvalue()).decode()
    return f"data:image/png;base64,{qr_b64}"


def _generate_qr(request, vehicle_id):
    url = request.build_absolute_uri(f"/vehiculos/{vehicle_id}")
    return _make_qr_data_uri(url)


# ─── CRUD ────────────────────────────────────────────────────────────────


@router.get("/", response=VehiculoListResponse, auth=JWTAuth())
@requiere_rol_minimo(Usuario.Rol.MECANICO)
def list_vehiculos(
    request,
    limit: int = Field(default=50, ge=1, le=100),
    offset: int = Field(default=0, ge=0),
    search: str | None = None,
    sort_by: str = "id",
    sort_order: str = "asc",
    estado_id: int | None = None,
    estatus_id: int | None = None,
    gerencia_id: int | None = None,
):
    qs = Vehiculo.objects.select_related(*SELECT_RELATED)
    user = request.auth
    if user.estado_id:
        qs = qs.filter(estado_id=user.estado_id)
    qs = filter_activos(qs, request)
    if search:
        qs = qs.filter(
            Q(numero_economico__icontains=search)
            | Q(vin__icontains=search)
            | Q(placa__icontains=search)
            | Q(placa_intt__icontains=search)
            | Q(serial_motor__icontains=search)
            | Q(numero_unidad__icontains=search)
        )
    if estado_id:
        qs = qs.filter(estado_id=estado_id)
    if estatus_id:
        qs = qs.filter(estatus_id=estatus_id)
    if gerencia_id:
        qs = qs.filter(gerencia_id=gerencia_id)

    sort_field = SORT_FIELD_MAP.get(sort_by)
    if sort_field:
        if sort_order == "desc":
            sort_field = f"-{sort_field}"
        qs = qs.order_by(sort_field)

    count = qs.count()
    items = [
        VehiculoListItemSchema(**d)
        for d in (_build_vehiculo_schema(v, include_qr=False) for v in qs[offset : offset + limit])
    ]

    return VehiculoListResponse(items=items, count=count)


@router.get("/{vehiculo_id}", response=VehiculoSchema, auth=JWTAuth())
@requiere_rol_minimo(Usuario.Rol.MECANICO)
def get_vehiculo(request, vehiculo_id: int):
    v = get_object_or_404(Vehiculo.objects.select_related(*SELECT_RELATED), vehiculo_id)
    return _build_vehiculo_schema(v)


@router.post("/", response=VehiculoSchema, auth=JWTAuth())
@requiere_rol_minimo(Usuario.Rol.NACIONAL)
def create_vehiculo(request, data: VehiculoCreate):
    if check_duplicate(Vehiculo, "numero_economico", data.numero_economico):
        raise HttpError(409, "Ya existe un vehículo activo con ese número económico")
    if data.numero_unidad and check_duplicate(Vehiculo, "numero_unidad", data.numero_unidad):
        raise HttpError(409, "Ya existe un vehículo activo con ese número de unidad")
    if check_duplicate(Vehiculo, "vin", data.vin):
        raise HttpError(409, "Ya existe un vehículo activo con ese VIN")
    if data.placa and data.color_placa_id:
        if check_duplicate_composite(
            Vehiculo, {"placa": data.placa, "color_placa_id": data.color_placa_id}
        ):
            raise HttpError(
                409, "Ya existe un vehículo activo con esa placa para el mismo color de placa"
            )

    v = Vehiculo.objects.create(**data.dict())
    v.codigo_qr = _generate_qr(request, v.id)
    v.save(update_fields=["codigo_qr"])

    v = Vehiculo.objects.select_related(*SELECT_RELATED).get(id=v.id)
    return _build_vehiculo_schema(v)


@router.put("/{vehiculo_id}", response=VehiculoSchema, auth=JWTAuth())
@requiere_rol_minimo(Usuario.Rol.NACIONAL)
def update_vehiculo(request, vehiculo_id: int, data: VehiculoUpdate):
    v = get_object_or_404(Vehiculo, vehiculo_id)
    payload = data.dict(exclude_unset=True)

    if "numero_economico" in payload and payload["numero_economico"] != v.numero_economico:
        if check_duplicate(
            Vehiculo, "numero_economico", payload["numero_economico"], exclude_id=vehiculo_id
        ):
            raise HttpError(409, "Ya existe un vehículo activo con ese número económico")
    if "numero_unidad" in payload and payload["numero_unidad"] != v.numero_unidad:
        if check_duplicate(
            Vehiculo, "numero_unidad", payload["numero_unidad"], exclude_id=vehiculo_id
        ):
            raise HttpError(409, "Ya existe un vehículo activo con ese número de unidad")
    if "vin" in payload and payload["vin"] != v.vin:
        if check_duplicate(Vehiculo, "vin", payload["vin"], exclude_id=vehiculo_id):
            raise HttpError(409, "Ya existe un vehículo activo con ese VIN")

    placa = payload.get("placa", v.placa)
    color_placa = payload.get("color_placa_id", v.color_placa_id)
    if placa and color_placa:
        changed_placa = "placa" in payload and payload["placa"] != v.placa
        changed_color = (
            "color_placa_id" in payload and payload["color_placa_id"] != v.color_placa_id
        )
        if changed_placa or changed_color:
            if check_duplicate_composite(
                Vehiculo,
                {"placa": placa, "color_placa_id": color_placa},
                exclude_id=vehiculo_id,
            ):
                raise HttpError(
                    409, "Ya existe un vehículo activo con esa placa para el mismo color de placa"
                )

    for attr, value in payload.items():
        setattr(v, attr, value)
    v.save()

    v = Vehiculo.objects.select_related(*SELECT_RELATED).get(id=vehiculo_id)
    return _build_vehiculo_schema(v)


@router.delete("/{vehiculo_id}", response={204: None}, auth=JWTAuth())
@requiere_rol_minimo(Usuario.Rol.NACIONAL)
def deactivate_vehiculo(request, vehiculo_id: int):
    v = get_object_or_404(Vehiculo, vehiculo_id)
    v.estatus_activo = False
    v.save()
    return 204, None


@router.post("/{vehiculo_id}/regenerar-qr", response=VehiculoSchema, auth=JWTAuth())
@requiere_rol_minimo(Usuario.Rol.NACIONAL)
def regenerar_qr(request, vehiculo_id: int):
    v = get_object_or_404(Vehiculo.objects.select_related(*SELECT_RELATED), vehiculo_id)
    v.codigo_qr = _generate_qr(request, v.id)
    v.save(update_fields=["codigo_qr"])
    return _build_vehiculo_schema(v)
