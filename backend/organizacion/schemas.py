from ninja import ModelSchema

from .models import Estado, Gerencia


class EstadoSchema(ModelSchema):
    class Meta:
        model = Estado
        fields = ["id", "nombre", "estatus_activo"]


class GerenciaSchema(ModelSchema):
    class Meta:
        model = Gerencia
        fields = ["id", "nombre", "estatus_activo"]
