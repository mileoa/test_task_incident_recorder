from core.settings.base import *

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}
ALLOWED_HOSTS = ["*"]
SECRET_KEY = "test"
