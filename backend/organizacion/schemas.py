from ninja import ModelSchema, Schema

from .models import CentroDeServicio, Estado, Gerencia


class EstadoSchema(ModelSchema):
    class Meta:
        model = Estado
        fields = ["id", "nombre", "estatus_activo"]


class EstadoCreate(Schema):
    nombre: str


class EstadoUpdate(Schema):
    nombre: str | None = None
    estatus_activo: bool | None = None


class GerenciaSchema(ModelSchema):
    class Meta:
        model = Gerencia
        fields = ["id", "nombre", "estatus_activo"]


class GerenciaCreate(Schema):
    nombre: str


class GerenciaUpdate(Schema):
    nombre: str | None = None
    estatus_activo: bool | None = None


class CentroDeServicioSchema(ModelSchema):
    estado: int
    estado_nombre: str | None = None

    class Meta:
        model = CentroDeServicio
        fields = ["id", "nombre", "estatus_activo"]


class CentroDeServicioCreate(Schema):
    nombre: str
    estado_id: int


class CentroDeServicioUpdate(Schema):
    nombre: str | None = None
    estado_id: int | None = None
    estatus_activo: bool | None = None
