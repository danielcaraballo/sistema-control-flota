from ninja import NinjaAPI
from ninja_jwt.authentication import JWTAuth

from organizacion.api import router as organizacion_router
from usuarios.auth_api import router as auth_router
from usuarios.usuarios_api import router as usuarios_router

api = NinjaAPI(
    title="SCF - Sistema de Control de Flota",
    version="1.0.0",
    description="API del Sistema de Control de Flota (SCF).",
    auth=JWTAuth(),
)

api.add_router("/auth/", auth_router, tags=["Autenticación"])
api.add_router("/usuarios/", usuarios_router, tags=["Usuarios"])
api.add_router("/organizacion/", organizacion_router, tags=["Organización"])
