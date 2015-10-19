#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import *
from migrate import *
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
import sys
import os
import json

from info_corredores import cortes

sys.path.insert(1, "../")
import config

meta = MetaData()

TipoCorte = Table(
    'tipo_corte', meta,
    Column('id', Integer, primary_key=True),
    Column('descripcion', String(140), nullable=False)
)

def init():
    Base = automap_base()
    engine = create_engine(config.db_url)
    Base.prepare(engine, reflect=True)
    session = Session(engine)
    add_cortes(Base, session)


def add_cortes(Base, session):
    """
    Guarda el enum de causas de una anomalia
    """
    # pdb.set_trace()
    TipoCorte = Base.classes.tipo_corte
    for corte in cortes:
        if not session.query(TipoCorte).filter(TipoCorte.id == corte['id']).count():
            session.add(
                TipoCorte(descripcion=corte['descripcion'].encode('utf-8'), id=corte['id']))
            session.commit()
    session.close()


def upgrade(migrate_engine):
    # Upgrade operations go here.
    meta.bind = migrate_engine
    TipoCorte.create()
    init()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    meta.bind = migrate_engine
    TipoCorte.drop()
