from sqlalchemy import *
from migrate import *

meta = MetaData()

segment_snapshot = Table(
    'segment_snapshot', meta,
    Column('id', Integer, primary_key=True),
    Column('timestamp_medicion', DateTime, nullable=False),
    Column('tiempo', Integer, nullable=False),
    Column('velocidad', Float, nullable=False),
    Column('comentario_causa', String(140), nullable=False),
    Column('causa_id', Integer, nullable=False),
    Column('duracion_anomalia', Integer, nullable=False),
    Column('indicador_anomalia', Float, nullable=False),
    Column('anomalia', Integer, nullable=False))


def upgrade(migrate_engine):
    # Upgrade operations go here.
    meta.bind = migrate_engine
    segment_snapshot.create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    meta.bind = migrate_engine
    segment_snapshot.drop()
