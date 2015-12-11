#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cProfile
import StringIO
import pstats
import contextlib

import sqlalchemy
from sqlalchemy import create_engine, exc, event
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.engine import Engine
from smtp_send import send_email_error

import time
import logging

from dashboard_logging import dashboard_logging
logger = dashboard_logging(config="logging.json", name=__name__)
logger.info("inicio conexion a base de datos")

def sqlalchemyDEBUG():

    from sqlalchemy import event
    from sqlalchemy.engine import Engine

    global profiled
    global before_cursor_execute
    global after_cursor_execute

    @event.listens_for(Engine, "before_cursor_execute")
    def before_cursor_execute(conn, cursor, statement,
                              parameters, context, executemany):
        conn.info.setdefault('query_start_time', []).append(time.time())
        logger.debug("Start Query: %s", statement)

    @event.listens_for(Engine, "after_cursor_execute")
    def after_cursor_execute(conn, cursor, statement,
                             parameters, context, executemany):
        total = time.time() - conn.info['query_start_time'].pop(-1)
        logger.debug("Query Complete!")
        logger.debug("Total Time: %f", total)

    @contextlib.contextmanager
    def profiled():
        pr = cProfile.Profile()
        pr.enable()
        yield
        pr.disable()
        s = StringIO.StringIO()
        ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
        ps.print_stats()
        # uncomment this to see who's calling what
        # ps.print_callers()
        print s.getvalue()

# sqlalchemyDEBUG()
"""
http://docs.sqlalchemy.org/en/latest/orm/extensions/automap.html?highlight=automap_base#sqlalchemy.ext.automap.AutomapBase.prepare.params.reflect

Reflect – if True, the MetaData.reflect() method is called on the
MetaData associated with this AutomapBase. The Engine passed via
AutomapBase.prepare.engine will be used to perform the reflection
if present
else, the MetaData should already be bound to some engine
else the operation will fail.
"""


class instanceSQL(object):

    def __init__(self, **params):
        self.cache_tables = set()
        self.debug = params.pop('debug', False)
        self.debug_pool = params.pop('debug_pool', False)
        self.cfg = params.pop('cfg', "config.py")
        self.__engine = False
        self.Session = False
        self.__c = False
        self.Base = automap_base()

    def createDBEngine(self):
        """
                http://docs.sqlalchemy.org/en/latest/core/engines.html?highlight=create_engine#sqlalchemy.create_engine
                engine = sqlalchemy.create_engine(
                    "postgres://postgres@/postgres")
                engine = sqlalchemy.create_engine("sqlite:///analysis.db")
        """
        try:
            self.__engine = create_engine(
                self.cfg.db_url, echo=self.debug, pool_timeout=60, echo_pool=self.debug_pool, client_encoding=self.cfg.db["client_encoding"])
            self.Base.prepare(self.__engine, reflect=True)
            self.__c = True
        except Exception, e:
            msg_error = "OperationalError: not connect {0} , traceback:{1}".format(self.cfg.db_url, e)
            logger.error("OperationalError: not connect {0} ".format(self.cfg.db_url), traceback=True)
            send_email_error(msg_error)

    def __unique(self, unique_table=""):
        assert self.Base.classes.has_key(unique_table)
        instance = self.Base.classes.get(unique_table)
        self.cache_tables.update([instance])
        return instance

    def listTables(self):
        if self.__c:
            return self.Base.classes.keys()
        else:
            return "OperationalError: not connect".format(self.cfg.db_url)

    def instanceTable(self, **args):
        """
        params
                instanceTable(unique_table="MyTable")
                instanceTable(list_tables=['MyTable1', 'MyTable2', 'MyTable3'])

        """
        table_name = args.pop('unique_table', "").lower()
        list_tables = set(args.pop('list_tables', []))
        if table_name:
            instance = self.__unique(unique_table=table_name.lower())
            return instance
        elif list_tables:
            for table in list_tables:
                self.__unique(unique_table=table)
            return self.cache_tables

    def getDBConnection(self):
        conn = self.__engine.connect()
        return conn

    def session(self, individual=True):
        """
                .session()
            individual is not global
                http://docs.sqlalchemy.org/en/latest/orm/session_api.html?highlight=sessionmaker#session-and-sessionmaker
        """
        if individual:
            self.Session = sessionmaker()
            self.Session.configure(bind=self.__engine)
            return self.Session()
        elif individual == False:
            self.Session = sessionmaker(autoflush=False)
            return self.Session()


def main():

    import config
    sqlalchemyDEBUG()

    with profiled():
        conn = instanceSQL(cfg=config)
        conn.createDBEngine()
        conn.instanceTable(
            list_tables=['causa', 'historical', 'anomaly', 'segment_snapshot'])


if __name__ == '__main__':
    main()
