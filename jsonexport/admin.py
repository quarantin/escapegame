# -*- coding: utf-8 -*-

from django import forms
from django.urls import path
from django.apps import apps
from django.contrib import admin

from siteconfig import settings
from escapegame.admin import site
from escapegame.models import *
from .models import *
from . import views

from collections import OrderedDict
from datetime import datetime
import json


#
# Admin models
#

class JsonImportAdmin(admin.ModelAdmin):
	form = JsonImportForm

	def get_changelist_form(self, request):
		return self.change_list_form

	def has_add_permission(self, *args, **kwargs):
		return False

	def has_del_permission(self, *args, **kwargs):
		return False

	def has_change_permission(self, request, obj=None):
		return request.user.is_superuser

class JsonExportAdmin(admin.ModelAdmin):
	form = JsonExportForm

	def get_changelist_form(self, request):
		return self.change_list_form

	def has_add_permission(self, *args, **kwargs):
		return False

	def has_del_permission(self, *args, **kwargs):
		return False

	def has_change_permission(self, request, obj=None):
		return request.user.is_superuser

#
# Register our models to our custom admin site
#

site.register([ JsonImport ], JsonImportAdmin)
site.register([ JsonExport ], JsonExportAdmin)
