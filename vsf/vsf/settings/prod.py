import environ
import dj_database_url

from .base import *

env = environ.Env()

DEBUG = env.bool("DEBUG", False)

SECRET_KEY = env("SECRET_KEY")

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")

DATABASES = {
    "default": dj_database_url.config(default='DATABASE_URL'),
}