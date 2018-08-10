# -*- coding: utf-8 -*-

from django import forms
from django.urls import path
from django.apps import apps
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from siteconfig import settings

from escapegame import admin as myadmin

from escapegame.models import *

from .models import *

from collections import OrderedDict

from datetime import datetime

import json

# Admin classes

class JsonImportAdmin(admin.ModelAdmin):
	change_list_form = JsonImportForm

	def get_changelist_form(self, request):
		return self.change_list_form

	def has_add_permission(self, *args, **kwargs):
		return False

	def has_del_permission(self, *args, **kwargs):
		return False

	def has_change_permission(self, request, obj=None):
		return request.user.is_superuser

	#def get_urls(self):
	#	
	#	urlspattern = path()

class JsonExportAdmin(admin.ModelAdmin):
	change_list_form = JsonExportForm

	def get_changelist_form(self, request):
		return self.change_list_form

	def has_add_permission(self, *args, **kwargs):
		return False

	def has_del_permission(self, *args, **kwargs):
		return False

	def has_change_permission(self, request, obj=None):
		return request.user.is_superuser

class JsonImportConfig(object):
	class Meta(object):
		app_label = 'jsonexport'
		object_name = 'JsonImportConfig'
		model_name = 'import'
		module_name = 'import'
		verbose_name = _('JSON Import')
		verbose_name_plural = _('JSON Import')
		private_fields = [],
		abstract = False
		swapped = False

		def get_ordered_objects(self):
			return False

		def get_change_permission(self):
			return 'change_%s' % self.model_name

		@property
		def app_config(self):
			return apps.get_app_config('%s' % self.app_label)

		@property
		def label(self):
			return '%s.%s' % (self.app_label, self.object_name)

		@property
		def label_lower(self):
			return '%s.%s' % (self.app_label, self.model_name)

	_meta = Meta()

class JsonExportConfig(object):
	class Meta(object):
		app_label = 'jsonexport'
		object_name = 'JsonExportConfig'
		model_name = 'export'
		module_name = 'export'
		verbose_name = _('JSON Export')
		verbose_name_plural = _('JSON Export')
		private_fields = [],
		abstract = False
		swapped = False

		def get_ordered_objects(self):
			return False

		def get_change_permission(self):
			return 'change_%s' % self.model_name

		@property
		def app_config(self):
			return apps.get_app_config(self.app_label)

		@property
		def label(self):
			return '%s.%s' % (self.app_label, self.object_name)

		@property
		def label_lower(self):
			return '%s.%s' % (self.app_label, self.model_name)

	_meta = Meta()

myadmin.site.register([ JsonImportConfig ], JsonImportAdmin)
myadmin.site.register([ JsonExportConfig ], JsonExportAdmin)
