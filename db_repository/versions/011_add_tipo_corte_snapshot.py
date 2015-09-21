from sqlalchemy import *
from migrate import *
from migrate.changeset import *


def upgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)
    segment_snapshot = Table('segment_snapshot', meta, autoload=True)
    tipo_corte = Column('tipo_corte', Integer)
    tipo_corte.create(segment_snapshot)


def downgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)
    segment_snapshot = Table('segment_snapshot', meta, autoload=True)
    segment_snapshot.c.tipo_corte.drop()
