from django.apps import apps
from django.core.management.base import BaseCommand, CommandError

from seeds import loaders

APP_LOADERS = {
    "organizacion": [
        ("organizacion", "Estado", loaders.load_estados),
        ("organizacion", "Gerencia", loaders.load_gerencias),
        ("organizacion", "CentroDeServicio", loaders.load_centros, "Estado"),
    ],
    "catalogos": [
        ("catalogos", "Marca", loaders.load_marcas_modelos, "Modelo"),
        ("catalogos", "Color", loaders.load_colores),
        ("catalogos", "EstatusVehiculo", loaders.load_estatus_vehiculo),
        ("catalogos", "ColorPlaca", loaders.load_colores_placa),
        ("catalogos", "TipoVehiculo", loaders.load_tipos_vehiculo),
        ("catalogos", "TipoUso", loaders.load_tipos_uso),
        ("catalogos", "ClaseVehiculo", loaders.load_clases_vehiculo),
        ("catalogos", "TipoCombustible", loaders.load_tipos_combustible),
        ("catalogos", "SistemaAfectado", loaders.load_sistemas_fallas, "TipoFalla"),
    ],
    "usuarios": [
        ("usuarios", "Usuario", loaders.load_usuarios),
    ],
}


class Command(BaseCommand):
    help = "Carga datos de referencia desde archivos JSON en seeds/"

    def add_arguments(self, parser):
        parser.add_argument(
            "--app",
            choices=[*list(APP_LOADERS), "all"],
            default="all",
            help="App cuyos datos de referencia cargar",
        )
        parser.add_argument(
            "--incluir-inactivos",
            action="store_true",
            default=False,
            help="No desactiva registros que sobran respecto al JSON",
        )

    def handle(self, **options):
        app = options["app"]
        incluir_inactivos = options["incluir_inactivos"]
        apps_to_load = list(APP_LOADERS) if app == "all" else [app]

        for app_label in apps_to_load:
            self.stdout.write(f"Cargando datos para {app_label}...")
            for loader_def in APP_LOADERS[app_label]:
                self._run_loader(app_label, loader_def, incluir_inactivos)

        self.stdout.write(self.style.SUCCESS("Datos de referencia cargados correctamente."))

    def _run_loader(self, app_label, loader_def, incluir_inactivos):
        if len(loader_def) == 3:
            app_name, model_name, loader_fn = loader_def
            extra_args = []
        elif len(loader_def) == 4:
            app_name, model_name, loader_fn, extra_model = loader_def
            extra_args = [apps.get_model(app_name, extra_model)]
        else:
            raise CommandError(f"Formato inválido: {loader_def}")

        model = apps.get_model(app_name, model_name)
        self.stdout.write(f"  {model._meta.verbose_name}...", ending=" ")
        loader_fn(model, *extra_args, incluir_inactivos=incluir_inactivos)
        self.stdout.write(self.style.SUCCESS("OK"))
