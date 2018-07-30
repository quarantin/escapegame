from django.template import loader
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
	template = loader.get_template('escapegame/index.html')
	return HttpResponse(template.render({}, request))
