from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='Index'),
	path('video-player', views.video_player, name='Video Player'),
	path('door-control', views.door_control, name='Door Control'),
	path('light-control', views.light_control, name='Light Control'),
	path('door-control', views.door_control, name='Door Control'),
]
