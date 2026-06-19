from django.db.models import Q
from ninja import Router
from ninja.errors import HttpError

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
    user = Usuario.objects.filter(
        Q(email=payload.username) | Q(username=payload.username),
        is_active=True,
    ).first()

    if not user or not user.check_password(payload.password):
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
            estado=user.estado_id,
            gerencia=user.gerencia_id,
            is_active=user.is_active,
            estado_nombre=user.estado.nombre if user.estado else None,
            gerencia_nombre=str(user.gerencia) if user.gerencia else None,
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
        estado=user.estado_id,
        gerencia=user.gerencia_id,
        is_active=user.is_active,
        estado_nombre=user.estado.nombre if user.estado else None,
        gerencia_nombre=str(user.gerencia) if user.gerencia else None,
    )
