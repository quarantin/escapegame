# -*- coding: utf-8 -*-

from django import forms
from django.urls import path
from django.apps import apps
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from siteconfig import settings

from escapegame.admin import site

from escapegame.models import *

from .models import *

from . import views

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
	#	return [
	#		path('import/', views.json_import, name='json_import'),
	#	]

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

	#def get_urls(self):
	#	return [
	#		path('export/', views.json_export, name='json_export'),
	#	]

site.register([ JsonImport ], JsonImportAdmin)
site.register([ JsonExport ], JsonExportAdmin)
