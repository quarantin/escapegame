from django.http import JsonResponse

def reset_challenge(request, challenge):
	return JsonResponse({ 'status': 'OK' })

def solve_challenge(request, challenge):
	return JsonResponse({ 'status': 'OK' })

def status_challenge(request, challenge):
	return JsonResponse({ 'status': 'OK' })
