#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os

def getData():
	
	filecorredorfake = os.path.abspath("analisis/corredores_fake.json")
	with open(filecorredorfake) as f:
		output = json.loads(f.read())

	return output

def parserEmitDataFake(self, result):
  """
    funcion que trae los datos de mongo, crea un json y emite al front segun corredor
  """
  corredores = ["independencia", "Illia", "nueve_de_julio", "alem", "corrientes", \
  "rivadavia", "av_de_mayo", "san_martin", "juan_b_justo", "cordoba", "paseo_colon", "cabildo", "pueyrredon", "alcorta", "libertador"]

  if len(result):
    for i in range(len(corredores)):
      self.emit(corredores[i], result['corredores'][i][result['corredores'][i].keys()[0]])
      time.sleep(0.5)
  else:
    self.emit('info', "sin datos")