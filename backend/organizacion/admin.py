from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import CentroDeServicio, Estado, Gerencia


@admin.register(Estado)
class EstadoAdmin(ModelAdmin):
    list_display = ["nombre", "estatus_activo"]
    search_fields = ["nombre"]
    list_filter = ["estatus_activo"]


@admin.register(Gerencia)
class GerenciaAdmin(ModelAdmin):
    list_display = ["nombre", "estatus_activo"]
    search_fields = ["nombre"]
    list_filter = ["estatus_activo"]


@admin.register(CentroDeServicio)
class CentroDeServicioAdmin(ModelAdmin):
    list_display = ["nombre", "estatus_activo"]
    search_fields = ["nombre"]
    list_filter = ["estatus_activo"]
