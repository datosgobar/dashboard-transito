from sqlalchemy import *
from migrate import *
from migrate.changeset import *


def upgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)
    anomaly = Table('anomaly', meta, autoload=True)
    timestamp_asignacion = Column('timestamp_asignacion', DateTime)
    timestamp_asignacion.create(anomaly)


def downgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)
    anomaly = Table('anomaly', meta, autoload=True)
    anomaly.c.timestamp_asignacion.drop()
