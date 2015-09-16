from sqlalchemy import *
from migrate import *

# TipoCorte = Table(
#     'tipo_corte', meta,
#     Column('id', Integer, primary_key=True),
#     Column('descripcion', String(140), nullable=False)
# )

def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pass


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pass
