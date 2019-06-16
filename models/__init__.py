import databases
import sqlalchemy
from sqlalchemy_utils import database_exists, create_database, drop_database
from sqlalchemy import create_engine

from starlette.applications import Starlette
from starlette.config import Config
from starlette.responses import JSONResponse

from .users import *
import configs

metadata = sqlalchemy.MetaData()

# create tables using metadata
users_table = create_users_table(metadata)


if configs.TESTING:
    drop_database(configs.DATABASE_URL)
    engine = create_engine(configs.DATABASE_URL)
    # if not database_exists(configs.DATABASE_URL):
    create_database(configs.DATABASE_URL)
    metadata.create_all(engine)

database = databases.Database(configs.DATABASE_URL)
