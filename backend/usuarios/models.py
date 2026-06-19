from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    class Rol(models.TextChoices):
        GERENTE_NACIONAL = "gerente_nacional", "Gerente Nacional"
        ANALISTA_NACIONAL = "analista_nacional", "Analista Nacional"
        RESPONSABLE_ESTATAL = "responsable_estatal", "Responsable Estatal"
        MECANICO = "mecanico", "Mecánico"

    rol = models.CharField(max_length=25, choices=Rol.choices, verbose_name="Rol")
    gerencia = models.ForeignKey(
        "organizacion.Gerencia",
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        related_name="usuarios",
        verbose_name="Gerencia",
    )
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
