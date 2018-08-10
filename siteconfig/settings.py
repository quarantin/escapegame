# -*- coding: utf-8 -*-

"""
Django settings for escapegame project.

Generated by 'django-admin startproject' using Django 2.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os, socket

DEFAULT_MASTER_HOSTNAME = 'escapegame.local'

IS_MASTER = ('%s.local' % socket.gethostname() == DEFAULT_MASTER_HOSTNAME)

RUNNING_ON_PI = ' '.join(os.uname()).strip().endswith('armv7l')

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'l7z2w=efd90^)1gi6a$u$^ohl&tnc=*aby*vr5z5)^-22^voh)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
	'127.0.0.1',
	'localhost',
	'%s.local' % socket.gethostname(),
]


# Application definition

INSTALLED_APPS = [
	'api',
	'web',
	'jsonexport',
	'escapegame',
	'corsheaders',
	'background_task',
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'constance',
	'constance.backends.database',
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

WSGI_APPLICATION = 'siteconfig.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASE_MYSQL = {
	'ENGINE': 'django.db.backends.mysql',
	'NAME': 'escapegame',
	'USER': 'escapegame',
	'PASSWORD': 'escapegame',
	'HOST': 'localhost',
	'OPTIONS': {
		'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
	},
}

DATABASE_SQLITE3 = {
	'ENGINE': 'django.db.backends.sqlite3',
	'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
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

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATICFILES_DIRS = [
	os.path.join(BASE_DIR, "siteconfig", "static"),
]

HOME = os.environ.get('HOME') or '/home/pi'
MEDIA_ROOT = os.path.join(HOME, 'media')
MEDIA_URL = '/media/'

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
	'REQUEST_TIMEOUT': (3, 'The default network timeout for requests.'),
	'IS_MASTER': (IS_MASTER, 'Whether this is the master host.'),
	'IS_SLAVE': (not IS_MASTER, 'Whether this is a slave host.'),
	'MASTER_HOSTNAME': (DEFAULT_MASTER_HOSTNAME, 'The domain name of the Raspberry Pi acting as master.'),
	'MASTER_PORT': (80, 'The TCP port of the Raspberry Pi acting as master.'),
	'UPLOAD_PATH': ('uploads', 'The directory to upload user files, images, etc.', 'text_field'),
	'VIDEO_PATH': ('/opt/vc/src/hello_pi/hello_video', 'The directory containing the videos.', 'text_field'),
	'VIDEO_PLAYER': (RUNNING_ON_PI and '/usr/bin/omxplayer' or '/usr/bin/mpv', 'The path of the executable to display videos.', 'text_field'),
	'RUNNING_ON_PI': (RUNNING_ON_PI, 'True if this application is running on a Raspberry PI, false otherwise.'),
}

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = False

#CORS_ORIGIN_WHITELIST = [
#	'.local',
#]

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
