#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os

def getData():
	
	filecorredorfake = os.path.abspath("analisis/corredores_fake.json")
	with open(filecorredorfake) as f:
		output = json.loads(f.read())

	return output
