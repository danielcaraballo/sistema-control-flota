from django.contrib import admin

from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ["username", "email", "rol", "estado", "gerencia", "is_active"]
    search_fields = ["username", "email"]
    list_filter = ["rol", "estado", "is_active"]
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Información personal", {"fields": ("first_name", "last_name", "email")}),
        ("Permisos", {"fields": ("rol", "estado", "gerencia", "is_active", "is_staff", "is_superuser")}),
        ("Fechas", {"fields": ("date_joined", "last_login")}),
    )
