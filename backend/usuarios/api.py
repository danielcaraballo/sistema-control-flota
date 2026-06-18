from typing import List

from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.errors import HttpError

from organizacion.models import Gerencia
from usuarios.models import Usuario

from .auth import AuthBearer, create_access_token, create_refresh_token, decode_token
from .schemas import (
    LoginInput,
    LoginOutput,
    TokenRefreshInput,
    TokenRefreshOutput,
    UsuarioCreate,
    UsuarioOut,
    UsuarioUpdate,
)

router = Router()


def require_roles(*roles: str):
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            user: Usuario = request.auth
            if user.rol not in roles:
                raise HttpError(403, "No tienes permiso para realizar esta acción")
            return func(request, *args, **kwargs)

        return wrapper

    return decorator


@router.post("/login", response=LoginOutput, auth=None)
def login(request, payload: LoginInput):
    try:
        user = Usuario.objects.get(email=payload.email, is_active=True)
        if not user.check_password(payload.password):
            raise HttpError(401, "Credenciales inválidas")
    except Usuario.DoesNotExist:
        raise HttpError(401, "Credenciales inválidas")

    access = create_access_token(user)
    refresh = create_refresh_token(user)

    return LoginOutput(
        access=access,
        refresh=refresh,
        user=UsuarioOut(
            id=user.id,
            username=user.username,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            rol=user.rol,
            gerencia=user.gerencia_id,
            is_active=user.is_active,
            gerencia_nombre=str(user.gerencia) if user.gerencia else None,
            estado_nombre=user.gerencia.estado.nombre if user.gerencia else None,
        ),
    )


@router.post("/refresh", response=TokenRefreshOutput, auth=None)
def refresh_token(request, payload: TokenRefreshInput):
    try:
        payload_data = decode_token(payload.refresh)
        if payload_data.get("type") != "refresh":
            raise HttpError(401, "Token inválido")
        user = Usuario.objects.get(id=payload_data["user_id"], is_active=True)
        return TokenRefreshOutput(access=create_access_token(user))
    except Exception:
        raise HttpError(401, "Token inválido o expirado")


@router.get("/me", response=UsuarioOut, auth=AuthBearer())
def me(request):
    user: Usuario = request.auth
    return UsuarioOut(
        id=user.id,
        username=user.username,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        rol=user.rol,
        gerencia=user.gerencia_id,
        is_active=user.is_active,
        gerencia_nombre=str(user.gerencia) if user.gerencia else None,
        estado_nombre=user.gerencia.estado.nombre if user.gerencia else None,
    )


@router.get("/", response=List[UsuarioOut], auth=AuthBearer())
@require_roles("gerente_nacional")
def list_usuarios(request):
    usuarios = Usuario.objects.select_related("gerencia__estado").all()
    result = []
    for u in usuarios:
        result.append(
            UsuarioOut(
                id=u.id,
                username=u.username,
                email=u.email,
                first_name=u.first_name,
                last_name=u.last_name,
                rol=u.rol,
                gerencia=u.gerencia_id,
                is_active=u.is_active,
                gerencia_nombre=str(u.gerencia) if u.gerencia else None,
                estado_nombre=u.gerencia.estado.nombre if u.gerencia else None,
            )
        )
    return result


@router.post("/", response=UsuarioOut, auth=AuthBearer())
@require_roles("gerente_nacional")
def create_usuario(request, data: UsuarioCreate):
    if Usuario.objects.filter(username=data.username).exists():
        raise HttpError(409, "El nombre de usuario ya existe")
    if Usuario.objects.filter(email=data.email).exists():
        raise HttpError(409, "El correo ya está registrado")

    if data.rol != "gerente_nacional" and not data.gerencia_id:
        raise HttpError(400, "Debe asignar una gerencia para este rol")

    gerencia = None
    if data.gerencia_id:
        gerencia = get_object_or_404(Gerencia, id=data.gerencia_id, estatus_activo=True)

    user = Usuario.objects.create(
        username=data.username,
        email=data.email,
        password=make_password(data.password),
        first_name=data.first_name,
        last_name=data.last_name,
        rol=data.rol,
        gerencia=gerencia,
    )

    return UsuarioOut(
        id=user.id,
        username=user.username,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        rol=user.rol,
        gerencia=user.gerencia_id,
        is_active=user.is_active,
        gerencia_nombre=str(user.gerencia) if user.gerencia else None,
        estado_nombre=user.gerencia.estado.nombre if user.gerencia else None,
    )


@router.put("/{usuario_id}", response=UsuarioOut, auth=AuthBearer())
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
    if data.gerencia_id is not None:
        user.gerencia = get_object_or_404(Gerencia, id=data.gerencia_id, estatus_activo=True)
    if data.is_active is not None:
        user.is_active = data.is_active

    if user.rol != "gerente_nacional" and not user.gerencia:
        raise HttpError(400, "Debe asignar una gerencia para este rol")

    user.save()

    return UsuarioOut(
        id=user.id,
        username=user.username,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        rol=user.rol,
        gerencia=user.gerencia_id,
        is_active=user.is_active,
        gerencia_nombre=str(user.gerencia) if user.gerencia else None,
        estado_nombre=user.gerencia.estado.nombre if user.gerencia else None,
    )
