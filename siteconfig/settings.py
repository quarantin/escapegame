# -*- coding: utf-8 -*-

"""
Django settings for escapegame project.

Generated by 'django-admin startproject' using Django 2.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os, imp, socket


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'l7z2w=efd90^)1gi6a$u$^ohl&tnc=*aby*vr5z5)^-22^voh)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Whether we are running on a Raspberry Pi or not
RUNNING_ON_PI = ' '.join(os.uname()).strip().endswith('armv7l')

# Load python code with the extension .py
MASTER_FILE = 'master-hostname.txt'
MASTER = imp.load_source(MASTER_FILE, os.path.join(BASE_DIR, MASTER_FILE))

# Whether we are the master game controller
IS_MASTER = (socket.gethostname() == MASTER.HOSTNAME)

# Build full hostname by appending master hostname with master TLD
MASTER_HOSTNAME = '%s%s' % (MASTER.HOSTNAME, MASTER.TLD)

# My hostname
HOSTNAME = '%s%s' % (socket.gethostname(), MASTER.TLD)

ALLOWED_HOSTS = [
	'127.0.0.1',
	'localhost',
	HOSTNAME,
]


# Application definition

INSTALLED_APPS = [
	'api',
	'web',
	'escapegame',
	'controllers',
	'multimedia',
	'jsonexport',
	'corsheaders',
	'background_task',
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.messages',
	'django.contrib.sessions',
	'django.contrib.staticfiles',
	'channels',
	'constance',
	'constance.backends.database',
	'django_extensions',
	'rest_framework.authtoken',
	'ws4redis',
]

MIDDLEWARE = [
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'corsheaders.middleware.CorsMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

if IS_MASTER:
	ROOT_URLCONF = 'siteconfig.urls'
else:
	ROOT_URLCONF = 'siteconfig.slave_urls'

TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [
			os.path.join(BASE_DIR, 'jsonexport', 'templates'),
			os.path.join(BASE_DIR, 'siteconfig', 'templates'),
			os.path.join(BASE_DIR, 'web', 'templates'),
		],
		'APP_DIRS': True,
		'OPTIONS': {
			'context_processors': [
				'django.template.context_processors.debug',
				'django.template.context_processors.request',
				'django.contrib.auth.context_processors.auth',
				'django.contrib.messages.context_processors.messages',
				'ws4redis.context_processors.default',
			],
			'libraries': {
				'customtags': 'siteconfig.templatetags.customtags',
			},
		},
	},
]

TEMPLATES_CONTEXT_PROCESSOR = [
	'django.template.context_processors.request',
]


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASE_MYSQL = {
	'ENGINE': 'django.db.backends.mysql',
	'NAME': 'escapegame',
	'USER': 'escapegame',
	'PASSWORD': 'escapegame',
	'HOST': IS_MASTER and 'localhost' or MASTER_HOSTNAME,
	'OPTIONS': {
		'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
	},
}

DATABASES = {
	'default': 	DATABASE_MYSQL,
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
	{
		'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
	},
	{
		'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
	},
	{
		'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
	},
	{
		'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
	},
]


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Paris'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Media files (Uploaded)

MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
MEDIA_URL = '/media/'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
STATIC_URL = '/static/'

STATICFILES_DIRS = (os.path.join(BASE_DIR, 'siteconfig', 'static'),)


# The following directive is required during development and ignored in production environments.
# It overrides Django’s internal main loop and adds a URL dispatcher in front of the request handler.
# https://django-websocket-redis.readthedocs.io/en/latest/installation.html#configuration

WSGI_APPLICATION = 'ws4redis.django_runserver.application'


# Websocket URLs
# https://django-websocket-redis.readthedocs.io/en/latest/installation.html#configuration

WEBSOCKET_URL = '/ws/'


# Use Redis as the session engine
# https://django-websocket-redis.readthedocs.io/en/latest/installation.html#replace-memcached-with-redis

SESSION_ENGINE = 'redis_sessions.session'
SESSION_REDIS_PREFIX = 'session'


# Channels

CHANNEL_LAYER = {
	"default": {
		"BACKEND": "channels_redis.core.RedisChannelLayer",
		"CONFIG": {
			"hosts": [("127.0.0.1", 6379)],
		},
		"ROUTING": "siteconfig.routing.channel_routing",
	},
}


# Constance settings

CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'

CONSTANCE_ADDITIONAL_FIELDS = {
	'text_field': [
		'django.forms.CharField',
		{
			'widget': 'django.forms.TextInput',
		}
	],
}

CONSTANCE_CONFIG = {
	'IS_MASTER': (IS_MASTER, 'Whether this is the master host.'),
	'IS_SLAVE': (not IS_MASTER, 'Whether this is a slave host.'),
	'TLD': (MASTER.TLD, 'The TLD (Top-Level-Domain) of this host.', 'text_field'),
	'HOSTNAME': (HOSTNAME, 'The full domain name of this host.', 'test_field'),
	'MASTER_TLD': (MASTER.TLD, 'The TLD (Top-Level-Domain) of the Raspberry Pi acting as master.', 'text_field'),
	'MASTER_HOSTNAME_SHORT': (MASTER.HOSTNAME, 'The hostname name of the Raspberry Pi acting as master.', 'text_field'),
	'MASTER_HOSTNAME': (MASTER_HOSTNAME, 'The full domain name of the host acting as master.', 'text_field'),
	'MASTER_PORT': (80, 'The TCP port of the Raspberry Pi acting as master.'),
	'REQUEST_TIMEOUT': (3, 'The default network timeout for requests, in seconds.'),
	'RUNNING_ON_PI': (RUNNING_ON_PI, 'True if this application is running on a Raspberry PI, false otherwise.'),
	'TOKEN_TIMEOUT': (15, 'The default expiration timeout for authentication tokens, in minutes.'),
	'UPLOAD_IMAGE_PATH': ('uploads/images', 'The directory to upload images.', 'text_field'),
	'UPLOAD_VIDEO_PATH': ('uploads/videos', 'The directory to upload videos.', 'text_field'),
	'VIDEO_PLAYER': (RUNNING_ON_PI and '/usr/bin/omxplayer' or '/usr/bin/mpv', 'The path of the executable to display videos.', 'text_field'),
}


# CORS settings

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = False

#CORS_ORIGIN_WHITELIST = [
#	'.local',
#]

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
