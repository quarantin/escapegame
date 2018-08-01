from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='Index'),
	path('escapegame/<slug:slug>', views.escapegame, name='Escape Game'),
]
