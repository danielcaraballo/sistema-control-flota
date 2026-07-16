import django.db.models.deletion
from django.db import migrations, models


def migrate_sistema_afectado(apps, schema_editor):
    SistemaAfectado = apps.get_model("catalogos", "SistemaAfectado")
    TipoFalla = apps.get_model("catalogos", "TipoFalla")

    valores_unicos = (
        TipoFalla.objects
        .values_list("sistema_afectado", flat=True)
        .distinct()
    )
    for valor in valores_unicos:
        SistemaAfectado.objects.get_or_create(
            nombre=valor, defaults={"estatus_activo": True})

    for tf in TipoFalla.objects.all():
        sa = SistemaAfectado.objects.get(nombre=tf.sistema_afectado)
        tf.sistema_afectado_new_id = sa.id
        tf.save()


def reverse_migrate_sistema_afectado(apps, schema_editor):
    TipoFalla = apps.get_model("catalogos", "TipoFalla")
    for tf in TipoFalla.objects.all():
        tf.sistema_afectado = tf.sistema_afectado_new.nombre if tf.sistema_afectado_new else ""
        tf.save()


class Migration(migrations.Migration):

    dependencies = [
        ("catalogos", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="SistemaAfectado",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nombre", models.CharField(max_length=50, unique=True, verbose_name="Nombre")),
                ("estatus_activo", models.BooleanField(default=True, verbose_name="Estatus activo")),
            ],
            options={
                "verbose_name": "Sistema afectado",
                "verbose_name_plural": "Sistemas afectados",
                "ordering": ["nombre"],
            },
        ),
        migrations.AddField(
            model_name="tipofalla",
            name="sistema_afectado_new",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.RESTRICT,
                to="catalogos.sistemaafectado",
                verbose_name="Sistema afectado",
            ),
        ),
        migrations.RunPython(
            migrate_sistema_afectado, reverse_migrate_sistema_afectado),
        migrations.RemoveField(
            model_name="tipofalla",
            name="sistema_afectado",
        ),
        migrations.RenameField(
            model_name="tipofalla",
            old_name="sistema_afectado_new",
            new_name="sistema_afectado",
        ),
    ]
