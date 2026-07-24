import json

from django.db.models import Count

from organizacion.models import Estado, Gerencia
from usuarios.models import Usuario
from vehiculos.models import Vehiculo


def dashboard_callback(request, context):
    total_usuarios = Usuario.objects.count()
    usuarios_activos = Usuario.objects.filter(is_active=True).count()
    total_estados = Estado.objects.filter(estatus_activo=True).count()
    total_gerencias = Gerencia.objects.filter(estatus_activo=True).count()

    total_vehiculos = Vehiculo.objects.count()
    vehiculos_activos = Vehiculo.objects.filter(estatus_activo=True).count()
    pct_operatividad = (
        round(vehiculos_activos / total_vehiculos * 100, 1) if total_vehiculos else 0.0
    )

    context["total_usuarios"] = total_usuarios
    context["usuarios_activos"] = usuarios_activos
    context["total_estados"] = total_estados
    context["total_gerencias"] = total_gerencias
    vehiculos_inactivos = total_vehiculos - vehiculos_activos

    context["total_vehiculos"] = total_vehiculos
    context["vehiculos_activos"] = vehiculos_activos
    context["vehiculos_inactivos"] = vehiculos_inactivos
    context["pct_operatividad"] = pct_operatividad

    # --- User charts ---
    rol_data = Usuario.objects.values("rol").annotate(count=Count("id")).order_by("rol")
    rol_labels = dict(Usuario.Rol.choices)

    context["rol_chart_data"] = json.dumps(
        {
            "labels": [rol_labels.get(item["rol"], item["rol"]) for item in rol_data],
            "datasets": [
                {
                    "label": "Usuarios",
                    "data": [item["count"] for item in rol_data],
                    "maxBarThickness": 80,
                }
            ],
        }
    )
    estado_data = (
        Usuario.objects.filter(estado__isnull=False)
        .values("estado__nombre")
        .annotate(count=Count("id"))
        .order_by("-count")
    )
    context["estado_chart_data"] = json.dumps(
        {
            "labels": [item["estado__nombre"] for item in estado_data],
            "datasets": [
                {
                    "label": "Usuarios",
                    "data": [item["count"] for item in estado_data],
                    "maxBarThickness": 80,
                }
            ],
        }
    )

    # --- Vehicle charts ---
    estatus_data = (
        Vehiculo.objects.values("estatus__nombre").annotate(count=Count("id")).order_by("-count")
    )
    context["vehiculo_estatus_chart"] = json.dumps(
        {
            "labels": [item["estatus__nombre"] for item in estatus_data],
            "datasets": [
                {
                    "label": "Vehículos",
                    "data": [item["count"] for item in estatus_data],
                    "maxBarThickness": 80,
                }
            ],
        }
    )

    flota_estado = (
        Vehiculo.objects.values("estado__nombre").annotate(count=Count("id")).order_by("-count")[:5]
    )
    context["flota_estado_chart"] = json.dumps(
        {
            "labels": [item["estado__nombre"] for item in flota_estado],
            "datasets": [
                {
                    "label": "Vehículos",
                    "data": [item["count"] for item in flota_estado],
                    "maxBarThickness": 80,
                }
            ],
        }
    )

    # --- Tables ---
    recent_users = Usuario.objects.select_related("estado").order_by("-date_joined")[:5]
    context["users_table"] = {
        "headers": ["Usuario", "Email", "Rol", "Estado", "Fecha"],
        "rows": [
            [
                user.username,
                user.email,
                user.get_rol_display(),
                str(user.estado) if user.estado else "-",
                user.date_joined.strftime("%d/%m/%Y"),
            ]
            for user in recent_users
        ],
    }

    vehiculos_recientes = Vehiculo.objects.select_related("estado", "marca", "modelo").order_by(
        "-id"
    )[:5]
    context["vehiculos_table"] = {
        "headers": ["Económico", "Marca / Modelo", "Estado", "Estatus", "Activo"],
        "rows": [
            [
                v.numero_economico,
                f"{v.marca} {v.modelo}",
                str(v.estado),
                str(v.estatus),
                "Sí" if v.estatus_activo else "No",
            ]
            for v in vehiculos_recientes
        ],
    }

    return context
