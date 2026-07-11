from django.db import migrations

from vehiculos.seed_data import CLASES_VEHICULO, TIPOS_COMBUSTIBLE


def seed_clase_combustible(apps, schema_editor):
    ClaseVehiculo = apps.get_model("catalogos", "ClaseVehiculo")
    TipoCombustible = apps.get_model("catalogos", "TipoCombustible")

    for nombre in CLASES_VEHICULO:
        ClaseVehiculo.objects.get_or_create(
            nombre__iexact=nombre,
            defaults={"nombre": nombre, "estatus_activo": True},
        )

    for nombre in TIPOS_COMBUSTIBLE:
        TipoCombustible.objects.get_or_create(
            nombre__iexact=nombre,
            defaults={"nombre": nombre, "estatus_activo": True},
        )


def reverse_seed(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("catalogos", "0008_clasevehiculo_tipocombustible"),
    ]

    operations = [
        migrations.RunPython(seed_clase_combustible, reverse_seed),
    ]
