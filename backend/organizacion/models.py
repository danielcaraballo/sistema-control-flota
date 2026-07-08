from django.db import models
from django.db.models import Q


class Estado(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    estatus_activo = models.BooleanField(default=True, verbose_name="Estatus activo")

    class Meta:
        verbose_name = "Estado"
        verbose_name_plural = "Estados"
        ordering = ["nombre"]
        constraints = [
            models.UniqueConstraint(
                fields=["nombre"],
                condition=Q(estatus_activo=True),
                name="unique_active_estado_nombre",
            ),
        ]

    def __str__(self):
        return self.nombre


class Gerencia(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    estatus_activo = models.BooleanField(default=True, verbose_name="Estatus activo")

    class Meta:
        verbose_name = "Gerencia"
        verbose_name_plural = "Gerencias"
        ordering = ["nombre"]
        constraints = [
            models.UniqueConstraint(
                fields=["nombre"],
                condition=Q(estatus_activo=True),
                name="unique_active_gerencia_nombre",
            ),
        ]

    def __str__(self):
        return self.nombre


class CentroDeServicio(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    estado = models.ForeignKey(
        Estado, on_delete=models.RESTRICT, verbose_name="Estado"
    )
    estatus_activo = models.BooleanField(default=True, verbose_name="Estatus activo")

    class Meta:
        verbose_name = "Centro de Servicio"
        verbose_name_plural = "Centros de Servicio"
        ordering = ["nombre"]
        constraints = [
            models.UniqueConstraint(
                fields=["nombre"],
                condition=Q(estatus_activo=True),
                name="unique_active_centrodeservicio_nombre",
            ),
        ]

    def __str__(self):
        return self.nombre
