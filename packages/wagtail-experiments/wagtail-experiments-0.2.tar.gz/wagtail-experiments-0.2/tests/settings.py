from __future__ import absolute_import, unicode_literals

import os
import django

from wagtail import VERSION as WAGTAIL_VERSION

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DATABASE_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': os.environ.get('DATABASE_NAME', 'wagtail_experiments'),
        'USER': os.environ.get('DATABASE_USER', None),
        'PASSWORD': os.environ.get('DATABASE_PASS', None),
        'HOST': os.environ.get('DATABASE_HOST', None),

        'TEST': {
            'NAME': os.environ.get('DATABASE_NAME', None),
        }
    }
}


SECRET_KEY = 'not needed'

ROOT_URLCONF = 'tests.urls'

STATIC_URL = '/static/'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

USE_TZ = True

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
            ],
            'debug': True,
        },
    },
]

if django.VERSION >= (1, 10):
    MIDDLEWARE = [
        'django.middleware.common.CommonMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]

    if WAGTAIL_VERSION < (2, 0):
        MIDDLEWARE.append('wagtail.wagtailcore.middleware.SiteMiddleware')
    else:
        MIDDLEWARE.append('wagtail.core.middleware.SiteMiddleware')

else:
    MIDDLEWARE_CLASSES = (
        'django.middleware.common.CommonMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',

        'wagtail.wagtailcore.middleware.SiteMiddleware',
    )

if WAGTAIL_VERSION < (2, 0):
    INSTALLED_APPS = (
        'experiments',
        'tests',

        'wagtail.contrib.modeladmin',
        'wagtail.wagtailsearch',
        'wagtail.wagtailsites',
        'wagtail.wagtailusers',
        'wagtail.wagtailimages',
        'wagtail.wagtaildocs',
        'wagtail.wagtailadmin',
        'wagtail.wagtailcore',

        'taggit',

        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
    )
else:
    INSTALLED_APPS = (
        'experiments',
        'tests',

        'wagtail.contrib.modeladmin',
        'wagtail.search',
        'wagtail.sites',
        'wagtail.users',
        'wagtail.images',
        'wagtail.documents',
        'wagtail.admin',
        'wagtail.core',

        'taggit',

        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
    )

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',  # don't use the intentionally slow default password hasher
)

WAGTAIL_SITE_NAME = 'wagtail-experiments test'
