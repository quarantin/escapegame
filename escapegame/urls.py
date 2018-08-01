from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='Index'),
	path('<slug:slug>', views.escapegame, name='Escape Game'),
	path('<slug:slug>/start', views.escapegame_start, name='Start Escape Game'),
	path('<slug:slug>/video/play', views.video_play, name='Play Brief Video'),
	path('<slug:slug>/video/stop', views.video_stop, name='Stop Brief Video'),
	path('<slug:slug>/door/<int:pin>', views.door_status, name='Door Status'),
	path('<slug:slug>/door/<int:pin>/open', views.door_open, name='Open door'),
	path('<slug:slug>/door/<int:pin>/close', views.door_close, name='Close door'),
]
