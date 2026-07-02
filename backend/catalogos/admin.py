from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import (
    Color,
    Marca,
    Modelo,
    SistemaAfectado,
    TipoFalla,
    TipoUso,
    TipoVehiculo,
)


@admin.register(Marca)
class MarcaAdmin(ModelAdmin):
    list_display = ["nombre", "estatus_activo"]
    search_fields = ["nombre"]
    list_filter = ["estatus_activo"]


@admin.register(Modelo)
class ModeloAdmin(ModelAdmin):
    list_display = ["nombre", "marca", "estatus_activo"]
    search_fields = ["nombre", "marca__nombre"]
    list_filter = ["marca", "estatus_activo"]


@admin.register(TipoVehiculo)
class TipoVehiculoAdmin(ModelAdmin):
    list_display = ["nombre", "estatus_activo"]
    search_fields = ["nombre"]
    list_filter = ["estatus_activo"]


@admin.register(TipoUso)
class TipoUsoAdmin(ModelAdmin):
    list_display = ["nombre", "estatus_activo"]
    search_fields = ["nombre"]
    list_filter = ["estatus_activo"]


@admin.register(Color)
class ColorAdmin(ModelAdmin):
    list_display = ["nombre", "estatus_activo"]
    search_fields = ["nombre"]
    list_filter = ["estatus_activo"]


@admin.register(SistemaAfectado)
class SistemaAfectadoAdmin(ModelAdmin):
    list_display = ["nombre", "estatus_activo"]
    search_fields = ["nombre"]
    list_filter = ["estatus_activo"]


@admin.register(TipoFalla)
class TipoFallaAdmin(ModelAdmin):
    list_display = ["descripcion", "sistema_afectado", "estatus_activo"]
    search_fields = ["descripcion", "sistema_afectado__nombre"]
    list_filter = ["sistema_afectado", "estatus_activo"]
