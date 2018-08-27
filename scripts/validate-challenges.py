#!/usr/bin/python3

import requests

urls = [
	'http://escapegame.local/web/les-1001-nuits/sas-les-1001-nuits/debut-du-jeu/validate/',
	'http://escapegame.local/web/les-1001-nuits/la-fontaine/la-fontaine/validate/',
	'http://escapegame.local/web/les-1001-nuits/la-fontaine/les-dalles/validate/',
]

for url in urls:

	input('Press enter to fetch URL:\n%s\n' % url)
	requests.get(url)
