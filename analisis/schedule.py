#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import time
import analisis
import os

from dashboard_logging import dashboard_logging
logger = dashboard_logging(config="analisis/logging.json", name=__name__)

if os.environ.get('OPENSHIFT_PYTHON_DIR'):
    # en caso de estarlo, activo entorno virtual y agarro las variables de
    # entorno para ip y puerto
    zvirtenv = os.path.join(os.environ['OPENSHIFT_PYTHON_DIR'],
                            'virtenv', 'bin', 'activate_this.py')
    execfile(zvirtenv, dict(__file__=zvirtenv))
    logger.info("activo virtenv openshift")
else:
    pass


class setInterval:

    def __init__(self):

        self.setTimeOut = 0
        self.dawn = [23, 00, 1, 2, 3, 4, 5, 6, 6]
        # 36 extraccion lun/vier, 9 extraciones sab/dom
        self.morning = range(7, 10)
        # 42 extraccion lun/vier, 21 extraciones sab/dom
        self.midday = range(10, 17)
        # 36 extraccion lun/vier, 18 extraciones sab, 9 extraciones dom
        self.afternoon = range(17, 20)
        self.night = range(20, 23)  # 12 extraccion lun/sab, 6 extraciones dom
        self.daily = ['Monday', 'Tuesday', 'Wednesday',
                      'Thursday', 'Friday', 'Saturday', 'Sunday']

    def setCfg(self):
        """
                https://docs.google.com/spreadsheets/d/16C5nXTNsDxncJOF_NCwKmrkqp4SUx4KUAbfWx6rD3Tk/edit#gid=1200731649

                pensar en calibracion, como calibrar entre periodos de horas y de dias

                Lunes a Viernes

                dawn, 23 a 7, 60 min
                morning, 7 a 10 , 5 min
                midday, 10 a 17, 10 min
                afternoon, 17 a 20, 5 min
                night, 20 a 23, 10 min

                Sabado

                dawn, 23 a 7, 60 min
                morning, 7 a 10 , 20 min
                midday, 10 a 17, 20 min
                afternoon, 17 a 20, 10 min
                night, 20 a 23, 10 min

                Domingos

                dawn, 23 a 7, 60 min
                morning, 7 a 10 , 20 min
                midday, 10 a 17, 20 min
                afternoon, 17 a 20, 20 min
                night, 20 a 23, 20 min

        """
        mytime = time.strftime("%A %b %d %Y %H:%M:%S")
        self.D = mytime.split(" ")[0]
        self.H = int(mytime.split(" ")[4].split(":")[0])
        self.M = int(mytime.split(" ")[4].split(":")[1])

        
        if self.H in self.dawn:
            self.setTimeOut = 60 * 59
        elif self.H in self.morning: 
            if self.D in self.daily[0:5]:
                self.setTimeOut = 5 * 60
            else:
                self.setTimeOut = 20 * 60
        elif self.H in self.midday: 
            if self.D in self.daily[0:5]:
                self.setTimeOut = 10 * 60
            else:
                self.setTimeOut = 20 * 60
        elif self.H in self.afternoon:  
            # 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'
            if self.D in self.daily[0:5]:
                self.setTimeOut = 5 * 60
            elif self.D == self.daily[5]: 
                self.setTimeOut = 10 * 60
            else:
                self.setTimeOut = 20 * 60  # Sunday
        elif self.H in self.night: 
            if self.D in self.daily[0:6]:
                self.setTimeOut = 10 * 60
            else:
                self.setTimeOut = 20 * 60

    def run(self):
        """
                hacer resta segun pase el tiempo
        """

        while True:

            self.setCfg()

            interval = self.setTimeOut / 60
            hasta = datetime.datetime.now()
            desde = hasta - datetime.timedelta(minutes=interval)

            analisis.executeLoop(desde, hasta, dontdownload=False)
            logger.info("run schedule, desde:{1} hasta:{0}, interval:{2}, setTimeout:{3}".format(
                hasta, desde, interval, self.setTimeOut))

            time.sleep(self.setTimeOut)


def main():
    setIntervalTime = setInterval()
    setIntervalTime.run()

if __name__ == '__main__':
    main()
