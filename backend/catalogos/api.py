from ninja import Router

from utils.crud_factory import CrudConfig, register_crud

from .models import (
    Color,
    ColorPlaca,
    EstatusVehiculo,
    Marca,
    Modelo,
    SistemaAfectado,
    TipoFalla,
    TipoUso,
    TipoVehiculo,
)
from .schemas import (
    ColorCreate,
    ColorPlacaCreate,
    ColorPlacaSchema,
    ColorPlacaUpdate,
    ColorSchema,
    ColorUpdate,
    EstatusVehiculoCreate,
    EstatusVehiculoSchema,
    EstatusVehiculoUpdate,
    MarcaCreate,
    MarcaSchema,
    MarcaUpdate,
    ModeloCreate,
    ModeloSchema,
    ModeloUpdate,
    SistemaAfectadoCreate,
    SistemaAfectadoSchema,
    SistemaAfectadoUpdate,
    TipoFallaCreate,
    TipoFallaSchema,
    TipoFallaUpdate,
    TipoUsoCreate,
    TipoUsoSchema,
    TipoUsoUpdate,
    TipoVehiculoCreate,
    TipoVehiculoSchema,
    TipoVehiculoUpdate,
)

router = Router()


def _build_modelo(m):
    return ModeloSchema(
        id=m.id,
        nombre=m.nombre,
        marca=m.marca_id,
        marca_nombre=m.marca.nombre,
        estatus_activo=m.estatus_activo,
    )


def _build_tipo_falla(tf):
    return TipoFallaSchema(
        id=tf.id,
        descripcion=tf.descripcion,
        sistema_afectado=tf.sistema_afectado_id,
        sistema_afectado_nombre=tf.sistema_afectado.nombre,
        estatus_activo=tf.estatus_activo,
    )


CONFIGS = [
    CrudConfig(
        prefix="marcas",
        model=Marca,
        read_schema=MarcaSchema,
        create_schema=MarcaCreate,
        update_schema=MarcaUpdate,
        display_name="marca",
        article="una",
    ),
    CrudConfig(
        prefix="modelos",
        model=Modelo,
        read_schema=ModeloSchema,
        create_schema=ModeloCreate,
        update_schema=ModeloUpdate,
        display_name="modelo",
        select_related=["marca"],
        response_builder=_build_modelo,
        fk_validations=[
            {
                "field": "marca_id",
                "model": Marca,
                "error_msg": "La marca especificada no existe o está inactiva",
            }
        ],
    ),
    CrudConfig(
        prefix="tipos-vehiculo",
        model=TipoVehiculo,
        read_schema=TipoVehiculoSchema,
        create_schema=TipoVehiculoCreate,
        update_schema=TipoVehiculoUpdate,
        display_name="tipo de vehículo",
    ),
    CrudConfig(
        prefix="tipos-uso",
        model=TipoUso,
        read_schema=TipoUsoSchema,
        create_schema=TipoUsoCreate,
        update_schema=TipoUsoUpdate,
        display_name="tipo de uso",
    ),
    CrudConfig(
        prefix="colores",
        model=Color,
        read_schema=ColorSchema,
        create_schema=ColorCreate,
        update_schema=ColorUpdate,
        display_name="color",
    ),
    CrudConfig(
        prefix="sistemas-afectados",
        model=SistemaAfectado,
        read_schema=SistemaAfectadoSchema,
        create_schema=SistemaAfectadoCreate,
        update_schema=SistemaAfectadoUpdate,
        display_name="sistema afectado",
    ),
    CrudConfig(
        prefix="tipos-falla",
        model=TipoFalla,
        read_schema=TipoFallaSchema,
        create_schema=TipoFallaCreate,
        update_schema=TipoFallaUpdate,
        display_name="tipo de falla",
        article="una",
        unique_field="descripcion",
        unique_field_label="descripción",
        select_related=["sistema_afectado"],
        response_builder=_build_tipo_falla,
        fk_validations=[
            {
                "field": "sistema_afectado_id",
                "model": SistemaAfectado,
                "error_msg": "El sistema afectado especificado no existe o está inactivo",
            }
        ],
    ),
    CrudConfig(
        prefix="estatus-vehiculo",
        model=EstatusVehiculo,
        read_schema=EstatusVehiculoSchema,
        create_schema=EstatusVehiculoCreate,
        update_schema=EstatusVehiculoUpdate,
        display_name="estatus de vehículo",
    ),
    CrudConfig(
        prefix="colores-placa",
        model=ColorPlaca,
        read_schema=ColorPlacaSchema,
        create_schema=ColorPlacaCreate,
        update_schema=ColorPlacaUpdate,
        display_name="color de placa",
        article="un",
    ),
]

for cfg in CONFIGS:
    register_crud(router, cfg)
