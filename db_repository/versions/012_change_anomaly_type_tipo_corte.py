from sqlalchemy import *
from migrate import *
from migrate.changeset import *
from sqlalchemy import MetaData, Table, Column, String, Integer


def upgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)
    anomaly = Table('anomaly', meta, autoload=True)
    anomaly.c.tipo_corte.drop()
    tipo_corte = Column('tipo_corte', Integer)
    tipo_corte.create(anomaly)

def downgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)
    anomaly = Table('anomaly', meta, autoload=True)
    anomaly.c.tipo_corte.drop()
    tipo_corte = Column('tipo_corte', String(210))
    tipo_corte.create(anomaly)
