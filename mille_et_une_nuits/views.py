from django.template import loader
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.edit import UpdateView
from django.contrib.auth.decorators import login_required

from escapegame import libraspi

from .models import MilleEtUneNuitsSettings

@login_required
def index(request):

	if request.method == 'POST':

		settings = MilleEtUneNuitsSettings.load()

		if 'play-video' in request.POST:
			libraspi.play_video(settings.video_path)

		elif 'lock-garden-door' in request.POST:
			libraspi.close_door(settings.pin_door_garden)

		elif 'unlock-garden-door' in request.POST:
			libraspi.open_door(settings.pin_door_garden, settings.pin_door_garden_duration)

	template = loader.get_template('1001_nuits/index.html')
	return HttpResponse(template.render({}, request))

@login_required
def door_control(request):
	return HttpResponse('Door control view (1001 nuits)')

@login_required
def light_control(request):
	return HttpResponse('Light control view (1001 nuits)')
