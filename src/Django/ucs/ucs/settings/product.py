from .base import *

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'UCS',
        'USER': 'root',
        'PASSWORD': os.environ['MYSQL_ROOT_PASSWORD'],
        'HOST': 'db',
        'PORT': '3306',
    }
}
