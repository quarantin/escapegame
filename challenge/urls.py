from django.urls import path
from . import views

urlpatterns = [
	path('reset/<int:challenge>', views.reset_challenge, name='Reset challenge'),
	path('solve/<int:challenge>', views.solve_challenge, name='Solve challenge'),
	path('status/<int:gameid>', views.status_challenge, name='Status challenge'),
]
