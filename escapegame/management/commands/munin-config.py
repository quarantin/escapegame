# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand

from controllers.models import RaspberryPi

import os


class Command(BaseCommand):
	help = 'Generate configuration file for Munin master'

	def handle(self, *args, **options):

		delay = os.getenv('WAIT_DELAY') or 1

		self.stdout.write('# Munin configuration generated automatically by script:')
		self.stdout.write('# %s' % os.path.realpath(__file__))
		self.stdout.write('')
		self.stdout.write('includedir /etc/munin/munin-conf.d')
		self.stdout.write('')
		self.stdout.write('[localhost.localdomain]')
		self.stdout.write('\taddress 127.0.0.1')
		self.stdout.write('\tuse_node_name yes')

		raspis = RaspberryPi.objects.all()

		for raspi in raspis:
			self.stdout.write('')
			self.stdout.write('[%s]' % raspi.hostname)
			self.stdout.write('\taddress %s' % raspi.hostname)

