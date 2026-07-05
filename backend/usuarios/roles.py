from functools import wraps

from ninja.errors import HttpError

from .models import Usuario

ROLE_HIERARCHY = {
    Usuario.Rol.MECANICO: None,
    Usuario.Rol.ANALISTA: Usuario.Rol.MECANICO,
    Usuario.Rol.ESTATAL: Usuario.Rol.ANALISTA,
    Usuario.Rol.NACIONAL: Usuario.Rol.ESTATAL,
}


def hereda_de(rol_hijo: str, rol_minimo: str) -> bool:
    """True si rol_hijo es igual o superior a rol_minimo en la jerarquía."""
    current = rol_hijo
    while current:
        if current == rol_minimo:
            return True
        current = ROLE_HIERARCHY.get(current)
    return False


def es_estatal(rol: str) -> bool:
    return rol in {Usuario.Rol.ESTATAL, Usuario.Rol.ANALISTA, Usuario.Rol.MECANICO}


def requiere_rol_minimo(rol_minimo: str):
    """Decorador: el usuario autenticado debe tener al menos este rol."""

    def decorator(func):
        @wraps(func)
        def wrapper(request, **kwargs):
            user: Usuario = request.auth
            if not hereda_de(user.rol, rol_minimo):
                raise HttpError(403, "No tienes permiso para realizar esta acción")
            return func(request, **kwargs)

        return wrapper

    return decorator


def acotar_por_estado(user: Usuario, queryset, campo_estado: str = "estado"):
    """Filtra queryset al estado del usuario. Nacional ve todo."""
    if user.rol == Usuario.Rol.NACIONAL:
        return queryset
    return queryset.filter(**{campo_estado: user.estado})
