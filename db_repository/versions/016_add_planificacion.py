from sqlalchemy import *
from migrate import *

meta = MetaData()

estadisticas = Table(
    'estadisticas', meta,
    Column('id', String(240), primary_key=True),
    Column('name', String(240), nullable=False),
    Column('filename', String(240), nullable=False),
    Column('timestamp_start', DateTime, nullable=False),
    Column('timestamp_end', DateTime, nullable=False)
)


def upgrade(migrate_engine):
    # Upgrade operations go here.
    meta.bind = migrate_engine
    estadisticas.create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    meta.bind = migrate_engine
    estadisticas.drop()