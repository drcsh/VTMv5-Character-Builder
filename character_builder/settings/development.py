from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'u#ml9#bo-&s5j%sxx5yync=xtj+%7xrjnzh$q$#d1c%1@xeclb'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
