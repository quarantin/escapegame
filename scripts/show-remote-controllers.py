# *-* coding: utf-8 *-*

from controllers.models import RaspberryPi


raspis = RaspberryPi.objects.all()
for raspi in raspis:
	print(raspi.hostname)
