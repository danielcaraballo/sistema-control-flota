from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import Vehiculo


@admin.register(Vehiculo)
class VehiculoAdmin(ModelAdmin):
    list_display = [
        "numero_economico", "numero_unidad", "gerencia", "marca", "modelo",
        "anio", "vin", "placa", "estatus", "estatus_activo",
    ]
    search_fields = [
        "numero_economico", "numero_unidad", "vin", "placa",
        "marca__nombre", "modelo__nombre",
    ]
    list_filter = ["gerencia", "estado", "estatus", "estatus_activo"]
