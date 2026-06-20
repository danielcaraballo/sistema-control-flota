from functools import wraps

from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.errors import HttpError
from ninja_jwt.authentication import JWTAuth

from organizacion.models import Estado, Gerencia
from usuarios.models import Usuario

from .schemas import UsuarioCreate, UsuarioOut, UsuarioUpdate
from .utils import generate_username

router = Router()

ESTATAL_ROLES = {"responsable_estatal", "mecanico"}


def require_roles(*roles: str):
    def decorator(func):
        @wraps(func)
        def wrapper(request, **kwargs):
            user: Usuario = request.auth
            if user.rol not in roles:
                raise HttpError(403, "No tienes permiso para realizar esta acción")
            return func(request, **kwargs)

        return wrapper

    return decorator


def _build_usuario_out(user: Usuario) -> UsuarioOut:
    return UsuarioOut(
        id=user.id,
        username=user.username,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        rol=user.rol,
        estado=user.estado_id,
        gerencia=user.gerencia_id,
        is_active=user.is_active,
        estado_nombre=user.estado.nombre if user.estado else None,
        gerencia_nombre=str(user.gerencia) if user.gerencia else None,
    )


@router.get("/", response=list[UsuarioOut], auth=JWTAuth())
@require_roles("gerente_nacional")
def list_usuarios(request):
    usuarios = Usuario.objects.select_related("estado", "gerencia").all()
    return [_build_usuario_out(u) for u in usuarios]


@router.post("/", response=UsuarioOut, auth=JWTAuth())
@require_roles("gerente_nacional")
def create_usuario(request, data: UsuarioCreate):
    username = data.username or generate_username(data.first_name, data.last_name)
    if not username:
        raise HttpError(400, "Debe proporcionar un nombre de usuario o nombre y apellido")

    if Usuario.objects.filter(username=username).exists():
        raise HttpError(409, "El nombre de usuario ya existe")
    if Usuario.objects.filter(email=data.email).exists():
        raise HttpError(409, "El correo ya está registrado")

    if data.rol in ESTATAL_ROLES and not data.estado_id:
        raise HttpError(400, "Debe asignar un estado para este rol")

    estado = None
    if data.estado_id:
        try:
            estado = Estado.objects.get(id=data.estado_id, estatus_activo=True)
        except Estado.DoesNotExist:
            raise HttpError(400, "Estado no válido")

    gerencia = None
    if data.gerencia_id:
        try:
            gerencia = Gerencia.objects.get(id=data.gerencia_id, estatus_activo=True)
        except Gerencia.DoesNotExist:
            raise HttpError(400, "Gerencia no válida")

    user = Usuario(
        username=username,
        email=data.email,
        first_name=data.first_name,
        last_name=data.last_name,
        rol=data.rol,
        estado=estado,
        gerencia=gerencia,
    )
    user.set_password(data.password)
    user.save()

    return _build_usuario_out(user)


@router.put("/{usuario_id}", response=UsuarioOut, auth=JWTAuth())
@require_roles("gerente_nacional")
def update_usuario(request, usuario_id: int, data: UsuarioUpdate):
    user = get_object_or_404(Usuario, id=usuario_id)

    if data.email is not None and data.email != user.email:
        if Usuario.objects.filter(email=data.email).exclude(id=usuario_id).exists():
            raise HttpError(409, "El correo ya está registrado")
        user.email = data.email

    if data.first_name is not None:
        user.first_name = data.first_name
    if data.last_name is not None:
        user.last_name = data.last_name
    if data.rol is not None:
        user.rol = data.rol
    if data.estado_id is not None:
        try:
            user.estado = Estado.objects.get(id=data.estado_id, estatus_activo=True)
        except Estado.DoesNotExist:
            raise HttpError(400, "Estado no válido")
    if data.gerencia_id is not None:
        try:
            user.gerencia = Gerencia.objects.get(id=data.gerencia_id, estatus_activo=True)
        except Gerencia.DoesNotExist:
            raise HttpError(400, "Gerencia no válida")
    if data.is_active is not None:
        user.is_active = data.is_active

    rol = data.rol or user.rol
    estado = data.estado_id if data.estado_id is not None else user.estado_id
    if rol in ESTATAL_ROLES and not estado:
        raise HttpError(400, "Debe asignar un estado para este rol")

    user.save()
    return _build_usuario_out(user)


@router.delete("/{usuario_id}", response={204: None}, auth=JWTAuth())
@require_roles("gerente_nacional")
def deactivate_usuario(request, usuario_id: int):
    user = get_object_or_404(Usuario, id=usuario_id)
    user.is_active = False
    user.save()
    return 204, None
