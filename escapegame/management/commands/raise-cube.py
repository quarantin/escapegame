from django.core.management.base import BaseCommand

from escapegame import libraspi

import sys


class Command(BaseCommand):
	help = 'Triggers cube opening after a specific number of seconds'

	def add_arguments(self, parser):
		parser.add_argument('--pin', required=True, type=int)
		parser.add_argument('--action', required=True, type=str, choices=[ 'lower', 'raise' ])

	def handle(self, *args, **options):

		pin = options['pin']
		action = options['action']

		sys.stdout.write(self.style.MIGRATE_HEADING('Cube opening\n'))

		signal = (action == 'raise' and 'HIGH' or 'LOW')
		sys.stdout.write('  Sending signal %s to pin number %d...' % (signal, pin))
		sys.stdout.flush()

		state = (action == 'raise')
		libraspi.set_pin_state(pin, state)
		sys.stdout.write(self.style.SUCCESS(' OK\n'))
