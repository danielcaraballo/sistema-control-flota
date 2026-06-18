from django.db import models


class Estado(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre")
    estatus_activo = models.BooleanField(default=True, verbose_name="Estatus activo")

    class Meta:
        verbose_name = "Estado"
        verbose_name_plural = "Estados"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Gerencia(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    estado = models.ForeignKey(
        Estado, on_delete=models.RESTRICT, related_name="gerencias", verbose_name="Estado"
    )
    estatus_activo = models.BooleanField(default=True, verbose_name="Estatus activo")

    class Meta:
        verbose_name = "Gerencia"
        verbose_name_plural = "Gerencias"
        ordering = ["estado__nombre", "nombre"]
        unique_together = ["nombre", "estado"]

    def __str__(self):
        return f"{self.nombre} - {self.estado.nombre}"
