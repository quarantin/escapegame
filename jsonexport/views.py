# -*- coding: utf-8 -*-

from django.template import loader
from django.contrib import messages
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseServerError, JsonResponse

from .models import JsonImportForm, JsonExportForm

import json
import traceback


@login_required
def json_index(request):

	try:
		context = {}
		template = loader.get_template('jsonexport/index.html')
		return HttpResponse(template.render(context, request))

	except Exception as err:
		return HttpResponseServerError('Error: %s' % traceback.format_exc())

@login_required
def json_import(request):

	try:
		if request.method == 'POST':
			form = JsonImportForm(request.POST, request.FILES)
			if form.is_valid():
				jsonfile = request.FILES['json_configuration']
				status, message = form.load(jsonfile)
				if status != 0:
					messages.error(request, "Failed to upload JSON file '%s' (%s)" % (jsonfile, message))
				else:
					messages.success(request, "Successfully imported JSON configuration '%s'" % jsonfile)
		else:
			form = JsonImportForm()

		context = {
			'form': form,
		}

		template = loader.get_template('jsonexport/import.html')
		return HttpResponse(template.render(context, request))

	except Exception as err:
		return HttpResponseServerError('Error: %s' % traceback.format_exc())

@login_required
def json_export(request):

	try:
		if request.method == 'POST':
			form = JsonExportForm(request.POST)
			if form.is_valid():

				jsondata = form.dump(request.POST)

				jsonfile = jsondata.pop('filename', 'escapegame-config.json')

				indent = jsondata.pop('indent', None) or None
				if indent:
					indent = 4

				json_dumps_params = dict(
					ensure_ascii=False,
					indent=indent,
				)

				response = JsonResponse(jsondata, json_dumps_params=json_dumps_params)
				response['Content-Disposition'] = 'attachment; filename=%s' % jsonfile
				return response

		else:
			form = JsonExportForm()

		context = {
			'form': form,
		}

		template = loader.get_template('jsonexport/export.html')
		return HttpResponse(template.render(context, request))

	except Exception as err:
		return HttpResponseServerError('Error: %s' % traceback.format_exc())
