from sqlalchemy import *
from migrate import *
from migrate.changeset import *
from migrate.changeset.constraint import ForeignKeyConstraint


def upgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)
    segment_snapshot = Table('segment_snapshot', meta, autoload=True)
    corredores = Table('corredores', meta, autoload=True)
    cons = ForeignKeyConstraint([segment_snapshot.c.id], [corredores.c.id])
    cons.create()

def downgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)
    corredores = Table('corredores', meta, autoload=True)
    segment_snapshot = Table('segment_snapshot', meta, autoload=True)
    cons = ForeignKeyConstraint([segment_snapshot.c.id], [corredores.c.id])
    cons.drop()
