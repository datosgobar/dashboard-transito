from sqlalchemy import *
from migrate import *


def upgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)
    estadisticas = Table('estadisticas', meta, autoload=True)
    tipo_grafico = Column('periodo', String(77), nullable=True)
    tipo_grafico.create(estadisticas)


def downgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)
    estadisticas = Table('estadisticas', meta, autoload=True)
    estadisticas.c.periodo.drop()
