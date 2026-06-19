from django.contrib import admin

from .models import Estado, Gerencia


@admin.register(Estado)
class EstadoAdmin(admin.ModelAdmin):
    list_display = ["nombre", "estatus_activo"]
    search_fields = ["nombre"]
    list_filter = ["estatus_activo"]


@admin.register(Gerencia)
class GerenciaAdmin(admin.ModelAdmin):
    list_display = ["nombre", "estado", "estatus_activo"]
    search_fields = ["nombre"]
    list_filter = ["estado", "estatus_activo"]
