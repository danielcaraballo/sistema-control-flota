from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("vehiculos", "0004_vehiculo_tipo_uso"),
    ]

    operations = [
        migrations.AddIndex(
            model_name="vehiculo",
            index=models.Index(
                fields=["estatus_activo", "estado_id"],
                name="idx_vehiculo_activo_estado",
            ),
        ),
        migrations.AddIndex(
            model_name="vehiculo",
            index=models.Index(
                fields=["estatus_id"],
                name="idx_vehiculo_estatus",
            ),
        ),
        migrations.AddIndex(
            model_name="vehiculo",
            index=models.Index(
                fields=["gerencia_id"],
                name="idx_vehiculo_gerencia",
            ),
        ),
    ]
