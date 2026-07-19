from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.models import Q

from vehiculos.api import _make_qr_data_uri
from vehiculos.models import Vehiculo


class Command(BaseCommand):
    help = "Genera códigos QR para vehículos que no tienen uno"

    def handle(self, *args, **options):
        qs = Vehiculo.objects.filter(Q(codigo_qr="") | Q(codigo_qr__isnull=True))
        count = qs.count()
        if count == 0:
            self.stdout.write(self.style.SUCCESS("No hay vehículos sin código QR"))
            return

        for v in qs:
            url = f"{settings.SITE_URL}/vehiculos/{v.id}"
            v.codigo_qr = _make_qr_data_uri(url)
            v.save(update_fields=["codigo_qr"])

        self.stdout.write(self.style.SUCCESS(f"QR generados para {count} vehículos"))
