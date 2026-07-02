from django.db import migrations


MARCAS = [
    "Toyota",
    "Ford",
    "Chevrolet",
    "Nissan",
    "Volkswagen",
    "Mitsubishi",
    "Hyundai",
    "Kia",
    "Renault",
    "Fiat",
    "Mercedes-Benz",
    "Freightliner",
    "Kenworth",
    "International",
    "Caterpillar",
]

MODELOS = {
    "Toyota": ["Hilux", "Corolla", "Tacoma", "Land Cruiser", "Fortuner"],
    "Ford": ["Ranger", "Explorer", "Transit", "F-150", "Escape"],
    "Chevrolet": ["Silverado", "Avalanche", "Tahoe", "Captiva", "S10"],
    "Nissan": ["Frontier", "NP300", "Sentra", "Versa", "Pathfinder"],
    "Volkswagen": ["Amarok", "Jetta", "T-Cross", "Taos", "Vento"],
    "Mitsubishi": ["L200", "Montero", "Outlander", "ASX", "Mirage"],
    "Hyundai": ["Tucson", "Santa Fe", "Creta", "Elantra", "H100"],
    "Kia": ["Sportage", "Sorento", "Rio", "Cerato", "Seltos"],
    "Renault": ["Duster", "Sandero", "Koleos", "Logan", "Stepway"],
    "Fiat": ["Strada", "Fiorino", "Ducato", "Mobi", "Pulse"],
    "Mercedes-Benz": ["Sprinter", "Actros", "Atego", "Citan", "Vito"],
    "Freightliner": ["Cascadia", "M2", "Coronado", "114SD", "eCascadia"],
    "Kenworth": ["T680", "T880", "W990", "K270", "C500"],
    "International": ["CV515", "LT625", "MV607", "HV513", "LoneStar"],
    "Caterpillar": ["D6", "950", "320", "730", "C15"],
}

TIPOS_VEHICULO = [
    "Sedan",
    "SUV",
    "Pickup",
    "Camión Cesta",
    "Camión Plataforma",
    "Montacargas",
    "Furgoneta",
    "Grúa",
    "Compacto",
    "Autobús",
    "Tractocamión",
    "Cuatrimoto",
]

TIPOS_USO = [
    "24 horas",
    "8 horas Administrativo",
    "Mixto",
    "Standby / Reserva",
    "Operativo Especial",
]

COLORES = [
    "Blanco",
    "Rojo",
    "Azul",
    "Gris",
    "Negro",
    "Verde",
    "Plateado",
    "Beige",
    "Naranja",
    "Amarillo",
]

TIPOS_FALLA = [
    ("Fuga de aceite de motor", "Motor"),
    ("Pastillas de freno gastadas", "Frenos"),
    ("Batería descargada o en mal estado", "Eléctrico"),
    ("Fuga en sistema hidráulico", "Hidráulico"),
    ("Transmisión no engrana correctamente", "Transmisión"),
    ("Suspensión delantera con desgaste", "Suspensión"),
    ("Dirección dura o con juego excesivo", "Dirección"),
    ("Golpe o abolladura en carrocería", "Carrocería"),
    ("Sobrecalentamiento del motor", "Motor"),
    ("Fallas en sistema de climatización", "Eléctrico"),
    ("Fugas en mangueras del radiador", "Motor"),
    ("Correa de distribución desgastada", "Motor"),
    ("Luces delanteras fundidas o rotas", "Eléctrico"),
    ("Frenos de aire con pérdida de presión", "Frenos"),
    ("Neumáticos con desgaste irregular o cortes", "Suspensión"),
]


def seed_catalogos(apps, schema_editor):
    Marca = apps.get_model("catalogos", "Marca")
    Modelo = apps.get_model("catalogos", "Modelo")
    TipoVehiculo = apps.get_model("catalogos", "TipoVehiculo")
    TipoUso = apps.get_model("catalogos", "TipoUso")
    Color = apps.get_model("catalogos", "Color")
    TipoFalla = apps.get_model("catalogos", "TipoFalla")

    for nombre in MARCAS:
        Marca.objects.get_or_create(nombre=nombre, defaults={"estatus_activo": True})

    for marca_nombre, modelos in MODELOS.items():
        marca = Marca.objects.get(nombre=marca_nombre)
        for modelo_nombre in modelos:
            Modelo.objects.get_or_create(
                nombre=modelo_nombre, marca=marca, defaults={"estatus_activo": True}
            )

    for nombre in TIPOS_VEHICULO:
        TipoVehiculo.objects.get_or_create(nombre=nombre, defaults={"estatus_activo": True})

    for nombre in TIPOS_USO:
        TipoUso.objects.get_or_create(nombre=nombre, defaults={"estatus_activo": True})

    for nombre in COLORES:
        Color.objects.get_or_create(nombre=nombre, defaults={"estatus_activo": True})

    for descripcion, sistema in TIPOS_FALLA:
        TipoFalla.objects.get_or_create(
            descripcion=descripcion,
            defaults={"sistema_afectado": sistema, "estatus_activo": True},
        )


def reverse_seed_catalogos(apps, schema_editor):
    Modelo = apps.get_model("catalogos", "Modelo")
    Modelo.objects.all().delete()
    for model_class in ["Marca", "TipoVehiculo", "TipoUso", "Color", "TipoFalla"]:
        apps.get_model("catalogos", model_class).objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("catalogos", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_catalogos, reverse_seed_catalogos),
    ]
