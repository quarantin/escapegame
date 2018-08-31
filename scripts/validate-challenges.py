#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import imp
import sys
import time
import requests


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MASTER_FILE = 'master-hostname.txt'

MASTER = imp.load_source(MASTER_FILE, os.path.join(BASE_DIR, MASTER_FILE))


urls_1001_nuits = [
	'web/les-1001-nuits/sas-les-1001-nuits/debut-du-jeu/validate/',
	'web/les-1001-nuits/la-fontaine/la-fontaine/validate/',
	'web/les-1001-nuits/la-fontaine/les-dalles/validate/',
	'web/les-1001-nuits/la-caverne/le-marchand/validate/',
	'web/les-1001-nuits/la-caverne/le-lanceur-de-couteaux/validate/',
	'web/les-1001-nuits/la-caverne/le-charmeur-de-serpents/validate/',
	'web/les-1001-nuits/la-caverne/le-fakir/validate/',
	'web/les-1001-nuits/la-lampe/la-lampe/validate/',
]

urls_stranger_things = [
	'web/stranger-things/sas-stranger-things-salle-claire/debut-du-jeu/validate/',
	'web/stranger-things/sas-stranger-things-salle-obscure/debut-du-jeu/validate/',
	'web/stranger-things/la-salle-claire/chall1/validate/',
	'web/stranger-things/la-salle-claire/chall2/validate/',
	'web/stranger-things/la-salle-obscure/chall1/validate/',
	'web/stranger-things/la-salle-obscure/chall2/validate/',
	'web/stranger-things/la-foret/chall1/validate/',
	'web/stranger-things/la-foret/chall2/validate/',
]

host = '%s%s' % (MASTER.HOSTNAME, MASTER.TLD)
port = ''

game = '1001-nuits'
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
	time.sleep(3)
	fullurl = 'http://%s%s/%s' % (host, port, url)
	print('Requesting URL %s' % fullurl)
	requests.get(fullurl)
