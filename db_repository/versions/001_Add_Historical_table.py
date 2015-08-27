from sqlalchemy import *
from migrate import *

meta = MetaData()

historical = Table(
    'historical', meta,
    Column('id', Integer, primary_key=True),
    Column('segment', Integer, nullable=False),
    Column('data', Integer, nullable=False),
    Column('timestamp', DateTime, nullable=False))


def upgrade(migrate_engine):
    # Upgrade operations go here.
    meta.bind = migrate_engine
    historical.create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    meta.bind = migrate_engine
    historical.drop()
