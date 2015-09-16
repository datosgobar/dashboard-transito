from sqlalchemy import *
from migrate import *
from migrate.changeset import *


def upgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)
    anomaly = Table('anomaly', meta, Column("tipo_corte", String), extend_existing=True)
    anomaly.c.tipo_corte.alter(type=Integer)

def downgrade(migrate_engine):
    meta=MetaData(bind=migrate_engine)
    anomaly=Table('anomaly', meta, Column(
        "tipo_corte", Integer), extend_existing=True)
    anomaly.c.tipo_corte.alter(type=String(210))
