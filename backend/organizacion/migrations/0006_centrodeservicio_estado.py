from django.db import migrations, models
import django.db.models.deletion


def assign_default_estado(apps, schema_editor):
    CentroDeServicio = apps.get_model("organizacion", "CentroDeServicio")
    Estado = apps.get_model("organizacion", "Estado")
    default_estado = Estado.objects.first()
    if default_estado:
        CentroDeServicio.objects.filter(estado__isnull=True).update(estado=default_estado)


class Migration(migrations.Migration):
    dependencies = [
        ("organizacion", "0005_alter_centrodeservicio_nombre_alter_estado_nombre_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="centrodeservicio",
            name="estado",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.RESTRICT,
                to="organizacion.estado",
                verbose_name="Estado",
            ),
        ),
        migrations.RunPython(assign_default_estado, reverse_code=migrations.RunPython.noop),
        migrations.AlterField(
            model_name="centrodeservicio",
            name="estado",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.RESTRICT,
                to="organizacion.estado",
                verbose_name="Estado",
            ),
        ),
    ]
