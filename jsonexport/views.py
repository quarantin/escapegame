from django.template import loader
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseServerError

from .models import JsonImportForm, JsonExportForm

import json

@csrf_exempt
def json_index(request):

	try:
		context = {}
		template = loader.get_template('jsonexport/index.html')
		return HttpResponse(template.render(context, request))

	except Exception as err:
		return HttpResponseServerError('Error: %s' % err)

@csrf_exempt
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

import traceback

@csrf_exempt
def json_export(request):

	try:
		if request.method == 'POST':
			form = JsonExportForm(request.POST)
			if form.is_valid():

				jsonconfig = form.dump(request.POST)

				jsonfile = jsonconfig.pop('filename', 'escapegame-config.json')
				indent = jsonconfig.pop('indent', None) or None
				if indent:
					indent = 4

				jsonstring = json.dumps(jsonconfig, indent=indent)
				response = HttpResponse(jsonstring, content_type='application/json')
				response['Content-Disposition'] = 'attachment; filename=%s' % jsonfile
				response['Content-Length'] = len(jsonstring)
				return response

		else:
			form = JsonExportForm()

		context = {
			'form': form,
		}

		template = loader.get_template('jsonexport/export.html')
		#template = loader.get_template('admin/app_index.html')
		return HttpResponse(template.render(context, request))

	except Exception as err:
		return HttpResponseServerError('Error: %s' % traceback.format_exc())
