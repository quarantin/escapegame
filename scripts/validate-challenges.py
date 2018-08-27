#!/usr/bin/python3

import time

import requests


urls = [
	'http://escapegame.local/web/les-1001-nuits/sas-les-1001-nuits/debut-du-jeu/validate/',
	'http://escapegame.local/web/les-1001-nuits/la-fontaine/la-fontaine/validate/',
	'http://escapegame.local/web/les-1001-nuits/la-fontaine/les-dalles/validate/',
	'http://escapegame.local/web/les-1001-nuits/la-caverne/le-marchand/validate/',
	'http://escapegame.local/web/les-1001-nuits/la-caverne/le-lanceur-de-couteaux/validate/',
	'http://escapegame.local/web/les-1001-nuits/la-caverne/le-charmeur-de-serpents/validate/',
	'http://escapegame.local/web/les-1001-nuits/la-caverne/le-fakir/validate/',
	'http://escapegame.local/web/les-1001-nuits/la-lampe/la-lampe/validate/',
]

input('Press enter to start validating the challenges')

for url in urls:
	time.sleep(2)
	requests.get(url)
