from ninja import Router
from ninja_jwt.authentication import JWTAuth

from usuarios.models import Usuario
from usuarios.roles import requiere_rol_minimo

from .models import Estado, Gerencia
from .schemas import EstadoSchema, GerenciaSchema

router = Router()


@router.get("/estados/", response=list[EstadoSchema], auth=JWTAuth())
@requiere_rol_minimo(Usuario.Rol.MECANICO)
def list_estados(request):
    return Estado.objects.filter(estatus_activo=True)


@router.get("/gerencias/", response=list[GerenciaSchema], auth=JWTAuth())
@requiere_rol_minimo(Usuario.Rol.MECANICO)
def list_gerencias(request):
    return Gerencia.objects.filter(estatus_activo=True)
