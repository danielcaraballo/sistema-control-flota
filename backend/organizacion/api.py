from ninja import Router

from utils.crud_factory import CrudConfig, register_crud

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


def _build_centro_servicio(cs):
    return CentroDeServicioSchema(
        id=cs.id,
        nombre=cs.nombre,
        estatus_activo=cs.estatus_activo,
        estado=cs.estado_id,
        estado_nombre=cs.estado.nombre,
    )


CONFIGS = [
    CrudConfig(
        prefix="estados",
        model=Estado,
        read_schema=EstadoSchema,
        create_schema=EstadoCreate,
        update_schema=EstadoUpdate,
        display_name="estado",
    ),
    CrudConfig(
        prefix="gerencias",
        model=Gerencia,
        read_schema=GerenciaSchema,
        create_schema=GerenciaCreate,
        update_schema=GerenciaUpdate,
        display_name="gerencia",
        article="una",
    ),
    CrudConfig(
        prefix="centros-servicio",
        model=CentroDeServicio,
        read_schema=CentroDeServicioSchema,
        create_schema=CentroDeServicioCreate,
        update_schema=CentroDeServicioUpdate,
        display_name="centro de servicio",
        select_related=["estado"],
        response_builder=_build_centro_servicio,
    ),
]

for cfg in CONFIGS:
    register_crud(router, cfg)
