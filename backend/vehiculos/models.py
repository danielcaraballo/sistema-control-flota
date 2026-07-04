from django.db import models


class Vehiculo(models.Model):
    numero_economico = models.CharField(
        max_length=50, unique=True, verbose_name="Número económico (Activo SAP)")
    gerencia = models.ForeignKey(
        "organizacion.Gerencia", on_delete=models.RESTRICT, verbose_name="Gerencia")
    categoria = models.ForeignKey(
        "catalogos.TipoVehiculo", on_delete=models.RESTRICT, verbose_name="Categoría")
    marca = models.ForeignKey(
        "catalogos.Marca", on_delete=models.RESTRICT, verbose_name="Marca")
    modelo = models.ForeignKey(
        "catalogos.Modelo", on_delete=models.RESTRICT, verbose_name="Modelo")
    anio = models.IntegerField(verbose_name="Año")
    vin = models.CharField(
        max_length=17, unique=True, verbose_name="VIN / Serial de chasis")
    estado = models.ForeignKey(
        "organizacion.Estado", on_delete=models.RESTRICT, verbose_name="Estado")
    emplazamiento = models.ForeignKey(
        "organizacion.CentroDeServicio", on_delete=models.RESTRICT, verbose_name="Emplazamiento")
    estatus = models.ForeignKey(
        "catalogos.EstatusVehiculo", on_delete=models.RESTRICT, verbose_name="Estatus")
    placa = models.CharField(max_length=20, verbose_name="Placa")
    color = models.ForeignKey(
        "catalogos.Color", on_delete=models.RESTRICT, verbose_name="Color")
    codigo_qr = models.TextField(
        blank=True, verbose_name="Código QR")
    estatus_activo = models.BooleanField(
        default=True, verbose_name="Estatus activo")

    class Meta:
        verbose_name = "Vehículo"
        verbose_name_plural = "Vehículos"
        ordering = ["numero_economico"]

    def __str__(self):
        return f"{self.numero_economico} - {self.marca} {self.modelo}"
