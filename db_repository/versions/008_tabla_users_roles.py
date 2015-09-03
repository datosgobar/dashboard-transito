from sqlalchemy import *
from migrate import *
from datetime import datetime
from cork.backends import SqlAlchemyBackend
from cork import Cork
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
import sys

sys.path.insert(1, "../")
import config

meta = MetaData()


def add_user(Base, session):
    Users = Base.classes.users
    sqlalchemy_backend = Cork(backend=SqlAlchemyBackend(config.db_url))
    session.add(Users(username="transito", role="admin", hash=sqlalchemy_backend._hash("transito", "transito"),
                      email_addr="transito@buenosaires.gob.ar", desc="operario",
                      creation_date=str(datetime.now()), last_login=str(datetime.now())
                      ))
    session.commit()
    session.close()


def add_role(Base, session):
    Roles = Base.classes.roles
    session.add(Roles(
        role='admin', level=100
    ))
    session.commit()
    session.close()


def init():
    Base = automap_base()
    engine = create_engine(config.db_url)
    Base.prepare(engine, reflect=True)
    session = Session(engine)
    add_role(Base, session)
    add_user(Base, session)


roles = Table('roles', meta,
              Column('role', String(128), primary_key=True),
              Column('level', Integer, nullable=False)
              )

users = Table('users', meta,
              Column('username', Unicode(128), primary_key=True),
              Column('role', ForeignKey("roles.role")),
              Column('hash', String(256), nullable=False),
              Column('email_addr', String(128)),
              Column('desc', String(128)),
              Column('creation_date', String(128), nullable=False),
              Column('last_login', String(128), nullable=False)
              )


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    roles.create()
    users.create()
    init()


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    users.drop()
    roles.drop()
