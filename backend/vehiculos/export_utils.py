import csv

from django.db.models import Q
from django.http import HttpResponse, StreamingHttpResponse
from openpyxl import Workbook

from .models import Vehiculo

CSV_HEADERS = [
    "N° Económico",
    "N° Unidad",
    "Placa",
    "Color Placa",
    "VIN",
    "Serial Motor",
    "Marca",
    "Modelo",
    "Año",
    "Estado",
    "Gerencia",
    "Emplazamiento",
    "Estatus",
    "Clase",
    "Tipo Combustible",
]

VALUE_FIELDS = [
    "numero_economico",
    "numero_unidad",
    "placa",
    "color_placa__nombre",
    "vin",
    "serial_motor",
    "marca__nombre",
    "modelo__nombre",
    "anio",
    "estado__nombre",
    "gerencia__nombre",
    "emplazamiento__nombre",
    "estatus__nombre",
    "clase__nombre",
    "tipo_combustible__nombre",
]


def build_export_qs(request, search, estado_id, estatus_id, gerencia_id, incluir_inactivos=False):
    qs = Vehiculo.objects.all()
    if request.auth.estado_id:
        qs = qs.filter(estado_id=request.auth.estado_id)
    if not incluir_inactivos:
        qs = qs.filter(estatus_activo=True)
    if search:
        qs = qs.filter(
            Q(numero_economico__icontains=search)
            | Q(vin__icontains=search)
            | Q(placa__icontains=search)
            | Q(placa_intt__icontains=search)
            | Q(serial_motor__icontains=search)
            | Q(numero_unidad__icontains=search)
        )
    if estado_id:
        qs = qs.filter(estado_id=estado_id)
    if estatus_id:
        qs = qs.filter(estatus_id=estatus_id)
    if gerencia_id:
        qs = qs.filter(gerencia_id=gerencia_id)
    return qs.values(*VALUE_FIELDS)


class _Echo:
    def write(self, value):
        return value


def csv_response(qs, filename):
    pseudo = _Echo()
    writer = csv.writer(pseudo)

    def generate():
        yield "\ufeff"
        yield writer.writerow(CSV_HEADERS)
        for row in qs.iterator():
            yield writer.writerow([str(row.get(f, "") or "") for f in VALUE_FIELDS])

    response = StreamingHttpResponse(generate(), content_type="text/csv; charset=utf-8")
    response["Content-Disposition"] = f'attachment; filename="{filename}.csv"'
    return response


def xlsx_response(qs, filename):
    wb = Workbook()
    ws = wb.active
    ws.title = "Vehículos"
    ws.append(CSV_HEADERS)
    for row in qs.iterator():
        ws.append([row.get(f, "") or "" for f in VALUE_FIELDS])

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = f'attachment; filename="{filename}.xlsx"'
    wb.save(response)
    return response
