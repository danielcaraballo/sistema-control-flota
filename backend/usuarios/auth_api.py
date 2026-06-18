from ninja import Router
from ninja.errors import HttpError

from django.contrib.auth.hashers import check_password
from usuarios.models import Usuario
from .auth import AuthBearer, create_access_token, create_refresh_token, decode_token
from .schemas import (
    LoginInput,
    LoginOutput,
    TokenRefreshInput,
    TokenRefreshOutput,
    UsuarioOut,
)

router = Router()


@router.post("/login", response=LoginOutput, auth=None)
def login(request, payload: LoginInput):
    try:
        user = Usuario.objects.get(email=payload.email, is_active=True)
    except Usuario.DoesNotExist:
        raise HttpError(401, "Credenciales inválidas")

    if not check_password(payload.password, user.password):
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
