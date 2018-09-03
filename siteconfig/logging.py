# -*- coding: utf-8 -*-

"""
LOGGING = {
	'version': 1,
	'disable_existing_loggers': False,
	'formatters': {
		'default': {
			'format': '%(levelname)s %(asctime)s %(module)s %(message)s'
		},
	},
	'handlers': {
		'console':{
			'level':'DEBUG',
			'class':'logging.StreamHandler',
			'formatter': 'default',
		},
		'logfile': {
			'level':'DEBUG',
			'class':'logging.FileHandler',
			'formatter': 'default',
			'filename': BASE_DIR + "/django-service.log",
		},
		'logfile_tasks': {
			'level':'DEBUG',
			'class':'logging.FileHandler',
			'formatter': 'default',
			'filename': BASE_DIR + "/django-background-tasks.log",
		},
		'logfile_db': {
			'level':'DEBUG',
			'class':'logging.FileHandler',
			'formatter': 'default',
			'filename': BASE_DIR + "/django-debug-database.log",
		},
	},
	'loggers': {
		'django.db.backends': {
			'handlers': [ 'logfile_db' ],
			'level': 'WARN',
			'propagate': True,
		},
		'django': {
			'handlers':[ 'logfile', 'console' ],
			'level':'INFO',
			'propagate': True,
		},
		'escapegame': {
			'handlers': [ 'logfile', 'console' ],
			'level': 'DEBUG',
			'propagate': True,
		},
		'escapegame.tasks': {
			'handlers': [ 'logfile_tasks', 'console' ],
			'level': 'DEBUG',
			'propagate': True,
		},
	}
}
"""
