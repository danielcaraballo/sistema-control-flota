from django.db import migrations


ESTADOS = [
    "Amazonas",
    "Anzoátegui",
    "Apure",
    "Aragua",
    "Barinas",
    "Bolívar",
    "Carabobo",
    "Cojedes",
    "Delta Amacuro",
    "Distrito Capital",
    "Falcón",
    "Guárico",
    "La Guaira",
    "Lara",
    "Mérida",
    "Miranda",
    "Monagas",
    "Nueva Esparta",
    "Portuguesa",
    "Sucre",
    "Táchira",
    "Trujillo",
    "Yaracuy",
    "Zulia",
]


def seed_estados(apps, schema_editor):
    Estado = apps.get_model("organizacion", "Estado")
    for nombre in ESTADOS:
        Estado.objects.get_or_create(nombre=nombre, defaults={"estatus_activo": True})


def reverse_seed_estados(apps, schema_editor):
    Estado = apps.get_model("organizacion", "Estado")
    Estado.objects.filter(nombre__in=ESTADOS).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("organizacion", "0002_simplify_gerencia"),
    ]

    operations = [
        migrations.RunPython(seed_estados, reverse_seed_estados),
    ]
