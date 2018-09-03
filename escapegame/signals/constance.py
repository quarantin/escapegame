# -*- coding: utf-8 -*-

from django.dispatch import receiver
from django.forms import ValidationError

from constance.signals import config_updated

from constance import config

from siteconfig.settings import BASE_DIR

import os
import subprocess

def set_hostname(new_hostname):

	hostname, tld = new_hostname.strip().rsplit('.', 1)

	script = os.path.join(BASE_DIR, 'scripts', 'set-hostname.sh')
	subprocess.call([ 'sudo', script, hostname ])

def set_master_hostname(new_hostname):

	hostname, tld = new_hostname.strip().rsplit('.', 1)

	fin = open(os.path.join(BASE_DIR, 'master-hostname.txt'), 'w')
	fin.write("HOSTNAME='%s'\n" % hostname)
	fin.write("TLD='.%s'\n" % tld)
	fin.close()


@receiver(config_updated)
def constance_updated(sender, key, old_value, new_value, **kwargs):

	if key in [ 'HOSTNAME', 'MASTER_HOSTNAME' ]:
		if not new_value.endswith(config.MASTER_TLD):
			raise ValidationError({
				'id_%s' % key: 'Hostnames must have the `%s` suffix.' % config.MASTER_TLD,
            })

	if key == 'HOSTNAME':
		set_hostname(new_value)

	elif key == 'MASTER_HOSTNAME':
		set_master_hostname(new_value)
