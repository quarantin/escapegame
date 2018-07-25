from django.template import loader
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
	template = loader.get_template('stranger_things/index.html')
	return HttpResponse(template.render({}, request))

@login_required
def video_player(request):
	return HttpResponse('Video player view (stranger things)')

@login_required
def door_control(request):
	return HttpResponse('Door control view (stranger things)')

@login_required
def light_control(request):
	return HttpResponse('Light control view (stranger things)')
