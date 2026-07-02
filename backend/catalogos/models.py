from django.db import models


class Marca(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre")
    estatus_activo = models.BooleanField(default=True, verbose_name="Estatus activo")

    class Meta:
        verbose_name = "Marca"
        verbose_name_plural = "Marcas"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Modelo(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    marca = models.ForeignKey(
        Marca, on_delete=models.CASCADE, verbose_name="Marca")
    estatus_activo = models.BooleanField(default=True, verbose_name="Estatus activo")

    class Meta:
        verbose_name = "Modelo"
        verbose_name_plural = "Modelos"
        ordering = ["marca__nombre", "nombre"]
        unique_together = ("nombre", "marca")

    def __str__(self):
        return f"{self.marca.nombre} {self.nombre}"


class TipoVehiculo(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre")
    estatus_activo = models.BooleanField(default=True, verbose_name="Estatus activo")

    class Meta:
        verbose_name = "Tipo de vehículo"
        verbose_name_plural = "Tipos de vehículo"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class TipoUso(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre")
    estatus_activo = models.BooleanField(default=True, verbose_name="Estatus activo")

    class Meta:
        verbose_name = "Tipo de uso"
        verbose_name_plural = "Tipos de uso"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Color(models.Model):
    nombre = models.CharField(max_length=50, unique=True, verbose_name="Nombre")
    estatus_activo = models.BooleanField(default=True, verbose_name="Estatus activo")

    class Meta:
        verbose_name = "Color"
        verbose_name_plural = "Colores"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class SistemaAfectado(models.Model):
    nombre = models.CharField(max_length=50, unique=True, verbose_name="Nombre")
    estatus_activo = models.BooleanField(default=True, verbose_name="Estatus activo")

    class Meta:
        verbose_name = "Sistema afectado"
        verbose_name_plural = "Sistemas afectados"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class TipoFalla(models.Model):
    descripcion = models.CharField(max_length=200, unique=True, verbose_name="Descripción")
    sistema_afectado = models.ForeignKey(
        SistemaAfectado, on_delete=models.RESTRICT, verbose_name="Sistema afectado")
    estatus_activo = models.BooleanField(default=True, verbose_name="Estatus activo")

    class Meta:
        verbose_name = "Tipo de falla"
        verbose_name_plural = "Tipos de falla"
        ordering = ["descripcion"]

    def __str__(self):
        return self.descripcion
