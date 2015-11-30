from sqlalchemy import *
from migrate import *
from migrate.changeset import *


def upgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)
    estadisticas = Table('estadisticas', meta, autoload=True)
    tipo_grafico = Column('tipo_grafico', String(240))
    tipo_grafico.create(estadisticas)


def downgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)
    estadisticas = Table('estadisticas', meta, autoload=True)
    estadisticas.c.tipo_grafico.drop()