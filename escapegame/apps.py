# -*- coding: utf-8 -*-

from django.db import connection
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

		# Update Redis tasks
		# (only the master should do it)
		from siteconfig.settings import IS_MASTER
		if IS_MASTER:
			self.update_redis_tasks()

		# Run Redis tasks
		# (all hosts should do it including the master)
		self.run_redis_tasks()

	def redis_connection(self):

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
