# -*- coding: utf-8 -*-

from django.apps import AppConfig

from celery.task.control import inspect, revoke

from ast import literal_eval

import logging
import redis
import json


class EscapegameConfig(AppConfig):
	name = 'escapegame'
	logger = logging.getLogger(name)
	tasks = {}

	def redis_client(self):

		# Redis is using a connection pool, so no
		# need to worry about closing connections.
		from siteconfig.settings import REDIS_HOST, REDIS_PORT
		return redis.Redis(host=REDIS_HOST, port=REDIS_PORT)

	def ready(self):

		# Register signals
		from .signals import save
		from .signals import constance

		# Register video player task
		# (Only if the table exists to avoid errors when populating database)
		from multimedia import tasks
		from django.db import connection
		db_tables = connection.introspection.table_names()
		if 'multimedia_video' in db_tables:
			tasks.setup_background_tasks()

		# Run Redis tasks
		# (all hosts should do it including the master)
		self.run_redis_tasks()

	def publish_redis_tasks(self):
		from controllers.models import ChallengeGPIO

		tasks = {}

		gpios = ChallengeGPIO.objects.all()
		for gpio in gpios:

			host = gpio.controller.hostname
			if host not in tasks:
				tasks[host] = {}
				tasks[host]['challenges'] = []

			tasks[host]['challenges'].append(gpio.id)

		client = self.redis_client()

		for host in tasks:

			key = 'tasks:%s' % host
			val = json.dumps(tasks[host])

			print("\n###\nPublising redis tasks (%s, %s)..." % (key, val))

			client.set(key, val)

	def get_running_tasks(self):
		from siteconfig.settings import MASTER_HOSTNAME, MASTER_TLD

		running_tasks = {}

		my_celery_id = 'celery@%s' % MASTER_HOSTNAME.replace(MASTER_TLD, '')
		celery_tasks = inspect().active()
		if not celery_tasks:
			print('\n###\nNo task already running!')
			return running_tasks

		my_tasks = celery_tasks[my_celery_id]
		for task in my_tasks:

			gpio_id = literal_eval(task['args'])[0]
			task_id = task['id']

			print('\n###\nFound already running task for GPIO ID %d: %s' % (gpio_id, task_id))
			running_tasks[gpio_id] = task_id

		return running_tasks

	def terminate_obsolete_tasks(self, running_tasks, published_tasks):

		real_running_tasks = running_tasks
		running_tasks = list(running_tasks)
		for gpio_id in running_tasks:

			if gpio_id not in published_tasks['challenges']:

				task_id = running_tasks[gpio_id]
				revoke(task_id, terminate=True)

				print('\n###\nFound obsolete running task for GPIO ID %d: %s, killing it' % (gpio_id, task_id))
				del real_running_tasks[gpio_id]

		if not running_tasks:
			print('\n###\nNo obsolete task to terminate!')

	def start_non_running_tasks(self, running_tasks, published_tasks):
		from .tasks import poll_challenge_gpio

		for gpio_id in published_tasks['challenges']:

			if gpio_id not in running_tasks:
				task = poll_challenge_gpio.delay(gpio_id)
				running_tasks[gpio_id] = task.id

			print('\n###\nI\'m running the following task: poll_challenge_gpio(%d) [%s]' % (gpio_id, running_tasks[gpio_id]))

		if not published_tasks['challenges']:
			print('\n###\nNo non-running tasks found!')

	def get_published_tasks(self):
		from controllers.models import RaspberryPi

		myself = RaspberryPi.get_myself()

		key = 'tasks:%s' % myself.hostname
		empty_task_list = b'{ "challenges": [] }'

		client = self.redis_client()

		jsonstring = client.get(key)
		if not jsonstring:
			jsonstring = empty_task_list

		return json.loads(jsonstring.decode('utf-8'))

	def run_redis_tasks(self):

		# Publish all Redis tasks
		# (only the master should do it)
		from siteconfig.settings import IS_MASTER
		if IS_MASTER:
			self.publish_redis_tasks()

		# Get the list of already running tasks from celery
		running_tasks = self.get_running_tasks()

		# Retrive the list of tasks published in Redis
		published_tasks = self.get_published_tasks()

		# Terminate the tasks that are now obsolete. A task could become obsolete for example
		# if a change in the configuration of the GPIO occurs (let's say the PIN number).
		self.terminate_obsolete_tasks(running_tasks, published_tasks)

		# Start the tasks that are not already running
		self.start_non_running_tasks(running_tasks, published_tasks)
