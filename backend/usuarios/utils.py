import re
import secrets
import string

from .models import Usuario

TRANSLIT = str.maketrans("áéíóúüñÁÉÍÓÚÜÑ", "aeiouunAEIOUUN")


def generate_password(length: int = 16) -> str:
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    return "".join(secrets.choice(chars) for _ in range(length))


def generate_username(first_name: str, last_name: str) -> str:
    if not first_name or not last_name:
        return ""

    base = (first_name[0] + last_name).lower()
    base = base.translate(TRANSLIT)
    base = re.sub(r"[^a-z0-9]", "", base)

    username = base
    counter = 1
    while Usuario.objects.filter(username=username).exists():
        counter += 1
        username = f"{base}{counter}"
    return username
