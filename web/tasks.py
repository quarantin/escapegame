# -*- coding: utf-8 -*-

from django.core.management import call_command

from background_task import background

from escapegame import libraspi


@background(schedule=0)
def cube_control(action, pin):
	call_command('clear-completed-tasks')
	return libraspi.cube_control(action, pin)
