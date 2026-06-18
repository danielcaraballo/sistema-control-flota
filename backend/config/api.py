from ninja import NinjaAPI
from ninja.errors import ValidationError

from usuarios.auth import AuthBearer
from usuarios.auth_api import router as auth_router
from usuarios.usuarios_api import router as usuarios_router

api = NinjaAPI(
    title="SCF - Sistema de Control de Flota",
    version="1.0.0",
    description="API para la gestión integral de flota vehicular corporativa",
    auth=AuthBearer(),
)

api.add_router("/auth/", auth_router, tags=["Autenticación"])
api.add_router("/usuarios/", usuarios_router, tags=["Usuarios"])
