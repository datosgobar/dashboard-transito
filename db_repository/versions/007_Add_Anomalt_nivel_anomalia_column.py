from sqlalchemy import *
from migrate import *


def upgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)
    anomaly = Table('anomaly', meta, autoload=True)
    nivel_anomalia = Column('nivel_anomalia', Integer, nullable=False)
    # Upgrade operations go here.
    meta.bind = migrate_engine
    nivel_anomalia.create(anomaly)


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    meta = MetaData(bind=migrate_engine)
    anomaly = Table('anomaly', meta, autoload=True)
    nivel_anomalia = Column('nivel_anomalia', Integer, nullable=False)
    meta.bind = migrate_engine
    nivel_anomalia.drop(anomaly)
