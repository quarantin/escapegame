from django.http import JsonResponse

#import RPi.GPIO as GPIO

def open_door(request, pin):

	try:
		#GPIO.output(pin, True)
		return JsonResponse({ 'status': 'OK' })
	except:
		return JsonResponse({ 'status': 'KO' })

def close_door(request, pin):

	try:
		#GPIO.output(pin, False)
		return JsonResponse({ 'status': 'OK' })
	except:
		return JsonResponse({ 'status': 'KO' })
