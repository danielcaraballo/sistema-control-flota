from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.errors import HttpError
from ninja_jwt.authentication import JWTAuth

from organizacion.models import Estado
from usuarios.models import Usuario

from .roles import es_estatal, requiere_rol_minimo
from .schemas import (
    ResetPasswordOut,
    UsuarioCreate,
    UsuarioCreateOut,
    UsuarioOut,
    UsuarioUpdate,
)
from .utils import generate_password, generate_username

router = Router()


def _build_usuario_out(user: Usuario) -> UsuarioOut:
    return UsuarioOut(
        id=user.id,
        username=user.username,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        rol=user.rol,
        estado=user.estado_id,
        is_active=user.is_active,
        estado_nombre=user.estado.nombre if user.estado else None,
    )


@router.get("/", response=list[UsuarioOut], auth=JWTAuth())
@requiere_rol_minimo(Usuario.Rol.NACIONAL)
def list_usuarios(request):
    usuarios = Usuario.objects.select_related("estado").all()
    return [_build_usuario_out(u) for u in usuarios]


@router.post("/", response=UsuarioCreateOut, auth=JWTAuth())
@requiere_rol_minimo(Usuario.Rol.NACIONAL)
def create_usuario(request, data: UsuarioCreate):
    username = data.username or generate_username(data.first_name, data.last_name)
    if not username:
        raise HttpError(400, "Debe proporcionar un nombre de usuario o nombre y apellido")

    if Usuario.objects.filter(username=username).exists():
        raise HttpError(409, "El nombre de usuario ya existe")
    if Usuario.objects.filter(email=data.email).exists():
        raise HttpError(409, "El correo ya está registrado")

    if data.rol == Usuario.Rol.NACIONAL and data.estado_id:
        raise HttpError(400, "El rol Nacional no debe tener estado asignado")
    if es_estatal(data.rol) and not data.estado_id:
        raise HttpError(400, "Debe asignar un estado para este rol")

    estado = None
    if data.estado_id:
        try:
            estado = Estado.objects.get(id=data.estado_id, estatus_activo=True)
        except Estado.DoesNotExist:
            raise HttpError(400, "Estado no válido")

    plain_password = data.password or generate_password()
    user = Usuario(
        username=username,
        email=data.email,
        first_name=data.first_name,
        last_name=data.last_name,
        rol=data.rol,
        estado=estado,
    )
    user.set_password(plain_password)
    user.save()

    return {"user": _build_usuario_out(user), "password": plain_password}


@router.put("/{usuario_id}", response=UsuarioOut, auth=JWTAuth())
@requiere_rol_minimo(Usuario.Rol.NACIONAL)
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
    if data.is_active is not None:
        user.is_active = data.is_active

    rol = data.rol or user.rol
    if rol == Usuario.Rol.NACIONAL and data.estado_id is not None:
        if data.estado_id:
            raise HttpError(400, "El rol Nacional no debe tener estado asignado")
    if es_estatal(rol):
        estado_val = data.estado_id if data.estado_id is not None else user.estado_id
        if not estado_val:
            raise HttpError(400, "Debe asignar un estado para este rol")

    user.save()
    return _build_usuario_out(user)


@router.delete("/{usuario_id}", response={204: None}, auth=JWTAuth())
@requiere_rol_minimo(Usuario.Rol.NACIONAL)
def deactivate_usuario(request, usuario_id: int):
    user = get_object_or_404(Usuario, id=usuario_id)
    user.is_active = False
    user.save()
    return 204, None


@router.post("/{usuario_id}/reset-password", response=ResetPasswordOut, auth=JWTAuth())
@requiere_rol_minimo(Usuario.Rol.NACIONAL)
def reset_password(request, usuario_id: int):
    user = get_object_or_404(Usuario, id=usuario_id)
    plain_password = generate_password()
    user.set_password(plain_password)
    user.save()
    return {"password": plain_password}
