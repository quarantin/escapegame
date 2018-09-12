# -*- coding: utf-8 -*-

from django.db import connection
from django.apps import AppConfig

import logging


class EscapegameConfig(AppConfig):
	name = 'escapegame'
	logger = logging.getLogger(name)

	def ready(self):
		from siteconfig.settings import IS_MASTER
		from multimedia import tasks as ext_tasks
		from . import tasks as int_tasks
		from .signals import save
		from .signals import constance

		if IS_MASTER:
			self.updateRedisTasks()

		db_tables = connection.introspection.table_names()

		if 'escapegame_escapegame' in db_tables:
		   int_tasks.setup_background_tasks()

		if 'multimedia_video' in db_tables:
			ext_tasks.setup_background_tasks()

	def updateRedisTasks(self):
		from siteconfig.settings import REDIS_HOST
		from controllers.models import ChallengeGPIO
		import redis
		import json

		client = redis.Redis(host=REDIS_HOST)

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

			client.set(key, val)

	def taskLogger(pin):
		return logging.getLogger('%s.tasks.poll.gpio.%d' % (EscapegameConfig.name, pin))
