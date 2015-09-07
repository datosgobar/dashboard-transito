#!/usr/bin/env python
# -*- coding: utf-8 -*-

import analisis
import os
import datetime

from dashboard_logging import dashboard_logging
logger = dashboard_logging(config="analisis/logging.json", name=__name__)


def run():
    """
        sudo crontab -e
        0 0 * * * /usr/bin/python2.7 /tu_home/tu_user/dashboard-operativo-transito/analisis/dailyUpdate.py
    """
    if os.environ.get('OPENSHIFT_PYTHON_DIR'):
        # en caso de estarlo, activo entorno virtual y agarro las variables de
        # entorno para ip y puerto
        zvirtenv = os.path.join(os.environ['OPENSHIFT_PYTHON_DIR'],
                                'virtenv', 'bin', 'activate_this.py')
        execfile(zvirtenv, dict(__file__=zvirtenv))

    analisis.dailyUpdate()
    logger.info("run dailyUpdate, time:{0}".format(datetime.datetime.now()))

if __name__ == '__main__':
    run()
