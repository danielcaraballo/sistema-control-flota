from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    class Rol(models.TextChoices):
        NACIONAL = "nacional", "Nacional"
        ESTATAL = "estatal", "Estatal"
        ANALISTA = "analista", "Analista"
        MECANICO = "mecanico", "Mecánico"

    rol = models.CharField(max_length=25, choices=Rol.choices, verbose_name="Rol")
    estado = models.ForeignKey(
        "organizacion.Estado",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Estado",
    )
    email = models.EmailField(unique=True, verbose_name="Correo corporativo")

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_rol_display()})"
