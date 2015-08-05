#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
#import analisis

class setInterval:

	def __init__(self):
		self.__cfg = {}
		self.setTimeOut = 0
		self.dawn = range(7, 24)
		self.dawn.reverse() # 17 extraccion lun/dom, 
		self.morning = range(8, 11) # 36 extraccion lun/vier, 9 extraciones sab/dom
		self.midday = range(11, 18) # 42 extraccion lun/vier, 21 extraciones sab/dom
		self.afternoon = range(18, 21) # 36 extraccion lun/vier, 18 extraciones sab, 9 extraciones dom
		self.night = range(21, 23) # 12 extraccion lun/sab, 6 extraciones dom
		self.daily = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
		#self.setCfg()

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

		if self.H in self.dawn: # [23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7]
			self.setTimeOut = 60*59
		if self.H in self.morning:  # [8, 9, 10]
			if self.D in self.daily[0:5]:
				self.setTimeOut = 5*60
			else:
				self.setTimeOut = 20*60
		if self.H in self.midday: # [11, 12, 13, 14, 15, 16, 17]
			if self.D in self.daily[0:5]:
				self.setTimeOut = 10*60
			else:
				self.setTimeOut = 20*60
		if self.H in self.afternoon: # [18, 19, 20]
			if self.D in self.daily[0:5]: # 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'
				self.setTimeOut = 5*60
			elif self.D == self.daily[5]: # Saturday
				self.setTimeOut = 10*60
			else:
				self.setTimeOut = 20*60 # Sunday
		if self.H in self.night: # [21, 22]
			if self.D in self.daily[0:6]:
				self.setTimeOut = 10*60
			else:
				self.setTimeOut = 20*60

	def run(self):
		"""
			hacer resta segun pase el tiempo
		"""
		#mytime = strftime("%b %d %Y %H:%M:%S")
		#self.init(mytime)

		while True:

			self.setCfg()
			print time.strftime("%H:%M:%S")
			print self.setTimeOut
			print "somethings, another code"
			#analisis.executeLoop()

			time.sleep(self.setTimeOut)


def main():
	setIntervalTime = setInterval()
	setIntervalTime.run()

if __name__ == '__main__':
	main()