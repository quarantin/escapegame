from django.urls import path
from . import views

urlpatterns = [
	path('open/<int:pin>', views.open_door, name='Open door'),
	path('close/<int:pin>', views.close_door, name='Close door'),
]
