from ninja import Router
from ninja.errors import HttpError
from ninja_jwt.authentication import JWTAuth

from usuarios.models import Usuario
from usuarios.roles import requiere_rol_minimo

from .models import (
    Color,
    Marca,
    Modelo,
    SistemaAfectado,
    TipoFalla,
    TipoUso,
    TipoVehiculo,
)
from .schemas import (
    ColorCreate,
    ColorSchema,
    ColorUpdate,
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


# ─── Marcas ───────────────────────────────────────────────────────────────


@router.get("/marcas/", response=list[MarcaSchema], auth=JWTAuth())
@requiere_rol_minimo(Usuario.Rol.MECANICO)
def list_marcas(request):
    return _filter_activos(Marca.objects.all(), request)


@router.get("/marcas/{marca_id}", response=MarcaSchema, auth=JWTAuth())
@requiere_rol_minimo(Usuario.Rol.MECANICO)
def get_marca(request, marca_id: int):
    return _get_object_or_404(Marca, marca_id)


@router.post("/marcas/", response=MarcaSchema, auth=JWTAuth())
@requiere_rol_minimo(Usuario.Rol.NACIONAL)
def create_marca(request, data: MarcaCreate):
    if Marca.objects.filter(nombre=data.nombre).exists():
        raise HttpError(409, "Ya existe una marca con ese nombre")
    return Marca.objects.create(**data.dict())


@router.put("/marcas/{marca_id}", response=MarcaSchema, auth=JWTAuth())
@requiere_rol_minimo(Usuario.Rol.NACIONAL)
def update_marca(request, marca_id: int, data: MarcaUpdate):
    marca = _get_object_or_404(Marca, marca_id)
    payload = data.dict(exclude_unset=True)
    if "nombre" in payload and payload["nombre"] != marca.nombre:
        if Marca.objects.filter(nombre=payload["nombre"]).exists():
            raise HttpError(409, "Ya existe una marca con ese nombre")
    for attr, value in payload.items():
        setattr(marca, attr, value)
    marca.save()
    return marca


@router.delete("/marcas/{marca_id}", response={204: None}, auth=JWTAuth())
@requiere_rol_minimo(Usuario.Rol.NACIONAL)
def deactivate_marca(request, marca_id: int):
    marca = _get_object_or_404(Marca, marca_id)
    marca.estatus_activo = False
    marca.save()
    return 204, None


# ─── Modelos ──────────────────────────────────────────────────────────────


@router.get("/modelos/", response=list[ModeloSchema], auth=JWTAuth())
@requiere_rol_minimo(Usuario.Rol.MECANICO)
def list_modelos(request):
    qs = Modelo.objects.select_related("marca")
    qs = _filter_activos(qs, request)
    return [
        ModeloSchema(
            id=m.id,
            nombre=m.nombre,
            marca=m.marca_id,
            marca_nombre=m.marca.nombre,
            estatus_activo=m.estatus_activo,
        )
        for m in qs
    ]


@router.get("/modelos/{modelo_id}", response=ModeloSchema, auth=JWTAuth())
@requiere_rol_minimo(Usuario.Rol.MECANICO)
def get_modelo(request, modelo_id: int):
    m = _get_object_or_404(Modelo, modelo_id)
    return ModeloSchema(
        id=m.id,
        nombre=m.nombre,
        marca=m.marca_id,
        marca_nombre=m.marca.nombre,
        estatus_activo=m.estatus_activo,
    )


@router.post("/modelos/", response=ModeloSchema, auth=JWTAuth())
@requiere_rol_minimo(Usuario.Rol.NACIONAL)
def create_modelo(request, data: ModeloCreate):
    if not Marca.objects.filter(id=data.marca_id, estatus_activo=True).exists():
        raise HttpError(400, "La marca especificada no existe o está inactiva")
    if Modelo.objects.filter(nombre=data.nombre, marca_id=data.marca_id).exists():
        raise HttpError(409, "Ya existe ese modelo para esta marca")
    m = Modelo.objects.create(nombre=data.nombre, marca_id=data.marca_id)
    return ModeloSchema(
        id=m.id,
        nombre=m.nombre,
        marca=m.marca_id,
        marca_nombre=m.marca.nombre,
        estatus_activo=m.estatus_activo,
    )


@router.put("/modelos/{modelo_id}", response=ModeloSchema, auth=JWTAuth())
@requiere_rol_minimo(Usuario.Rol.NACIONAL)
def update_modelo(request, modelo_id: int, data: ModeloUpdate):
    m = _get_object_or_404(Modelo, modelo_id)
    payload = data.dict(exclude_unset=True)

    marca_id = payload.get("marca_id", m.marca_id)
    nombre = payload.get("nombre", m.nombre)
    if nombre != m.nombre or marca_id != m.marca_id:
        if Modelo.objects.filter(nombre=nombre, marca_id=marca_id).exclude(id=modelo_id).exists():
            raise HttpError(409, "Ya existe ese modelo para esta marca")

    for attr, value in payload.items():
        setattr(m, attr, value)
    m.save()
    m.refresh_from_db()
    return ModeloSchema(
        id=m.id,
        nombre=m.nombre,
        marca=m.marca_id,
        marca_nombre=m.marca.nombre,
        estatus_activo=m.estatus_activo,
    )


@router.delete("/modelos/{modelo_id}", response={204: None}, auth=JWTAuth())
@requiere_rol_minimo(Usuario.Rol.NACIONAL)
def deactivate_modelo(request, modelo_id: int):
    modelo = _get_object_or_404(Modelo, modelo_id)
    modelo.estatus_activo = False
    modelo.save()
    return 204, None


# ─── Tipos de Vehículo ────────────────────────────────────────────────────


@router.get("/tipos-vehiculo/", response=list[TipoVehiculoSchema], auth=JWTAuth())
@requiere_rol_minimo(Usuario.Rol.MECANICO)
def list_tipos_vehiculo(request):
    return _filter_activos(TipoVehiculo.objects.all(), request)


@router.get("/tipos-vehiculo/{tv_id}", response=TipoVehiculoSchema, auth=JWTAuth())
@requiere_rol_minimo(Usuario.Rol.MECANICO)
def get_tipo_vehiculo(request, tv_id: int):
    return _get_object_or_404(TipoVehiculo, tv_id)


@router.post("/tipos-vehiculo/", response=TipoVehiculoSchema, auth=JWTAuth())
@requiere_rol_minimo(Usuario.Rol.NACIONAL)
def create_tipo_vehiculo(request, data: TipoVehiculoCreate):
    if TipoVehiculo.objects.filter(nombre=data.nombre).exists():
        raise HttpError(409, "Ya existe un tipo de vehículo con ese nombre")
    return TipoVehiculo.objects.create(**data.dict())


@router.put("/tipos-vehiculo/{tv_id}", response=TipoVehiculoSchema, auth=JWTAuth())
@requiere_rol_minimo(Usuario.Rol.NACIONAL)
def update_tipo_vehiculo(request, tv_id: int, data: TipoVehiculoUpdate):
    tv = _get_object_or_404(TipoVehiculo, tv_id)
    payload = data.dict(exclude_unset=True)
    if "nombre" in payload and payload["nombre"] != tv.nombre:
        if TipoVehiculo.objects.filter(nombre=payload["nombre"]).exists():
            raise HttpError(409, "Ya existe un tipo de vehículo con ese nombre")
    for attr, value in payload.items():
        setattr(tv, attr, value)
    tv.save()
    return tv


@router.delete("/tipos-vehiculo/{tv_id}", response={204: None}, auth=JWTAuth())
@requiere_rol_minimo(Usuario.Rol.NACIONAL)
def deactivate_tipo_vehiculo(request, tv_id: int):
    tv = _get_object_or_404(TipoVehiculo, tv_id)
    tv.estatus_activo = False
    tv.save()
    return 204, None


# ─── Tipos de Uso ─────────────────────────────────────────────────────────


@router.get("/tipos-uso/", response=list[TipoUsoSchema], auth=JWTAuth())
@requiere_rol_minimo(Usuario.Rol.MECANICO)
def list_tipos_uso(request):
    return _filter_activos(TipoUso.objects.all(), request)


@router.get("/tipos-uso/{tu_id}", response=TipoUsoSchema, auth=JWTAuth())
@requiere_rol_minimo(Usuario.Rol.MECANICO)
def get_tipo_uso(request, tu_id: int):
    return _get_object_or_404(TipoUso, tu_id)


@router.post("/tipos-uso/", response=TipoUsoSchema, auth=JWTAuth())
@requiere_rol_minimo(Usuario.Rol.NACIONAL)
def create_tipo_uso(request, data: TipoUsoCreate):
    if TipoUso.objects.filter(nombre=data.nombre).exists():
        raise HttpError(409, "Ya existe un tipo de uso con ese nombre")
    return TipoUso.objects.create(**data.dict())


@router.put("/tipos-uso/{tu_id}", response=TipoUsoSchema, auth=JWTAuth())
@requiere_rol_minimo(Usuario.Rol.NACIONAL)
def update_tipo_uso(request, tu_id: int, data: TipoUsoUpdate):
    tu = _get_object_or_404(TipoUso, tu_id)
    payload = data.dict(exclude_unset=True)
    if "nombre" in payload and payload["nombre"] != tu.nombre:
        if TipoUso.objects.filter(nombre=payload["nombre"]).exists():
            raise HttpError(409, "Ya existe un tipo de uso con ese nombre")
    for attr, value in payload.items():
        setattr(tu, attr, value)
    tu.save()
    return tu


@router.delete("/tipos-uso/{tu_id}", response={204: None}, auth=JWTAuth())
@requiere_rol_minimo(Usuario.Rol.NACIONAL)
def deactivate_tipo_uso(request, tu_id: int):
    tu = _get_object_or_404(TipoUso, tu_id)
    tu.estatus_activo = False
    tu.save()
    return 204, None


# ─── Colores ──────────────────────────────────────────────────────────────


@router.get("/colores/", response=list[ColorSchema], auth=JWTAuth())
@requiere_rol_minimo(Usuario.Rol.MECANICO)
def list_colores(request):
    return _filter_activos(Color.objects.all(), request)


@router.get("/colores/{color_id}", response=ColorSchema, auth=JWTAuth())
@requiere_rol_minimo(Usuario.Rol.MECANICO)
def get_color(request, color_id: int):
    return _get_object_or_404(Color, color_id)


@router.post("/colores/", response=ColorSchema, auth=JWTAuth())
@requiere_rol_minimo(Usuario.Rol.NACIONAL)
def create_color(request, data: ColorCreate):
    if Color.objects.filter(nombre=data.nombre).exists():
        raise HttpError(409, "Ya existe un color con ese nombre")
    return Color.objects.create(**data.dict())


@router.put("/colores/{color_id}", response=ColorSchema, auth=JWTAuth())
@requiere_rol_minimo(Usuario.Rol.NACIONAL)
def update_color(request, color_id: int, data: ColorUpdate):
    color = _get_object_or_404(Color, color_id)
    payload = data.dict(exclude_unset=True)
    if "nombre" in payload and payload["nombre"] != color.nombre:
        if Color.objects.filter(nombre=payload["nombre"]).exists():
            raise HttpError(409, "Ya existe un color con ese nombre")
    for attr, value in payload.items():
        setattr(color, attr, value)
    color.save()
    return color


@router.delete("/colores/{color_id}", response={204: None}, auth=JWTAuth())
@requiere_rol_minimo(Usuario.Rol.NACIONAL)
def deactivate_color(request, color_id: int):
    color = _get_object_or_404(Color, color_id)
    color.estatus_activo = False
    color.save()
    return 204, None


# ─── Sistemas Afectados ───────────────────────────────────────────────────


@router.get("/sistemas-afectados/", response=list[SistemaAfectadoSchema], auth=JWTAuth())
@requiere_rol_minimo(Usuario.Rol.MECANICO)
def list_sistemas_afectados(request):
    return _filter_activos(SistemaAfectado.objects.all(), request)


@router.get("/sistemas-afectados/{sa_id}", response=SistemaAfectadoSchema, auth=JWTAuth())
@requiere_rol_minimo(Usuario.Rol.MECANICO)
def get_sistema_afectado(request, sa_id: int):
    return _get_object_or_404(SistemaAfectado, sa_id)


@router.post("/sistemas-afectados/", response=SistemaAfectadoSchema, auth=JWTAuth())
@requiere_rol_minimo(Usuario.Rol.NACIONAL)
def create_sistema_afectado(request, data: SistemaAfectadoCreate):
    if SistemaAfectado.objects.filter(nombre=data.nombre).exists():
        raise HttpError(409, "Ya existe un sistema afectado con ese nombre")
    return SistemaAfectado.objects.create(**data.dict())


@router.put("/sistemas-afectados/{sa_id}", response=SistemaAfectadoSchema, auth=JWTAuth())
@requiere_rol_minimo(Usuario.Rol.NACIONAL)
def update_sistema_afectado(request, sa_id: int, data: SistemaAfectadoUpdate):
    sa = _get_object_or_404(SistemaAfectado, sa_id)
    payload = data.dict(exclude_unset=True)
    if "nombre" in payload and payload["nombre"] != sa.nombre:
        if SistemaAfectado.objects.filter(nombre=payload["nombre"]).exists():
            raise HttpError(409, "Ya existe un sistema afectado con ese nombre")
    for attr, value in payload.items():
        setattr(sa, attr, value)
    sa.save()
    return sa


@router.delete("/sistemas-afectados/{sa_id}", response={204: None}, auth=JWTAuth())
@requiere_rol_minimo(Usuario.Rol.NACIONAL)
def deactivate_sistema_afectado(request, sa_id: int):
    sa = _get_object_or_404(SistemaAfectado, sa_id)
    sa.estatus_activo = False
    sa.save()
    return 204, None


# ─── Tipos de Falla ───────────────────────────────────────────────────────


@router.get("/tipos-falla/", response=list[TipoFallaSchema], auth=JWTAuth())
@requiere_rol_minimo(Usuario.Rol.MECANICO)
def list_tipos_falla(request):
    qs = TipoFalla.objects.select_related("sistema_afectado")
    qs = _filter_activos(qs, request)
    return [
        TipoFallaSchema(
            id=tf.id,
            descripcion=tf.descripcion,
            sistema_afectado=tf.sistema_afectado_id,
            sistema_afectado_nombre=tf.sistema_afectado.nombre,
            estatus_activo=tf.estatus_activo,
        )
        for tf in qs
    ]


@router.get("/tipos-falla/{tf_id}", response=TipoFallaSchema, auth=JWTAuth())
@requiere_rol_minimo(Usuario.Rol.MECANICO)
def get_tipo_falla(request, tf_id: int):
    tf = _get_object_or_404(TipoFalla, tf_id)
    return TipoFallaSchema(
        id=tf.id,
        descripcion=tf.descripcion,
        sistema_afectado=tf.sistema_afectado_id,
        sistema_afectado_nombre=tf.sistema_afectado.nombre,
        estatus_activo=tf.estatus_activo,
    )


@router.post("/tipos-falla/", response=TipoFallaSchema, auth=JWTAuth())
@requiere_rol_minimo(Usuario.Rol.NACIONAL)
def create_tipo_falla(request, data: TipoFallaCreate):
    if not SistemaAfectado.objects.filter(id=data.sistema_afectado_id, estatus_activo=True).exists():
        raise HttpError(400, "El sistema afectado especificado no existe o está inactivo")
    if TipoFalla.objects.filter(descripcion=data.descripcion).exists():
        raise HttpError(409, "Ya existe un tipo de falla con esa descripción")
    tf = TipoFalla.objects.create(
        descripcion=data.descripcion,
        sistema_afectado_id=data.sistema_afectado_id,
    )
    return TipoFallaSchema(
        id=tf.id,
        descripcion=tf.descripcion,
        sistema_afectado=tf.sistema_afectado_id,
        sistema_afectado_nombre=tf.sistema_afectado.nombre,
        estatus_activo=tf.estatus_activo,
    )


@router.put("/tipos-falla/{tf_id}", response=TipoFallaSchema, auth=JWTAuth())
@requiere_rol_minimo(Usuario.Rol.NACIONAL)
def update_tipo_falla(request, tf_id: int, data: TipoFallaUpdate):
    tf = _get_object_or_404(TipoFalla, tf_id)
    payload = data.dict(exclude_unset=True)
    if "descripcion" in payload and payload["descripcion"] != tf.descripcion:
        if TipoFalla.objects.filter(descripcion=payload["descripcion"]).exists():
            raise HttpError(409, "Ya existe un tipo de falla con esa descripción")
    if "sistema_afectado_id" in payload:
        sa_id = payload.pop("sistema_afectado_id")
        if sa_id != tf.sistema_afectado_id:
            if not SistemaAfectado.objects.filter(id=sa_id, estatus_activo=True).exists():
                raise HttpError(400, "El sistema afectado especificado no existe o está inactivo")
            tf.sistema_afectado_id = sa_id
    for attr, value in payload.items():
        setattr(tf, attr, value)
    tf.save()
    tf.refresh_from_db()
    return TipoFallaSchema(
        id=tf.id,
        descripcion=tf.descripcion,
        sistema_afectado=tf.sistema_afectado_id,
        sistema_afectado_nombre=tf.sistema_afectado.nombre,
        estatus_activo=tf.estatus_activo,
    )


@router.delete("/tipos-falla/{tf_id}", response={204: None}, auth=JWTAuth())
@requiere_rol_minimo(Usuario.Rol.NACIONAL)
def deactivate_tipo_falla(request, tf_id: int):
    tf = _get_object_or_404(TipoFalla, tf_id)
    tf.estatus_activo = False
    tf.save()
    return 204, None
