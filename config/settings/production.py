import os

from .base import *


ALLOWED_HOSTS = ['mintama.work']

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mintama_db',
        'USER': os.environ.get('MINTAMA_DB_USER'),
        'PASSWORD': os.environ.get('MINTAMA_DB_PASSWORD'),
        'HOST': os.environ.get('MINTAMA_DB_HOST'),
        'PORT': 3306,
        'TEST': {
             'NAME': 'test_mintama_db'
         }
    }
}

AWS_ACCESS_KEY_ID = os.environ.get('MINTAMA_AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('MINTAMA_AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = 'mintama-bucket'
AWS_S3_ALTERNATE_DOMAIN_NAME = 'static.mintama.work'
AWS_S3_CUSTOM_DOMAIN = AWS_S3_ALTERNATE_DOMAIN_NAME
#AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_LOCATION = 'static'
AWS_DEFAULT_ACL = None
STATIC_URL = 'https://%s/%s/' % (AWS_S3_ALTERNATE_DOMAIN_NAME, AWS_LOCATION)
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_FILE_STORAGE = 'localupload.storage_backends.MediaStorage'