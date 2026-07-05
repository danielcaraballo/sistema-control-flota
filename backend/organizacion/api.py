from django.db import IntegrityError
from ninja import Router
from ninja.errors import HttpError
from ninja_jwt.authentication import JWTAuth

from usuarios.models import Usuario
from usuarios.roles import requiere_rol_minimo

from .models import CentroDeServicio, Estado, Gerencia
from .schemas import (
    CentroDeServicioCreate,
    CentroDeServicioSchema,
    CentroDeServicioUpdate,
    EstadoCreate,
    EstadoSchema,
    EstadoUpdate,
    GerenciaCreate,
    GerenciaSchema,
    GerenciaUpdate,
)

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


# ─── Estados ────────────────────────────────────────────────────────────────


@router.get("/estados/", response=list[EstadoSchema], auth=JWTAuth())
@requiere_rol_minimo(Usuario.Rol.MECANICO)
def list_estados(request):
    return _filter_activos(Estado.objects.all(), request)


@router.get("/estados/{estado_id}", response=EstadoSchema, auth=JWTAuth())
@requiere_rol_minimo(Usuario.Rol.MECANICO)
def get_estado(request, estado_id: int):
    return _get_object_or_404(Estado, estado_id)


@router.post("/estados/", response=EstadoSchema, auth=JWTAuth())
@requiere_rol_minimo(Usuario.Rol.NACIONAL)
def create_estado(request, data: EstadoCreate):
    if Estado.objects.filter(nombre=data.nombre).exists():
        raise HttpError(409, "Ya existe un estado con ese nombre")
    try:
        return Estado.objects.create(**data.dict())
    except IntegrityError:
        raise HttpError(409, "Ya existe un estado con ese nombre")


@router.put("/estados/{estado_id}", response=EstadoSchema, auth=JWTAuth())
@requiere_rol_minimo(Usuario.Rol.NACIONAL)
def update_estado(request, estado_id: int, data: EstadoUpdate):
    estado = _get_object_or_404(Estado, estado_id)
    payload = data.dict(exclude_unset=True)
    if "nombre" in payload and payload["nombre"] != estado.nombre:
        if Estado.objects.filter(nombre=payload["nombre"]).exists():
            raise HttpError(409, "Ya existe un estado con ese nombre")
    for attr, value in payload.items():
        setattr(estado, attr, value)
    try:
        estado.save()
    except IntegrityError:
        raise HttpError(409, "Ya existe un estado con ese nombre")
    return estado


@router.delete("/estados/{estado_id}", response={204: None}, auth=JWTAuth())
@requiere_rol_minimo(Usuario.Rol.NACIONAL)
def deactivate_estado(request, estado_id: int):
    estado = _get_object_or_404(Estado, estado_id)
    estado.estatus_activo = False
    estado.save()
    return 204, None


# ─── Gerencias ──────────────────────────────────────────────────────────────


@router.get("/gerencias/", response=list[GerenciaSchema], auth=JWTAuth())
@requiere_rol_minimo(Usuario.Rol.MECANICO)
def list_gerencias(request):
    return _filter_activos(Gerencia.objects.all(), request)


@router.get("/gerencias/{gerencia_id}", response=GerenciaSchema, auth=JWTAuth())
@requiere_rol_minimo(Usuario.Rol.MECANICO)
def get_gerencia(request, gerencia_id: int):
    return _get_object_or_404(Gerencia, gerencia_id)


@router.post("/gerencias/", response=GerenciaSchema, auth=JWTAuth())
@requiere_rol_minimo(Usuario.Rol.NACIONAL)
def create_gerencia(request, data: GerenciaCreate):
    if Gerencia.objects.filter(nombre=data.nombre).exists():
        raise HttpError(409, "Ya existe una gerencia con ese nombre")
    try:
        return Gerencia.objects.create(**data.dict())
    except IntegrityError:
        raise HttpError(409, "Ya existe una gerencia con ese nombre")


@router.put("/gerencias/{gerencia_id}", response=GerenciaSchema, auth=JWTAuth())
@requiere_rol_minimo(Usuario.Rol.NACIONAL)
def update_gerencia(request, gerencia_id: int, data: GerenciaUpdate):
    gerencia = _get_object_or_404(Gerencia, gerencia_id)
    payload = data.dict(exclude_unset=True)
    if "nombre" in payload and payload["nombre"] != gerencia.nombre:
        if Gerencia.objects.filter(nombre=payload["nombre"]).exists():
            raise HttpError(409, "Ya existe una gerencia con ese nombre")
    for attr, value in payload.items():
        setattr(gerencia, attr, value)
    try:
        gerencia.save()
    except IntegrityError:
        raise HttpError(409, "Ya existe una gerencia con ese nombre")
    return gerencia


@router.delete("/gerencias/{gerencia_id}", response={204: None}, auth=JWTAuth())
@requiere_rol_minimo(Usuario.Rol.NACIONAL)
def deactivate_gerencia(request, gerencia_id: int):
    gerencia = _get_object_or_404(Gerencia, gerencia_id)
    gerencia.estatus_activo = False
    gerencia.save()
    return 204, None


# ─── Centros de Servicio ────────────────────────────────────────────────────


@router.get("/centros-servicio/", response=list[CentroDeServicioSchema], auth=JWTAuth())
@requiere_rol_minimo(Usuario.Rol.MECANICO)
def list_centros_servicio(request):
    return _filter_activos(CentroDeServicio.objects.all(), request)


@router.get("/centros-servicio/{cs_id}", response=CentroDeServicioSchema, auth=JWTAuth())
@requiere_rol_minimo(Usuario.Rol.MECANICO)
def get_centro_servicio(request, cs_id: int):
    return _get_object_or_404(CentroDeServicio, cs_id)


@router.post("/centros-servicio/", response=CentroDeServicioSchema, auth=JWTAuth())
@requiere_rol_minimo(Usuario.Rol.NACIONAL)
def create_centro_servicio(request, data: CentroDeServicioCreate):
    if CentroDeServicio.objects.filter(nombre=data.nombre).exists():
        raise HttpError(409, "Ya existe un centro de servicio con ese nombre")
    try:
        return CentroDeServicio.objects.create(**data.dict())
    except IntegrityError:
        raise HttpError(409, "Ya existe un centro de servicio con ese nombre")


@router.put("/centros-servicio/{cs_id}", response=CentroDeServicioSchema, auth=JWTAuth())
@requiere_rol_minimo(Usuario.Rol.NACIONAL)
def update_centro_servicio(request, cs_id: int, data: CentroDeServicioUpdate):
    cs = _get_object_or_404(CentroDeServicio, cs_id)
    payload = data.dict(exclude_unset=True)
    if "nombre" in payload and payload["nombre"] != cs.nombre:
        if CentroDeServicio.objects.filter(nombre=payload["nombre"]).exists():
            raise HttpError(409, "Ya existe un centro de servicio con ese nombre")
    for attr, value in payload.items():
        setattr(cs, attr, value)
    try:
        cs.save()
    except IntegrityError:
        raise HttpError(409, "Ya existe un centro de servicio con ese nombre")
    return cs


@router.delete("/centros-servicio/{cs_id}", response={204: None}, auth=JWTAuth())
@requiere_rol_minimo(Usuario.Rol.NACIONAL)
def deactivate_centro_servicio(request, cs_id: int):
    cs = _get_object_or_404(CentroDeServicio, cs_id)
    cs.estatus_activo = False
    cs.save()
    return 204, None
