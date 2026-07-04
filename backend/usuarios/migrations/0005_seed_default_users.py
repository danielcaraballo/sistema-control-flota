from django.contrib.auth.hashers import make_password
from django.db import migrations


USERS = [
    {
        "username": "root",
        "password": "root",
        "email": "root@scf.local",
        "first_name": "Super",
        "last_name": "Admin",
        "rol": "nacional",
        "is_staff": True,
        "is_superuser": True,
    },
    {
        "username": "nacional",
        "password": "nacional",
        "email": "nacional@scf.local",
        "first_name": "Usuario",
        "last_name": "Nacional",
        "rol": "nacional",
    },
    {
        "username": "estatal",
        "password": "estatal",
        "email": "estatal@scf.local",
        "first_name": "Usuario",
        "last_name": "Estatal",
        "rol": "estatal",
        "estado_id": 1,
    },
    {
        "username": "analista",
        "password": "analista",
        "email": "analista@scf.local",
        "first_name": "Usuario",
        "last_name": "Analista",
        "rol": "analista",
    },
    {
        "username": "mecanico",
        "password": "mecanico",
        "email": "mecanico@scf.local",
        "first_name": "Usuario",
        "last_name": "Mecanico",
        "rol": "mecanico",
    },
]


def seed_users(apps, schema_editor):
    Usuario = apps.get_model("usuarios", "Usuario")
    for data in USERS:
        Usuario.objects.get_or_create(
            username=data["username"],
            defaults={
                "password": make_password(data["password"]),
                "email": data["email"],
                "first_name": data["first_name"],
                "last_name": data["last_name"],
                "rol": data["rol"],
                "is_staff": data.get("is_staff", False),
                "is_superuser": data.get("is_superuser", False),
                "estado_id": data.get("estado_id"),
            },
        )


def reverse_seed_users(apps, schema_editor):
    Usuario = apps.get_model("usuarios", "Usuario")
    Usuario.objects.filter(username__in=[u["username"] for u in USERS]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("usuarios", "0004_update_roles_and_remove_gerencia"),
    ]

    operations = [
        migrations.RunPython(seed_users, reverse_seed_users),
    ]
