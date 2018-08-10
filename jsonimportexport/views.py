from django.template import loader
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseServerError

from siteconfig.admin import JsonImportForm, JsonExportForm

import json

def json_import_export_view(request):

	try:
		context = {}
		template = loader.get_template('admin/app_index.html')
		return HttpResponse(template.render(context, request))

	except Exception as err:
		return HttpResponseServerError('Error: %s' % err)

@csrf_exempt
def json_import_view(request):

	try:
		if request.method == 'POST':
			form = JsonImportForm(request.POST, request.FILES)
			if form.is_valid():
				jsonfile = request.FILES['json_configuration']
				status, message = form.json_import(jsonfile)
				if status != 0:
					messages.error(request, "Failed to upload JSON file '%s' (%s)" % (jsonfile, message))
				else:
					messages.success(request, "Successfully uploaded file '%s'" % jsonfile)
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
		#template = loader.get_template('admin/app_index.html')
		return HttpResponse(template.render(context, request))

	except Exception as err:
		return HttpResponseServerError('Error: %s' % traceback.format_exc())
