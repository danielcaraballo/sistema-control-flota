from ninja import ModelSchema, Schema

from .models import Usuario


class UsuarioOut(ModelSchema):
    estado_nombre: str | None = None
    gerencia_nombre: str | None = None

    class Meta:
        model = Usuario
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "rol",
            "estado",
            "gerencia",
            "is_active",
        ]


class UsuarioCreate(Schema):
    username: str | None = None
    email: str
    password: str
    first_name: str = ""
    last_name: str = ""
    rol: Usuario.Rol
    estado_id: int | None = None
    gerencia_id: int | None = None


class UsuarioUpdate(Schema):
    email: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    rol: Usuario.Rol | None = None
    estado_id: int | None = None
    gerencia_id: int | None = None
    is_active: bool | None = None


class LoginInput(Schema):
    username: str
    password: str


class LoginOutput(Schema):
    access: str
    refresh: str
    user: UsuarioOut


class TokenRefreshInput(Schema):
    refresh: str


class TokenRefreshOutput(Schema):
    access: str
