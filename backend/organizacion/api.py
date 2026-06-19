from ninja import Router

from usuarios.auth import AuthBearer

from .models import Estado, Gerencia
from .schemas import EstadoSchema, GerenciaSchema

router = Router()


@router.get("/estados/", response=list[EstadoSchema], auth=AuthBearer())
def list_estados(request):
    return Estado.objects.filter(estatus_activo=True)


@router.get("/gerencias/", response=list[GerenciaSchema], auth=AuthBearer())
def list_gerencias(request):
    return Gerencia.objects.filter(estatus_activo=True)
