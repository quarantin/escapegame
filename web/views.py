from django.shortcuts import render
from django.http import HttpResponse

def index(request):
	return HttpResponse('Hello World!!!')

def video_player(request):
	return HttpResponse('Hello Video Player!!!')
