import json

from django.db.models import Count

from organizacion.models import Estado, Gerencia
from usuarios.models import Usuario


def dashboard_callback(request, context):
    total_usuarios = Usuario.objects.count()
    usuarios_activos = Usuario.objects.filter(is_active=True).count()
    total_estados = Estado.objects.filter(estatus_activo=True).count()
    total_gerencias = Gerencia.objects.filter(estatus_activo=True).count()

    context["total_usuarios"] = total_usuarios
    context["usuarios_activos"] = usuarios_activos
    context["total_estados"] = total_estados
    context["total_gerencias"] = total_gerencias

    rol_data = (
        Usuario.objects
        .values("rol")
        .annotate(count=Count("id"))
        .order_by("rol")
    )
    rol_labels = dict(Usuario.Rol.choices)

    context["rol_chart_data"] = json.dumps({
        "labels": [rol_labels.get(item["rol"], item["rol"]) for item in rol_data],
        "datasets": [{
            "label": "Usuarios",
            "data": [item["count"] for item in rol_data],
            "maxBarThickness": 80,
        }],
    })
    estado_data = (
        Usuario.objects
        .filter(estado__isnull=False)
        .values("estado__nombre")
        .annotate(count=Count("id"))
        .order_by("-count")
    )
    context["estado_chart_data"] = json.dumps({
        "labels": [item["estado__nombre"] for item in estado_data],
        "datasets": [{
            "label": "Usuarios",
            "data": [item["count"] for item in estado_data],
            "maxBarThickness": 80,
        }],
    })

    recent_users = Usuario.objects.select_related(
        "estado").order_by("-date_joined")[:5]
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

    return context
