from sqlalchemy import *
from migrate import *
from migrate.changeset import *


def upgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)
    segment_snapshot = Table('segment_snapshot', meta, autoload=True)
    #anomaly = Table('anomaly', meta, autoload=True)
    anomalia_id = Column('anomalia_id', Integer)
    anomalia_id.create(segment_snapshot)


def downgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)
    segment_snapshot = Table('segment_snapshot', meta, autoload=True)
    segment_snapshot.c.anomalia_id.drop()
