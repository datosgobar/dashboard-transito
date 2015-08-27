from sqlalchemy import *
from migrate import *

meta = MetaData()

causa = Table(
    'causa', meta,
    Column('id', Integer, primary_key=True),
    Column('descripcion', String(140), nullable=False))


def upgrade(migrate_engine):
    # Upgrade operations go here.
    meta.bind = migrate_engine
    causa.create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    meta.bind = migrate_engine
    causa.drop()
