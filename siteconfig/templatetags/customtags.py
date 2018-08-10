from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def basename(value):
	import os
	return os.path.basename(value.strip('/'))

@register.filter
@stringfilter
def path(path, n):
	tokens = path.strip('/').split('/')
	if len(tokens) < n:
		return path

	return '/'.join(tokens[:n])
