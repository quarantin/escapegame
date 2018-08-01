from django.template import loader
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from .models import EscapeGame, EscapeGameRoom

@login_required
def index(request):

	context = {
		'games': EscapeGame.objects.all(),
	}

	template = loader.get_template('escapegame/index.html')

	return HttpResponse(template.render(context, request))

@login_required
def escapegame(request, slug):

	game = EscapeGame.objects.get(slug=slug)

	context = {
		'game': game,
		'rooms': EscapeGameRoom.objects.filter(game=game),
	}

	template = loader.get_template('escapegame/escapegame.html')

	return HttpResponse(template.render(context, request))
