from sqlalchemy import *
from migrate import *

meta = MetaData()

anomaly = Table(
    'anomaly', meta,
    Column('id', Integer, primary_key=True),
    Column('id_segment', Integer, nullable=False),
    Column('timestamp_start', DateTime, nullable=False),
    Column('timestamp_end', DateTime, nullable=False),
    Column('comentario_causa', String(140), nullable=False),
    Column('causa_id', Integer, nullable=False),
    Column('indicador_anomalia', Float, nullable=False))


col = Column('nivel_anomalia', Integer, nullable=False)


def upgrade(migrate_engine):
    # Upgrade operations go here.
    meta.bind = migrate_engine
    col.create(anomaly, populate_default=True)


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    meta.bind = migrate_engine
    anomaly.drop(anomaly)
