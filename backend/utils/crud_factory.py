from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from ninja import Router
from ninja.errors import HttpError
from ninja_jwt.authentication import JWTAuth

from usuarios.models import Usuario
from usuarios.roles import requiere_rol_minimo
from utils.api_helpers import check_duplicate, filter_activos, get_object_or_404


@dataclass
class CrudConfig:
    prefix: str
    model: type
    read_schema: type
    create_schema: type
    update_schema: type
    display_name: str
    article: str = "un"
    unique_field: str = "nombre"
    unique_field_label: str | None = None
    rol_list: str = Usuario.Rol.MECANICO
    rol_mutate: str = Usuario.Rol.NACIONAL
    select_related: list[str] | None = None
    response_builder: Callable | None = None
    fk_validations: list[dict] = field(default_factory=list)


def register_crud(router: Router, cfg: CrudConfig) -> None:
    label = cfg.unique_field_label or cfg.unique_field
    g = cfg.article
    dn = cfg.display_name

    tag = cfg.prefix.replace("-", "_")

    # ── LIST ────────────────────────────────────────────────────────────
    @router.get(f"/{cfg.prefix}/", response=list[cfg.read_schema], auth=JWTAuth())
    @requiere_rol_minimo(cfg.rol_list)
    def view(request):
        qs = cfg.model.objects.all()
        if cfg.select_related:
            qs = qs.select_related(*cfg.select_related)
        qs = filter_activos(qs, request)
        if cfg.response_builder:
            return [cfg.response_builder(obj) for obj in qs]
        return qs

    view.__name__ = f"list_{tag}"

    # ── GET ─────────────────────────────────────────────────────────────
    @router.get(f"/{cfg.prefix}/{{entity_id}}", response=cfg.read_schema, auth=JWTAuth())
    @requiere_rol_minimo(cfg.rol_list)
    def view(request, entity_id: int):
        qs = (
            cfg.model.objects
            if not cfg.select_related
            else cfg.model.objects.select_related(*cfg.select_related)
        )
        obj = get_object_or_404(qs, entity_id)
        if cfg.response_builder:
            return cfg.response_builder(obj)
        return obj

    view.__name__ = f"get_{tag}"

    # ── CREATE ──────────────────────────────────────────────────────────
    @router.post(f"/{cfg.prefix}/", response=cfg.read_schema, auth=JWTAuth())
    @requiere_rol_minimo(cfg.rol_mutate)
    def view(request, data: cfg.create_schema):
        payload = data.dict()

        for v in cfg.fk_validations:
            fk_value = payload.get(v["field"])
            if fk_value is not None:
                if not v["model"].objects.filter(id=fk_value, estatus_activo=True).exists():
                    raise HttpError(400, v["error_msg"])

        val = payload.get(cfg.unique_field)
        if val is not None:
            extra = _build_extra_filters(payload, cfg.fk_validations)
            if check_duplicate(cfg.model, cfg.unique_field, val, extra_filters=extra):
                raise HttpError(409, _dup_msg(g, dn, label, extra))

        obj = cfg.model.objects.create(**payload)
        if cfg.select_related and cfg.response_builder:
            full = cfg.model.objects.select_related(*cfg.select_related).get(id=obj.id)
            return cfg.response_builder(full)
        return obj

    view.__name__ = f"create_{tag}"

    # ── UPDATE ──────────────────────────────────────────────────────────
    @router.put(f"/{cfg.prefix}/{{entity_id}}", response=cfg.read_schema, auth=JWTAuth())
    @requiere_rol_minimo(cfg.rol_mutate)
    def view(request, entity_id: int, data: cfg.update_schema):
        obj = get_object_or_404(cfg.model, entity_id)
        payload = data.dict(exclude_unset=True)

        for v in cfg.fk_validations:
            fk_value = payload.get(v["field"])
            if fk_value is not None and fk_value != getattr(obj, v["field"]):
                if not v["model"].objects.filter(id=fk_value, estatus_activo=True).exists():
                    raise HttpError(400, v["error_msg"])

        val = payload.get(cfg.unique_field)
        if val is not None and val != getattr(obj, cfg.unique_field):
            extra = _build_extra_filters(payload, cfg.fk_validations, obj)
            if check_duplicate(
                cfg.model, cfg.unique_field, val, exclude_id=entity_id, extra_filters=extra
            ):
                raise HttpError(409, _dup_msg(g, dn, label, extra))

        for attr, value in payload.items():
            setattr(obj, attr, value)
        obj.save()

        if cfg.select_related and cfg.response_builder:
            full = cfg.model.objects.select_related(*cfg.select_related).get(id=entity_id)
            return cfg.response_builder(full)
        return obj

    view.__name__ = f"update_{tag}"

    # ── DEACTIVATE ──────────────────────────────────────────────────────
    @router.delete(f"/{cfg.prefix}/{{entity_id}}", response={204: None}, auth=JWTAuth())
    @requiere_rol_minimo(cfg.rol_mutate)
    def view(request, entity_id: int):
        obj = get_object_or_404(cfg.model, entity_id)
        obj.estatus_activo = False
        obj.save()
        return 204, None

    view.__name__ = f"deactivate_{tag}"


def _build_extra_filters(
    payload: dict, fk_validations: list[dict], obj: Any | None = None
) -> dict | None:
    extra = {}
    for v in fk_validations:
        fk_val = payload.get(v["field"])
        if fk_val is None and obj is not None:
            fk_val = getattr(obj, v["field"], None)
        if fk_val is not None:
            extra[v["field"]] = fk_val
    return extra or None


def _dup_msg(g: str, dn: str, label: str, extra: dict | None) -> str:
    adj = "a" if g == "una" else "o"
    msg = f"Ya existe {g} {dn} activ{adj} con ese {label}"
    if g == "una" and extra:
        pass
    return msg
