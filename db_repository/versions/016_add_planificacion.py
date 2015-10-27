#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import *
from migrate import *
from sqlalchemy.schema import Sequence

meta = MetaData()

estadisticas = Table(
    'estadisticas', meta,
    Column('idg', String(40), primary_key=True),
    Column('name', String(240), nullable=False),
    Column('filename', String(240), nullable=False),
    Column('timestamp_start', Date, nullable=False),
    Column('timestamp_end', Date, nullable=False)
)


def upgrade(migrate_engine):
    # Upgrade operations go here.
    meta.bind = migrate_engine
    estadisticas.create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    meta.bind = migrate_engine
    estadisticas.drop()