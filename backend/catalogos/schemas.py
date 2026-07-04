from ninja import ModelSchema, Schema

from .models import (
    Color,
    EstatusVehiculo,
    Marca,
    Modelo,
    SistemaAfectado,
    TipoFalla,
    TipoUso,
    TipoVehiculo,
)


class MarcaSchema(ModelSchema):
    class Meta:
        model = Marca
        fields = ["id", "nombre", "estatus_activo"]


class MarcaCreate(Schema):
    nombre: str


class MarcaUpdate(Schema):
    nombre: str | None = None


class ModeloSchema(ModelSchema):
    marca: int
    marca_nombre: str | None = None

    class Meta:
        model = Modelo
        fields = ["id", "nombre", "estatus_activo"]


class ModeloCreate(Schema):
    nombre: str
    marca_id: int


class ModeloUpdate(Schema):
    nombre: str | None = None
    marca_id: int | None = None


class TipoVehiculoSchema(ModelSchema):
    class Meta:
        model = TipoVehiculo
        fields = ["id", "nombre", "estatus_activo"]


class TipoVehiculoCreate(Schema):
    nombre: str


class TipoVehiculoUpdate(Schema):
    nombre: str | None = None


class TipoUsoSchema(ModelSchema):
    class Meta:
        model = TipoUso
        fields = ["id", "nombre", "estatus_activo"]


class TipoUsoCreate(Schema):
    nombre: str


class TipoUsoUpdate(Schema):
    nombre: str | None = None


class ColorSchema(ModelSchema):
    class Meta:
        model = Color
        fields = ["id", "nombre", "estatus_activo"]


class ColorCreate(Schema):
    nombre: str


class ColorUpdate(Schema):
    nombre: str | None = None


class SistemaAfectadoSchema(ModelSchema):
    class Meta:
        model = SistemaAfectado
        fields = ["id", "nombre", "estatus_activo"]


class SistemaAfectadoCreate(Schema):
    nombre: str


class SistemaAfectadoUpdate(Schema):
    nombre: str | None = None


class TipoFallaSchema(ModelSchema):
    sistema_afectado: int
    sistema_afectado_nombre: str | None = None

    class Meta:
        model = TipoFalla
        fields = ["id", "descripcion", "estatus_activo"]


class TipoFallaCreate(Schema):
    descripcion: str
    sistema_afectado_id: int


class TipoFallaUpdate(Schema):
    descripcion: str | None = None
    sistema_afectado_id: int | None = None


class EstatusVehiculoSchema(ModelSchema):
    class Meta:
        model = EstatusVehiculo
        fields = ["id", "nombre", "estatus_activo"]


class EstatusVehiculoCreate(Schema):
    nombre: str


class EstatusVehiculoUpdate(Schema):
    nombre: str | None = None
