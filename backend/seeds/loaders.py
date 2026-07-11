import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


def _load_json(app_name):
    path = BASE_DIR / app_name / "data.json"
    if not path.exists():
        return {}
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def load_estados(estado_cls, *, incluir_inactivos=False):
    data = _load_json("organizacion")
    nombres = data.get("estados", [])
    csv = set()
    for nombre in nombres:
        csv.add(nombre)
        estado_cls.objects.update_or_create(
            nombre__iexact=nombre,
            defaults={"nombre": nombre, "estatus_activo": True},
        )
    if not incluir_inactivos:
        estado_cls.objects.filter(estatus_activo=True).exclude(nombre__in=csv).update(
            estatus_activo=False
        )


def load_gerencias(gerencia_cls, *, incluir_inactivos=False):
    data = _load_json("organizacion")
    nombres = data.get("gerencias", [])
    csv = set()
    for nombre in nombres:
        csv.add(nombre)
        gerencia_cls.objects.update_or_create(
            nombre__iexact=nombre,
            defaults={"nombre": nombre, "estatus_activo": True},
        )
    if not incluir_inactivos:
        gerencia_cls.objects.filter(estatus_activo=True).exclude(nombre__in=csv).update(
            estatus_activo=False
        )


def load_centros(centro_cls, estado_cls, *, incluir_inactivos=False):
    data = _load_json("organizacion")
    centros = data.get("centros", [])
    estado_cache = {e.nombre.lower(): e for e in estado_cls.objects.filter(estatus_activo=True)}
    csv = set()
    for item in centros:
        estado = estado_cache.get(item["estado"].lower())
        if not estado:
            continue
        csv.add(item["nombre"])
        centro_cls.objects.update_or_create(
            nombre__iexact=item["nombre"],
            defaults={"nombre": item["nombre"], "estado": estado, "estatus_activo": True},
        )
    if not incluir_inactivos:
        centro_cls.objects.filter(estatus_activo=True).exclude(nombre__in=csv).update(
            estatus_activo=False
        )


def load_marcas_modelos(marca_cls, modelo_cls, *, incluir_inactivos=False):
    data = _load_json("catalogos")
    marcas_csv = set()
    marca_cache = {}

    for nombre in data.get("marcas", []):
        marcas_csv.add(nombre)
        marca, _ = marca_cls.objects.update_or_create(
            nombre__iexact=nombre,
            defaults={"nombre": nombre, "estatus_activo": True},
        )
        marca_cache[nombre.lower()] = marca

    if not incluir_inactivos:
        marca_cls.objects.filter(estatus_activo=True).exclude(nombre__in=marcas_csv).update(
            estatus_activo=False
        )

    modelos_csv = set()
    for entry in data.get("modelos", []):
        marca = marca_cache.get(entry["marca"].lower())
        if not marca:
            continue
        for nombre in entry["nombres"]:
            modelos_csv.add(nombre)
            modelo_cls.objects.update_or_create(
                nombre__iexact=nombre,
                marca=marca,
                defaults={"nombre": nombre, "marca": marca, "estatus_activo": True},
            )

    if not incluir_inactivos:
        for m in modelo_cls.objects.filter(estatus_activo=True).exclude(nombre__in=modelos_csv):
            m.estatus_activo = False
            m.save()


def load_colores(color_cls, *, incluir_inactivos=False):
    data = _load_json("catalogos")
    nombres = data.get("colores", [])
    existing = {
        c.lower()
        for c in color_cls.objects.filter(estatus_activo=True).values_list("nombre", flat=True)
    }
    for nombre in nombres:
        if nombre.lower() not in existing:
            color_cls.objects.create(nombre=nombre)


def load_estatus_vehiculo(estatus_cls, *, incluir_inactivos=False):
    data = _load_json("catalogos")
    nombres = data.get("estatus_vehiculo", [])
    csv = set()
    for nombre in nombres:
        csv.add(nombre)
        estatus_cls.objects.update_or_create(
            nombre__iexact=nombre,
            defaults={"nombre": nombre, "estatus_activo": True},
        )
    if not incluir_inactivos:
        estatus_cls.objects.filter(estatus_activo=True).exclude(nombre__in=csv).update(
            estatus_activo=False
        )


def load_colores_placa(color_placa_cls, *, incluir_inactivos=False):
    data = _load_json("catalogos")
    nombres = data.get("colores_placa", [])
    csv = set()
    for nombre in nombres:
        csv.add(nombre)
        color_placa_cls.objects.update_or_create(
            nombre__iexact=nombre,
            defaults={"nombre": nombre, "estatus_activo": True},
        )
    if not incluir_inactivos:
        color_placa_cls.objects.filter(estatus_activo=True).exclude(nombre__in=csv).update(
            estatus_activo=False
        )


