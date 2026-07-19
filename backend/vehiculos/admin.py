from django.contrib import admin
from unfold.admin import ModelAdmin

from .api import _make_qr_data_uri
from .models import Vehiculo


@admin.register(Vehiculo)
class VehiculoAdmin(ModelAdmin):
    list_display = [
        "numero_economico",
        "numero_unidad",
        "gerencia",
        "marca",
        "modelo",
        "anio",
        "vin",
        "placa",
        "clase",
        "tipo_combustible",
        "estatus",
        "estatus_activo",
    ]
    search_fields = [
        "numero_economico",
        "numero_unidad",
        "vin",
        "placa",
        "marca__nombre",
        "modelo__nombre",
    ]
    list_filter = ["gerencia", "estado", "estatus", "estatus_activo"]

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            super().save_model(request, obj, form, change)
        if not obj.codigo_qr:
            url = request.build_absolute_uri(f"/vehiculos/{obj.pk}")
            obj.codigo_qr = _make_qr_data_uri(url)
            obj.save(update_fields=["codigo_qr"])
        else:
            super().save_model(request, obj, form, change)
