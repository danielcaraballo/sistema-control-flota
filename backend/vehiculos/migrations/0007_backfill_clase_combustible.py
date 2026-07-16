import django.db.models.deletion
from django.db import migrations, models


def backfill_clase_combustible(apps, schema_editor):
    ClaseVehiculo = apps.get_model("catalogos", "ClaseVehiculo")
    TipoCombustible = apps.get_model("catalogos", "TipoCombustible")
    Vehiculo = apps.get_model("vehiculos", "Vehiculo")

    clase_default = ClaseVehiculo.objects.first()
    combustible_default = TipoCombustible.objects.first()

    if not clase_default or not combustible_default:
        return

    Vehiculo.objects.filter(clase__isnull=True).update(clase=clase_default)
    Vehiculo.objects.filter(tipo_combustible__isnull=True).update(tipo_combustible=combustible_default)


def reverse_backfill(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("vehiculos", "0006_remove_vehiculo_idx_vehiculo_activo_estado_and_more"),
    ]

    operations = [
        migrations.RunPython(backfill_clase_combustible, reverse_backfill),
        migrations.AlterField(
            model_name="vehiculo",
            name="clase",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.RESTRICT,
                to="catalogos.clasevehiculo",
                verbose_name="Clase",
            ),
        ),
        migrations.AlterField(
            model_name="vehiculo",
            name="tipo_combustible",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.RESTRICT,
                to="catalogos.tipocombustible",
                verbose_name="Tipo de combustible",
            ),
        ),
    ]