def load_tipos_vehiculo(tipo_vehiculo_cls, *, incluir_inactivos=False):
    data = _load_json("catalogos")
    nombres = data.get("tipos_vehiculo", [])
    csv = set()
    for nombre in nombres:
        csv.add(nombre)
        tipo_vehiculo_cls.objects.update_or_create(
            nombre__iexact=nombre,
            defaults={"nombre": nombre, "estatus_activo": True},
        )
    if not incluir_inactivos:
        tipo_vehiculo_cls.objects.filter(estatus_activo=True).exclude(nombre__in=csv).update(
            estatus_activo=False
        )


def load_tipos_uso(tipo_uso_cls, *, incluir_inactivos=False):
    data = _load_json("catalogos")
    nombres = data.get("tipos_uso", [])
    csv = set()
    for nombre in nombres:
        csv.add(nombre)
        tipo_uso_cls.objects.update_or_create(
            nombre__iexact=nombre,
            defaults={"nombre": nombre, "estatus_activo": True},
        )
    if not incluir_inactivos:
        tipo_uso_cls.objects.filter(estatus_activo=True).exclude(nombre__in=csv).update(
            estatus_activo=False
        )


def load_clases_vehiculo(clase_vehiculo_cls, *, incluir_inactivos=False):
    data = _load_json("catalogos")
    nombres = data.get("clases_vehiculo", [])
    csv = set()
    for nombre in nombres:
        csv.add(nombre)
        clase_vehiculo_cls.objects.update_or_create(
            nombre__iexact=nombre,
            defaults={"nombre": nombre, "estatus_activo": True},
        )
    if not incluir_inactivos:
        clase_vehiculo_cls.objects.filter(estatus_activo=True).exclude(nombre__in=csv).update(
            estatus_activo=False
        )


def load_tipos_combustible(tipo_combustible_cls, *, incluir_inactivos=False):
    data = _load_json("catalogos")
    nombres = data.get("tipos_combustible", [])
    csv = set()
    for nombre in nombres:
        csv.add(nombre)
        tipo_combustible_cls.objects.update_or_create(
            nombre__iexact=nombre,
            defaults={"nombre": nombre, "estatus_activo": True},
        )
    if not incluir_inactivos:
        tipo_combustible_cls.objects.filter(estatus_activo=True).exclude(nombre__in=csv).update(
            estatus_activo=False
        )


def load_sistemas_fallas(sistema_cls, falla_cls, *, incluir_inactivos=False):
    data = _load_json("catalogos")
    sistemas_csv = set()
    sa_cache = {}

    for nombre in data.get("sistemas_afectados", []):
        sistemas_csv.add(nombre)
        sa, _ = sistema_cls.objects.update_or_create(
            nombre__iexact=nombre,
            defaults={"nombre": nombre, "estatus_activo": True},
        )
        sa_cache[nombre.lower()] = sa

    if not incluir_inactivos:
        sistema_cls.objects.filter(estatus_activo=True).exclude(nombre__in=sistemas_csv).update(
            estatus_activo=False
        )

    fallas_csv = set()
    for entry in data.get("tipos_falla", []):
        sa = sa_cache.get(entry["sistema"].lower())
        if not sa:
            continue
        fallas_csv.add(entry["descripcion"])
        falla_cls.objects.update_or_create(
            descripcion__iexact=entry["descripcion"],
            defaults={
                "descripcion": entry["descripcion"],
                "sistema_afectado": sa,
                "estatus_activo": True,
            },
        )

    if not incluir_inactivos:
        falla_cls.objects.filter(estatus_activo=True).exclude(descripcion__in=fallas_csv).update(
            estatus_activo=False
        )


def load_usuarios(usuario_cls, *, incluir_inactivos=False):
    from django.contrib.auth.hashers import make_password

    data = _load_json("usuarios")
    for entry in data.get("usuarios", []):
        defaults = {
            "password": make_password(entry["password"]),
            "email": entry.get("email", ""),
            "first_name": entry.get("first_name", ""),
            "last_name": entry.get("last_name", ""),
            "rol": entry["rol"],
            "is_staff": entry.get("is_staff", False),
            "is_superuser": entry.get("is_superuser", False),
            "estado_id": entry.get("estado_id"),
        }
        usuario_cls.objects.update_or_create(
            username=entry["username"],
            defaults=defaults,
        )
