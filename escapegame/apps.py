# -*- coding: utf-8 -*-

from django.apps import AppConfig

import logging
import redis
import json

class EscapegameConfig(AppConfig):
	name = 'escapegame'
	logger = logging.getLogger(name)
	client = None

	def ready(self):

		# Register signals
		from .signals import save
		from .signals import constance

		# Connect to Redis server
		from siteconfig.settings import REDIS_HOST, REDIS_PORT
		self.client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)

		# Register video player task
		# (Only if the table exists to avoid errors when populating database)
		from multimedia import tasks
		from django.db import connection
		db_tables = connection.introspection.table_names()
		if 'multimedia_video' in db_tables:
			tasks.setup_background_tasks()

		# Update Redis tasks
		# (only the master should do it)
		from siteconfig.settings import IS_MASTER
		if IS_MASTER:
			self.update_redis_tasks()

		# Run Redis tasks
		# (all hosts should do it including the master)
		self.run_redis_tasks()

	def update_redis_tasks(self):
		from controllers.models import ChallengeGPIO

		tasks = {}

		gpios = ChallengeGPIO.objects.all()
		for gpio in gpios:

			host = gpio.controller.hostname
			if host not in tasks:
				tasks[host] = {}
				tasks[host]['challenges'] = {}

			tasks[host]['challenges']['reset_pin'] = gpio.reset_pin
			tasks[host]['challenges']['action_pin'] = gpio.action_pin

		for host in tasks:

			key = 'tasks:%s' % host
			val = json.dumps(tasks[host])

			print("Updating redis tasks (%s, %s)..." % (key, val))

			self.client.set(key, val)

	def run_tasks(self):
		from controllers.models import RaspberryPi

		myself = RaspberryPi.get_myself()

		key = 'tasks:%s' % myself.hostname

		jsonstring = self.client.get(key)
		jsondata = json.loads(jsonstring)

		print("I am %s and I will run the following tasks:")
		print(json.dump(jsondata, indent=4))

	def taskLogger(pin):
		return logging.getLogger('%s.tasks.poll.gpio.%d' % (EscapegameConfig.name, pin))
