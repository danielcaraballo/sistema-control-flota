from django.db.models import Q
from ninja import Router
from ninja.errors import HttpError
from ninja_jwt.authentication import JWTAuth
from ninja_jwt.tokens import RefreshToken

from usuarios.models import Usuario

from .schemas import ChangePasswordInput, LoginInput, LoginOutput, RefreshInput, UsuarioOut

router = Router()


@router.post("/login", response=LoginOutput, auth=None)
def login(request, payload: LoginInput):
    user = Usuario.objects.filter(
        Q(email=payload.username) | Q(username=payload.username),
        is_active=True,
    ).first()

    if not user or not user.check_password(payload.password):
        raise HttpError(401, "Credenciales inválidas")

    refresh = RefreshToken.for_user(user)
    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
        "user": UsuarioOut(
            id=user.id,
            username=user.username,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            rol=user.rol,
            estado=user.estado_id,
            is_active=user.is_active,
            estado_nombre=user.estado.nombre if user.estado else None,
        ),
    }


@router.post("/refresh", auth=None)
def refresh_token(request, payload: RefreshInput):
    try:
        token = RefreshToken(payload.refresh)
        return {"access": str(token.access_token)}
    except Exception:
        raise HttpError(401, "Token inválido o expirado")


@router.get("/me", response=UsuarioOut, auth=JWTAuth())
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
        is_active=user.is_active,
        estado_nombre=user.estado.nombre if user.estado else None,
    )


@router.post("/change-password", auth=JWTAuth())
def change_password(request, payload: ChangePasswordInput):
    user: Usuario = request.auth
    if not user.check_password(payload.current_password):
        raise HttpError(400, "La contraseña actual no es correcta")
    if len(payload.new_password) < 8:
        raise HttpError(400, "La nueva contraseña debe tener al menos 8 caracteres")
    user.set_password(payload.new_password)
    user.save()
    return {"detail": "Contraseña cambiada exitosamente"}
