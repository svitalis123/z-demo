import os
import dj_database_url
from .base import *  # noqa: F401,F403

DEBUG = False

ALLOWED_HOSTS = os.environ.get(
    'ALLOWED_HOSTS', ''
).split(',')

DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600,
    ),
}

SECURE_PROXY_SSL_HEADER = (
    'HTTP_X_FORWARDED_PROTO', 'https'
)
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True