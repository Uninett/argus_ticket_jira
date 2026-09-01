SECRET_KEY = "stuffandnonsense"

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

AUTH_USER_MODEL = "argus_auth.User"

USE_TZ = True
TIME_ZONE = "Europe/Oslo"

INSTALLED_APPS = [
    # overrides others. must come first
    "argus.htmx",
    # Django 1st party apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.postgres",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.forms",
    # 3rd party apps
    "django_tasks",
    "django_tasks_db",
    "corsheaders",
    "social_django",
    "rest_framework",
    "rest_framework.authtoken",
    "drf_spectacular",
    "django_filters",
    "phonenumber_field",
    "knox",  # token auth
    "django_htmx",
    "widget_tweaks",
    "fontawesomefree",
    # Argus apps
    "argus.auth",
    "argus.base",
    "argus.incident",
    "argus.filter",
    "argus.notificationprofile",
    "argus.dev",
    "argus.plannedmaintenance",
    "argus.versioncheck",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "social_django.middleware.SocialAuthExceptionMiddleware",
    "django.contrib.auth.middleware.RemoteUserMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
    "argus.htmx.middleware.LoginRequiredMiddleware",
    "argus.htmx.middleware.HtmxMessageMiddleware",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    },
}

MIDDLEWARE_CLASSES = ()

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "OPTIONS": {
            "debug": True,
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "social_django.context_processors.backends",
                "social_django.context_processors.login_redirect",
                "argus.auth.context_processors.preferences",
                "argus.htmx.context_processors.static_paths",
                "argus.htmx.context_processors.metadata",
                "argus.htmx.context_processors.banner_message",
            ],
        },
    }
]

# Argus specific settings
MEDIA_PLUGINS = [
    "argus.notificationprofile.media.email.EmailNotification",
]
