from ninja.errors import HttpError


def filter_activos(queryset, request):
    incluir_inactivos = request.GET.get("incluir_inactivos") == "true"
    if not incluir_inactivos:
        return queryset.filter(estatus_activo=True)
    return queryset


def get_object_or_404(model_or_qs, id):
    if hasattr(model_or_qs, "_meta"):
        qs = model_or_qs.objects
    else:
        qs = model_or_qs
    model = qs.model if hasattr(qs, "model") else model_or_qs
    try:
        return qs.get(id=id)
    except model.DoesNotExist:
        name = model._meta.verbose_name if hasattr(model, "_meta") else "recurso"
        raise HttpError(404, f"{name} no encontrado")


def check_duplicate(model, field, value, exclude_id=None, extra_filters=None):
    qs = model.objects.filter(estatus_activo=True, **{field: value})
    if exclude_id is not None:
        qs = qs.exclude(id=exclude_id)
    if extra_filters:
        qs = qs.filter(**extra_filters)
    return qs.exists()


def check_duplicate_composite(model, fields: dict, exclude_id=None):
    qs = model.objects.filter(estatus_activo=True, **fields)
    if exclude_id is not None:
        qs = qs.exclude(id=exclude_id)
    return qs.exists()
