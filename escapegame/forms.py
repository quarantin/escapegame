# -*- coding: utf-8 -*-

from django.forms import ValidationError

from constance import config


def __validate_hostname(key, hostname):
	if not hostname.endswith(config.MASTER_TLD):
		raise ValidationError([{
			'id_%s' % key: 'Hostnames must have the `%s` prefix.' % config.MASTER_TLD,
		}])

def validate_hostname(hostname):
	return __validate_hostname('HOSTNAME', hostname)

def validate_master_hostname(hostname):
	return __validate_hostname('MASTER_HOSTNAME', hostname)
