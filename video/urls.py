from django.urls import path
from . import views

urlpatterns = [
	path('play/<str:filename>', views.play_video, name='Play video'),
	path('stop', views.stop_video, name='Stop video'),
]
