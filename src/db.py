import databases
import sqlalchemy
from geoalchemy2 import Geometry
from sqlalchemy import Table, Column, Integer, String, JSON

import config

metadata = sqlalchemy.MetaData()

gis_polygon = Table(
    'gis_polygon',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('class_id', String),
    Column('props', JSON),
    Column('geometry', Geometry('POLYGON'))
)

DATABASE_URL = (f'postgresql://{config.POSTGRES_USER}:'
                f'{config.POSTGRES_PASSWORD}@'
                f'{config.POSTGRES_HOST}:'
                f'{config.POSTGRES_PORT}/'
                f'{config.POSTGRES_DB}')

database = databases.Database(DATABASE_URL)
engine = sqlalchemy.create_engine(DATABASE_URL)
metadata.create_all(engine)
