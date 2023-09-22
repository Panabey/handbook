"""
Django settings for admin project.

Generated by 'django-admin startproject' using Django 4.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
from pathlib import Path
from core.settings import settings

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = settings.SECRET_APP

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = settings.DEBUG_MODE

# Application PROTECTION

ALLOWED_HOSTS = settings.ALLOWED_HOSTS

CSRF_COOKIE_SECURE = settings.CSRF_COOKIE_SECURE

CSRF_TRUSTED_ORIGINS = settings.CSRF_TRUSTED_ORIGINS

CORS_ALLOWED_ORIGINS = settings.CORS_ALLOWED_ORIGINS

SESSION_COOKIE_SECURE = settings.SESSION_COOKIE_SECURE

# Application definition

INSTALLED_APPS = [
    "whitenoise.runserver_nostatic",
    "panel",
    "mdeditor",
    "colorfield",
    "corsheaders",
    "django_cleanup.apps.CleanupConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "axes",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "axes.middleware.AxesMiddleware",
]

ROOT_URLCONF = "admin.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "admin.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": settings.DATABASE_HOST,
        "NAME": settings.DB_ADMIN_NAME,
        "USER": settings.DB_ADMIN_USER,
        "PASSWORD": settings.DB_ADMIN_PASSWORD,
    },
    "handbook": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": settings.DATABASE_HOST,
        "NAME": settings.DB_BACKEND_NAME,
        "USER": settings.DB_BACKEND_USER,
        "PASSWORD": settings.DB_BACKEND_PASSWORD,
    },
}

DATABASE_ROUTERS = [
    "core.routing_database.BaseRouter",
]

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",  # noqa: E501
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]

# Security
# https://django-axes.readthedocs.io/en/latest/4_configuration.html

AUTHENTICATION_BACKENDS = [
    "axes.backends.AxesStandaloneBackend",
    # Django ModelBackend is the default authentication backend.
    "django.contrib.auth.backends.ModelBackend",
]

AXES_IPWARE_META_PRECEDENCE_ORDER = [
    "HTTP_X_FORWARDED_FOR",
    "REMOTE_ADDR",
]

AXES_FAILURE_LIMIT = 5
AXES_RESET_ON_SUCCESS = True
AXES_ONLY_ADMIN_SITE = True
AXES_DISABLE_ACCESS_LOG = settings.AXES_DISABLE_ACCESS_LOG
AXES_ACCESS_FAILURE_LOG_PER_USER_LIMIT = 50
AXES_HANDLER = "core.axes_handler.AxesCustomHandler"
# custom settings
# если True, то очищает все данные из GET и POST для записи в БД
AXES_CLEAR_DATA = settings.AXES_CLEAR_DATA

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "ru-ru"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"

STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "media/"

MEDIA_ROOT = BASE_DIR / "media"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Markdown v2 editor
# https://github.com/pylixm/django-mdeditor

MDEDITOR_CONFIGS = {
    "default": {
        "emoji": False,
        "language": "en",
        "upload_image_formats": ["jpg", "jpeg", "gif", "png", "bmp", "webp", "svg"],
        "image_folder": "general/",
        "lineWrapping": True,
    }
}
