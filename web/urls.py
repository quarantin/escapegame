from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='Index'),
	path('video-player', views.video_player, name='Video Player'),
]
