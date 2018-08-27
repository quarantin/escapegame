#!/usr/bin/python3

import sys

import time

import requests


urls_1001_nuits = [
	'http://escapegame.local/web/les-1001-nuits/sas-les-1001-nuits/debut-du-jeu/validate/',
	'http://escapegame.local/web/les-1001-nuits/la-fontaine/la-fontaine/validate/',
	'http://escapegame.local/web/les-1001-nuits/la-fontaine/les-dalles/validate/',
	'http://escapegame.local/web/les-1001-nuits/la-caverne/le-marchand/validate/',
	'http://escapegame.local/web/les-1001-nuits/la-caverne/le-lanceur-de-couteaux/validate/',
	'http://escapegame.local/web/les-1001-nuits/la-caverne/le-charmeur-de-serpents/validate/',
	'http://escapegame.local/web/les-1001-nuits/la-caverne/le-fakir/validate/',
	'http://escapegame.local/web/les-1001-nuits/la-lampe/la-lampe/validate/',
]

urls_stranger_things = [
	'http://escapegame.local/web/stranger-things/sas-stranger-things-salle-claire/debut-du-jeu/validate/',
	'http://escapegame.local/web/stranger-things/sas-stranger-things-salle-obscure/debut-du-jeu/validate/',
	'http://escapegame.local/web/stranger-things/la-salle-claire/chall-1/validate/',
	'http://escapegame.local/web/stranger-things/la-salle-claire/chall-2/validate/',
	'http://escapegame.local/web/stranger-things/la-salle-obscure/chall-1/validate/',
	'http://escapegame.local/web/stranger-things/la-salle-obscure/chall-2/validate/',
	'http://escapegame.local/web/stranger-things/la-foret/chall-1/validate/',
	'http://escapegame.local/web/stranger-things/la-foret/chall-2/validate/',
]



urls = urls_1001_nuits

if len(sys.argv) > 1:

	game = sys.argv[1]

	if game == '1001-nuits':
		urls = urls_1001_nuits

	elif game == 'stranger-things':
		urls = urls_stranger_things

	else:
		print('Invalid game: `%s` (Must be one of 1001-nuits or stranger-things)' % game)
		sys.exit()

input('Press enter to start validating the challenges for escape game %s' % game)

for url in urls:
	time.sleep(2)
	requests.get(url)
