from datetime import timedelta
from pathlib import Path

from decouple import Csv, config
from django.urls import reverse_lazy

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config(
    "SECRET_KEY", default="django-insecure-dev-key-change-in-production")
DEBUG = config("DEBUG", default=True, cast=bool)
ALLOWED_HOSTS = config(
    "ALLOWED_HOSTS", default="localhost,127.0.0.1", cast=Csv())

INSTALLED_APPS = [
    "unfold",
    "dashboard",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "ninja",
    "ninja_jwt",
    "organizacion",
    "usuarios",
    "catalogos",
]

AUTH_USER_MODEL = "usuarios.Usuario"

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

DATABASE_URL = config("DATABASE_URL", default=None)

if DATABASE_URL:
    import dj_database_url

    DATABASES = {"default": dj_database_url.parse(DATABASE_URL)}
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "es-ES"
TIME_ZONE = "America/Caracas"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "static"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CORS_ALLOWED_ORIGINS = config(
    "CORS_ALLOWED_ORIGINS", default="http://localhost:5173", cast=Csv())
CORS_ALLOW_CREDENTIALS = True

NINJA_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "AUTH_HEADER_TYPES": ("Bearer",),
}

UNFOLD = {
    "DASHBOARD_CALLBACK": "dashboard.callbacks.dashboard_callback",
    "SIDEBAR": {
        "show_search": True,
        "navigation": [
            {
                "title": "Flota",
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": "Dashboard",
                        "icon": "dashboard",
                        "link": reverse_lazy("admin:index"),
                    },
                    {
                        "title": "Usuarios",
                        "icon": "people",
                        "link": reverse_lazy("admin:usuarios_usuario_changelist"),
                    },
                    {
                        "title": "Estados",
                        "icon": "location_on",
                        "link": reverse_lazy("admin:organizacion_estado_changelist"),
                    },
                    {
                        "title": "Gerencias",
                        "icon": "business",
                        "link": reverse_lazy("admin:organizacion_gerencia_changelist"),
                    },
                ],
            },
            {
                "title": "Catálogos",
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": "Marcas",
                        "icon": "local_offer",
                        "link": reverse_lazy("admin:catalogos_marca_changelist"),
                    },
                    {
                        "title": "Modelos",
                        "icon": "model_training",
                        "link": reverse_lazy("admin:catalogos_modelo_changelist"),
                    },
                    {
                        "title": "Tipos de Vehículo",
                        "icon": "directions_car",
                        "link": reverse_lazy("admin:catalogos_tipovehiculo_changelist"),
                    },
                    {
                        "title": "Tipos de Uso",
                        "icon": "work_history",
                        "link": reverse_lazy("admin:catalogos_tipouso_changelist"),
                    },
                    {
                        "title": "Colores",
                        "icon": "palette",
                        "link": reverse_lazy("admin:catalogos_color_changelist"),
                    },
                    {
                        "title": "Sistemas Afectados",
                        "icon": "build",
                        "link": reverse_lazy("admin:catalogos_sistemaafectado_changelist"),
                    },
                    {
                        "title": "Tipos de Falla",
                        "icon": "report_problem",
                        "link": reverse_lazy("admin:catalogos_tipofalla_changelist"),
                    },
                ],
            },
        ],
    },
}
