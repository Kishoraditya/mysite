#please rename the file from rm_local.py to local.py and then follow the following instructions
import os
#python3 manage.py shell
#from django.core.management.utils import get_random_secret_key
#get_random_secret_key()
SECRET_KEY = ""
#replace with your db_name, username, and password and cut paste from base.py to local.py
DATABASES = {
    'default': {
        'ENGINE': os.environ.get('SQL_ENGINE', 'django.db.backends.postgresql'),
        'NAME': os.environ.get('SQL_DATABASE','db_name'),
        'USER': os.environ.get('SQL_USER','username'),
        'PASSWORD': os.environ.get('SQL_PASSWORD','password'),
        'HOST': os.environ.get('SQL_HOST','127.0.0.1'),
        'PORT': os.environ.get('SQL_PORT','5432'),
    }
}

# if you have email authentication created
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'yourusername@gmail.com'
EMAIL_HOST_PASSWORD = 'yourpassword'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER