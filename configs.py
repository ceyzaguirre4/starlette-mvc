from starlette.config import Config
from starlette.datastructures import URL, Secret

# Config will be read from environment variables and/or ".env" files.
_config = Config(".env")

DEBUG = _config('DEBUG', cast=bool, default=False)
TESTING = _config('TESTING', cast=bool, default=False)
SECRET_KEY = _config('SECRET_KEY', cast=Secret)         # casting as secret to minimize exposing its value in tracebacks, etc.
DATABASE_URL = _config('DATABASE_URL')
