from django.template import loader
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
	template = loader.get_template('stranger_things/index.html')
	return HttpResponse(template.render({}, request))
