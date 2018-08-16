from django.db import models
from django.utils import timezone
from constance import config
from rest_framework.authtoken.models import Token

from datetime import timedelta


class RestToken(Token):
	host = models.CharField(max_length=255)

	def is_valid(self):
		return not self.has_expired()

	def has_expired(self):
		expire = timezone.localtime(self.created) + timedelta(minutes=config.TOKEN_TIMEOUT)
		return expire < timezone.localtime()

	"""
		Create or get token for host and user.
	"""
	def __generate_token(host, user):
		token, created = RestToken.objects.get_or_create(host=host, user=user)
		expire = timezone.localtime(token.created) + timedelta(minutes=config.TOKEN_TIMEOUT)
		return token, expire

	"""
		Create or get a non-expired token for host and user.
	"""
	def get_token(host, user):
		token, expire = RestToken.__generate_token(host, user)
		if token and token.has_expired():
			token.delete()
			token, expire = RestToken.__generate_token(user)

		return token, expire

	"""
		Check if the supplied token is valid for the host.
	"""
	def is_valid_token(token_id, host):
		try:
			token = RestToken.objects.get(pk=token_id, host=host)
			return token.is_valid()

		except:
			return False
