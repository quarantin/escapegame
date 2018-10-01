# -*- coding: utf-8 -*-

from django.apps import AppConfig

import logging


class EscapegameConfig(AppConfig):
	name = 'escapegame'
	logger = logging.getLogger(name)
