from background_task import background

from escapegame import libraspi


@background(schedule=0)
def cube_control(action, pin):
	return libraspi.cube_control(action, pin)
