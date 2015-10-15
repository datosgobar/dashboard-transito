#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import *
from migrate import *

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from info_corredores import corredores
from unidecode import unidecode

import sys
import os
import json

meta = MetaData()

sys.path.insert(1, "../")
import config

Corredores = Table(
    'corredores', meta,
    Column('id', Integer, primary_key=True),
    Column('corredor', String(240), nullable=False),
    Column('ids', String(10), nullable=False),
    Column('segmento', String(240), nullable=False),
    Column('sentido', String(240), nullable=False)
)

Waypoints = Table(
    'waypoints', meta,
    Column('id', ForeignKey("corredores.id"), primary_key=True),
    Column('desde', String(240), nullable=False),
    Column('hasta', String(240), nullable=False),
    Column('linestring', String(240), nullable=False),
)


def init():
    Base = automap_base()
    engine = create_engine(config.db_url)
    Base.prepare(engine, reflect=True)
    session = Session(engine)
    add_corredores(Base, session)


def encode_unicode(s):
    return unidecode(s.decode('utf-8'))

def add_corredores(Base, session):
    Corredores = Base.classes.corredores
    Waypoints = Base.classes.waypoints
    for info_corredores in corredores:
        session.add(Corredores(
            id=info_corredores['id'],
            corredor=encode_unicode(info_corredores['corredor']),
            ids=encode_unicode(info_corredores['ids']),
            segmento=encode_unicode(info_corredores['segmento']),
            sentido=info_corredores['sentido']
        ))
        session.add(Waypoints(
            id=info_corredores['id'],
            desde=info_corredores['from'],
            hasta=info_corredores['to'],
            linestring=info_corredores['waypoints']
        ))
    session.commit()
    session.close()


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    Corredores.create()
    Waypoints.create()
    init()


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    Waypoints.drop()
    Corredores.drop()
