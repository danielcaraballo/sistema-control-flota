from ninja import Schema


class EstatusKPI(Schema):
    id: int
    nombre: str
    cantidad: int


class MarcaItem(Schema):
    id: int
    nombre: str
    cantidad: int


class AnioItem(Schema):
    anio: int
    cantidad: int


class KPIsResponse(Schema):
    total_vehiculos: int
    porcentaje_operatividad: float
    operativos: int
    inactivos: int
    completitud_promedio: float
    estatus: list[EstatusKPI]


class EstadoDashboardItem(Schema):
    estado_nombre: str
    total: int
    operatividad: float
    activos: int
    inactivos: int


class EstadoResumen(EstadoDashboardItem):
    estatus: list[EstatusKPI]


class ChartsResponse(Schema):
    por_estado: list[EstadoDashboardItem]
    por_marca: list[MarcaItem]
    por_anio: list[AnioItem]


class NacionalResponse(Schema):
    resumen_estados: list[EstadoResumen]
    total_vehiculos: int
    total_estados_con_vehiculos: int
    mejor_operatividad: EstadoDashboardItem | None = None
    peor_operatividad: EstadoDashboardItem | None = None
