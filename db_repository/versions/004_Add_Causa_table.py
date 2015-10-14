#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import *
from migrate import *
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
import sys
import os
import json

sys.path.insert(1, "../")
import config

meta = MetaData()

causa = Table(
    'causa', meta,
    Column('id', Integer, primary_key=True),
    Column('descripcion', String(140), nullable=False))


def init():
    Base = automap_base()
    engine = create_engine(config.db_url)
    Base.prepare(engine, reflect=True)
    session = Session(engine)
    add_causas(Base, session)


def add_causas(Base, session):
    """
    Guarda el enum de causas de una anomalia
    """
    # pdb.set_trace()
    Causa = Base.classes.causa
    file_causas = os.path.realpath("../dashboard-operativo-transito/static/data/causas.json")
    with open(file_causas) as causas_data:
        causas = json.load(causas_data)
    for causa in causas['causas']:
        if not session.query(Causa).filter(Causa.id == causa['id']).count():
            session.add(
                Causa(descripcion=causa['descripcion'].encode('utf-8'), id=causa['id']))
            session.commit()
    session.close()


def upgrade(migrate_engine):
    # Upgrade operations go here.
    meta.bind = migrate_engine
    causa.create()
    init()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    meta.bind = migrate_engine
    causa.drop()
