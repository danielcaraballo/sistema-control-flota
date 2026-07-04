from ninja import ModelSchema, Schema

from .models import Vehiculo


class VehiculoSchema(ModelSchema):
    gerencia: int
    gerencia_nombre: str | None = None
    unidad_usuaria: int | None = None
    unidad_usuaria_nombre: str | None = None
    categoria: int
    categoria_nombre: str | None = None
    marca: int
    marca_nombre: str | None = None
    modelo: int
    modelo_nombre: str | None = None
    estado: int
    estado_nombre: str | None = None
    emplazamiento: int
    emplazamiento_nombre: str | None = None
    estatus: int
    estatus_nombre: str | None = None
    color: int | None = None
    color_nombre: str | None = None
    color_placa: int | None = None
    color_placa_nombre: str | None = None

    class Meta:
        model = Vehiculo
        fields = [
            "id",
            "numero_economico",
            "numero_unidad",
            "anio",
            "vin",
            "placa",
            "placa_intt",
            "serial_motor",
            "codigo_qr",
            "estatus_activo",
        ]


class VehiculoCreate(Schema):
    numero_economico: str
    numero_unidad: str | None = None
    gerencia_id: int
    unidad_usuaria_id: int | None = None
    categoria_id: int
    marca_id: int
    modelo_id: int
    anio: int
    vin: str
    estado_id: int
    emplazamiento_id: int
    estatus_id: int
    placa: str | None = None
    color_placa_id: int | None = None
    color_id: int | None = None
    placa_intt: str = ""
    serial_motor: str = ""


class VehiculoUpdate(Schema):
    numero_economico: str | None = None
    numero_unidad: str | None = None
    gerencia_id: int | None = None
    unidad_usuaria_id: int | None = None
    categoria_id: int | None = None
    marca_id: int | None = None
    modelo_id: int | None = None
    anio: int | None = None
    vin: str | None = None
    estado_id: int | None = None
    emplazamiento_id: int | None = None
    estatus_id: int | None = None
    placa: str | None = None
    color_placa_id: int | None = None
    color_id: int | None = None
    placa_intt: str | None = None
    serial_motor: str | None = None
