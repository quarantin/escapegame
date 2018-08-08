from django.template import loader
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseServerError

from siteconfig.forms import JsonImportForm, JsonExportForm

import json

@csrf_exempt
def json_import_view(request):

	try:
		if request.method == 'POST':
			form = JsonImportForm(request.POST, request.FILES)
			if form.is_valid():
				form.json_import(request.FILES['json_configuration'])
				messages.success(request, "Successfully uploaded file '%s'" % request.FILES['json_configuration'])

		else:
			form = JsonImportForm()

		context = {
			'form': form,
		}

		template = loader.get_template('siteconfig/json-import.html')
		return HttpResponse(template.render(context, request))

	except Exception as err:
		return HttpResponseServerError('Error: %s' % err)

import traceback

@csrf_exempt
def json_export_view(request):

	try:
		if request.method == 'POST':
			form = JsonExportForm(request.POST)
			if form.is_valid():

				jsonconfig = form.json_export(request.POST)

				filename = jsonconfig.pop('filename', 'escapegame-config.json')
				indent = jsonconfig.pop('indent', None) or None
				if indent:
					indent = 4

				jsonstring = json.dumps(jsonconfig, indent=indent)
				response = HttpResponse(jsonstring, content_type='application/json')
				response['Content-Disposition'] = 'attachment; filename=%s' % filename
				response['Content-Length'] = len(jsonstring)
				return response

		else:
			form = JsonExportForm()

		context = {
			'form': form,
		}

		template = loader.get_template('siteconfig/json-export.html')
		return HttpResponse(template.render(context, request))

	except Exception as err:
		return HttpResponseServerError('Error: %s' % traceback.format_exc())
