from django.template import loader
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
	template = loader.get_template('1001_nuits/index1001.html')
	return HttpResponse(template.render({}, request))

@login_required
def video_player(request):
	return HttpResponse('Video player view (1001 nuits)')

@login_required
def door_control(request):
	return HttpResponse('Door control view (1001 nuits)')

@login_required
def light_control(request):
	return HttpResponse('Light control view (1001 nuits)')

@login_required
def settings(request):
	return HttpResponse('Settings view (1001 nuits)')
