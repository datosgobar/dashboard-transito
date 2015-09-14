from sqlalchemy import *
from migrate import *
from cork.backends import SqlAlchemyBackend
from cork import Cork
import sys

sys.path.insert(1, "../")
import config


def change_pass(pwd):
    sqlalchemy_backend = Cork(backend=SqlAlchemyBackend(config.db_url))
    metadata = MetaData()
    engine = create_engine(config.db_url)
    metadata.bind = engine
    users = Table("users", metadata, extend_existing=True,
                  autoload=True, autoload_with=engine)
    users.update().where(users.c.username == "transito").values(
        hash=sqlalchemy_backend._hash("transito", pwd)).execute()


def upgrade(migrate_engine):
    change_pass("tr4ns1t01234")


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    change_pass("transito")
