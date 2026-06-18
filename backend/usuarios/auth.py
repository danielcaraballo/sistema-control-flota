from datetime import datetime, timedelta
from typing import Any

import jwt
from django.conf import settings
from ninja.security import HttpBearer
from usuarios.models import Usuario


def create_access_token(user: Usuario) -> str:
    payload = {
        "user_id": user.id,
        "username": user.username,
        "email": user.email,
        "rol": user.rol,
        "exp": datetime.utcnow() + timedelta(hours=8),
        "iat": datetime.utcnow(),
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")


def create_refresh_token(user: Usuario) -> str:
    payload = {
        "user_id": user.id,
        "exp": datetime.utcnow() + timedelta(days=7),
        "iat": datetime.utcnow(),
        "type": "refresh",
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")


def decode_token(token: str) -> dict[str, Any]:
    return jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])


class AuthBearer(HttpBearer):
    def authenticate(self, request, token: str) -> Usuario | None:
        try:
            payload = decode_token(token)
            if payload.get("type") == "refresh":
                return None
            user = Usuario.objects.get(id=payload["user_id"], is_active=True)
            return user
        except Exception:
            return None
