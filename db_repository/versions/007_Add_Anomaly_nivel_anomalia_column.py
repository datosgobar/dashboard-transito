from sqlalchemy import *
from migrate import *
from migrate.changeset import *


def upgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)
    anomaly = Table('anomaly', meta, autoload=True)
    nivel_anomalia = Column('nivel_anomalia', Integer)
    nivel_anomalia.create(anomaly)


def downgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)
    anomaly = Table('anomaly', meta, autoload=True)
    anomaly.c.nivel_anomalia.drop()
