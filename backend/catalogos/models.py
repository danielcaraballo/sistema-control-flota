from django.db import models
from django.db.models import Q


class Marca(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    estatus_activo = models.BooleanField(default=True, verbose_name="Estatus activo")

    class Meta:
        verbose_name = "Marca"
        verbose_name_plural = "Marcas"
        ordering = ["nombre"]
        constraints = [
            models.UniqueConstraint(
                fields=["nombre"],
                condition=Q(estatus_activo=True),
                name="unique_active_marca_nombre",
            ),
        ]

    def __str__(self):
        return self.nombre


class Modelo(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE, verbose_name="Marca")
    estatus_activo = models.BooleanField(default=True, verbose_name="Estatus activo")

    class Meta:
        verbose_name = "Modelo"
        verbose_name_plural = "Modelos"
        ordering = ["marca__nombre", "nombre"]
        constraints = [
            models.UniqueConstraint(
                fields=["nombre", "marca"],
                condition=Q(estatus_activo=True),
                name="unique_active_modelo_nombre_marca",
            ),
        ]

    def __str__(self):
        return f"{self.marca.nombre} {self.nombre}"


class TipoVehiculo(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    estatus_activo = models.BooleanField(default=True, verbose_name="Estatus activo")

    class Meta:
        verbose_name = "Tipo de vehículo"
        verbose_name_plural = "Tipos de vehículo"
        ordering = ["nombre"]
        constraints = [
            models.UniqueConstraint(
                fields=["nombre"],
                condition=Q(estatus_activo=True),
                name="unique_active_tipovehiculo_nombre",
            ),
        ]

    def __str__(self):
        return self.nombre


class TipoUso(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    estatus_activo = models.BooleanField(default=True, verbose_name="Estatus activo")

    class Meta:
        verbose_name = "Tipo de uso"
        verbose_name_plural = "Tipos de uso"
        ordering = ["nombre"]
        constraints = [
            models.UniqueConstraint(
                fields=["nombre"],
                condition=Q(estatus_activo=True),
                name="unique_active_tipouso_nombre",
            ),
        ]

    def __str__(self):
        return self.nombre


class Color(models.Model):
    nombre = models.CharField(max_length=50, verbose_name="Nombre")
    estatus_activo = models.BooleanField(default=True, verbose_name="Estatus activo")

    class Meta:
        verbose_name = "Color"
        verbose_name_plural = "Colores"
        ordering = ["nombre"]
        constraints = [
            models.UniqueConstraint(
                fields=["nombre"],
                condition=Q(estatus_activo=True),
                name="unique_active_color_nombre",
            ),
        ]

    def __str__(self):
        return self.nombre


class SistemaAfectado(models.Model):
    nombre = models.CharField(max_length=50, verbose_name="Nombre")
    estatus_activo = models.BooleanField(default=True, verbose_name="Estatus activo")

    class Meta:
        verbose_name = "Sistema afectado"
        verbose_name_plural = "Sistemas afectados"
        ordering = ["nombre"]
        constraints = [
            models.UniqueConstraint(
                fields=["nombre"],
                condition=Q(estatus_activo=True),
                name="unique_active_sistemaafectado_nombre",
            ),
        ]

    def __str__(self):
        return self.nombre


class EstatusVehiculo(models.Model):
    nombre = models.CharField(max_length=50, verbose_name="Nombre")
    estatus_activo = models.BooleanField(default=True, verbose_name="Estatus activo")

    class Meta:
        verbose_name = "Estatus de vehículo"
        verbose_name_plural = "Estatus de vehículos"
        ordering = ["nombre"]
        constraints = [
            models.UniqueConstraint(
                fields=["nombre"],
                condition=Q(estatus_activo=True),
                name="unique_active_estatusvehiculo_nombre",
            ),
        ]

    def __str__(self):
        return self.nombre


class ColorPlaca(models.Model):
    nombre = models.CharField(max_length=50, verbose_name="Nombre")
    estatus_activo = models.BooleanField(default=True, verbose_name="Estatus activo")

    class Meta:
        verbose_name = "Color de placa"
        verbose_name_plural = "Colores de placa"
        ordering = ["nombre"]
        constraints = [
            models.UniqueConstraint(
                fields=["nombre"],
                condition=Q(estatus_activo=True),
                name="unique_active_colorplaca_nombre",
            ),
        ]

    def __str__(self):
        return self.nombre


class ClaseVehiculo(models.Model):
    nombre = models.CharField(max_length=50, verbose_name="Nombre")
    estatus_activo = models.BooleanField(default=True, verbose_name="Estatus activo")

    class Meta:
        verbose_name = "Clase de vehículo"
        verbose_name_plural = "Clases de vehículo"
        ordering = ["nombre"]
        constraints = [
            models.UniqueConstraint(
                fields=["nombre"],
                condition=Q(estatus_activo=True),
                name="unique_active_clasevehiculo_nombre",
            ),
        ]

    def __str__(self):
        return self.nombre


class TipoCombustible(models.Model):
    nombre = models.CharField(max_length=50, verbose_name="Nombre")
    estatus_activo = models.BooleanField(default=True, verbose_name="Estatus activo")

    class Meta:
        verbose_name = "Tipo de combustible"
        verbose_name_plural = "Tipos de combustible"
        ordering = ["nombre"]
        constraints = [
            models.UniqueConstraint(
                fields=["nombre"],
                condition=Q(estatus_activo=True),
                name="unique_active_tipocombustible_nombre",
            ),
        ]

    def __str__(self):
        return self.nombre


class TipoFalla(models.Model):
    descripcion = models.CharField(max_length=200, verbose_name="Descripción")
    sistema_afectado = models.ForeignKey(
        SistemaAfectado, on_delete=models.RESTRICT, null=True, verbose_name="Sistema afectado"
    )
    estatus_activo = models.BooleanField(default=True, verbose_name="Estatus activo")

    class Meta:
        verbose_name = "Tipo de falla"
        verbose_name_plural = "Tipos de falla"
        ordering = ["descripcion"]
        constraints = [
            models.UniqueConstraint(
                fields=["descripcion"],
                condition=Q(estatus_activo=True),
                name="unique_active_tipofalla_descripcion",
            ),
        ]

    def __str__(self):
        return self.descripcion
