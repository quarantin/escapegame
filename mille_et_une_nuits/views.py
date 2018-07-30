from django.template import loader
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.edit import UpdateView
from django.contrib.auth.decorators import login_required

from escapegame.models import EscapeGame, EscapeGameRoom

@login_required
def index(request):
	template = loader.get_template('1001_nuits/index.html')

	# TODO retrieve video_path from database
	context = { 'video_path': 'test.h264' }

	return HttpResponse(template.render(context, request))
