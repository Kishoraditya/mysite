"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 4.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/


# Application definition

INSTALLED_APPS = [
    "blog",
    "scraper",
    "userauth",
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    "django_countries",
    "widget_tweaks",
    "wagtailcodeblock",
    "wagtailmetadata",
    "debug_toolbar",
    "flex",
    "streams",
    "site_settings",
    "subscribers",
    "menus",
    "contact",
    "home",
    "search",
    "captcha",
    "wagtailcaptcha",
    "rest_framework",
    "core",
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.contrib.settings",
    "wagtail.contrib.modeladmin",
    "wagtail.contrib.routable_page",
    "wagtail.contrib.sitemaps",
    "wagtail.contrib.styleguide",
    "wagtail.embeds",
    "wagtail.sites",
    'wagtail.locales',
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.search",
    "wagtail.admin",
    "wagtail",
    "wagtail.api.v2",
    "modelcluster",
    "taggit",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.contrib.sitemaps",
]

MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    'django.middleware.locale.LocaleMiddleware',
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = "mysite.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(PROJECT_DIR, "templates"),
            os.path.join(BASE_DIR, 'userauth/templates/userauth/'),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                'blog.amp_context_processors.amp',
                'django.template.context_processors.i18n',
                "wagtail.contrib.settings.context_processors.settings",
            ],
        },
    },
]

WSGI_APPLICATION = "mysite.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

#DATABASES = {
#    "default": {
#        "ENGINE": "django.db.backends.sqlite3",
#        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
#    }
#}
#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.postgresql',
#        'NAME': 'db_name',
#        'USER': 'username',
#        'PASSWORD': 'password',
#        'HOST': '127.0.0.1',
#        'PORT': '5432',
#    }
#}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/
INTERNAL_IPS = ("127.0.0.1", "172.17.0.1")
LANGUAGE_CODE = "en-us"

#LOCALE_PATHS = (os.path.join(BASE_DIR, 'locale'),)

TIME_ZONE = "UTC"

USE_I18N = True
WAGTAIL_I18N_ENABLED = True
USE_L10N = True

USE_TZ = True
LANGUAGES = [
    ('en-GB', "English (Great Britain)"),
    ('en-US', "English (United States)"),
    ('en-CA', "English (Canada)"),
    ('fr-FR', "French (France)"),
    ('fr-CA', "French (Canada)"),
]

LANGUAGE_CODE = 'en'
#LANGUAGES = [
#    ('en', 'English'),
#    ('fr', 'Français'),
#    ('nl', 'Nederlands'),
#]


WAGTAIL_CONTENT_LANGUAGES = [
    ('en-GB', "English"),
    ('fr-FR', "French"),
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

STATICFILES_DIRS = [
    os.path.join(PROJECT_DIR, "static"),
]

# ManifestStaticFilesStorage is recommended in production, to prevent outdated
# JavaScript / CSS assets being served from cache (e.g. after a Wagtail upgrade).
# See https://docs.djangoproject.com/en/4.2/ref/contrib/staticfiles/#manifeststaticfilesstorage
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"

STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = "/static/"

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"


# Wagtail settings

WAGTAIL_SITE_NAME = "mysite"
AUTH_USER_MODEL = 'userauth.CustomUser'
WAGTAIL_USER_CREATION_FORM = 'userauth.forms.WagtailUserCreationForm'
WAGTAIL_USER_EDIT_FORM = 'userauth.forms.WagtailUserEditForm'
WAGTAIL_USER_CUSTOM_FIELDS = ['display_name', 'date_of_birth', 'address1', 'address2', 'zip_code', 'city', 'country', 'mobile_phone', 'additional_information', 'photo',]
# Search
# https://docs.wagtail.org/en/stable/topics/search/backends.html
WAGTAILSEARCH_BACKENDS = {
    "default": {
        "BACKEND": "wagtail.search.backends.database",
    }
}

# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
WAGTAILADMIN_BASE_URL = "http://thisisthedomainwagtail.com"

#allauth settings

AUTHENTICATION_BACKENDS = (
    
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",

    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
    
)

SITE_ID = 1

ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_USERNAME_REQUIRED = False

ACCOUNT_SIGNUP_FORM_CLASS = 'userauth.forms.SignupForm'

WAGTAIL_CODE_BLOCK_THEME = None
WAGTAIL_CODE_BLOCK_LANGUAGES = (
    ('bash', 'Bash/Shell'),
    ('css', 'CSS'),
    ('html', 'HTML'),
    ('javascript', 'Javascript'),
    ('json', 'JSON'),
    ('python', 'Python'),
    ('sql', 'SQL'),
    ('yaml', 'YAML'),
    ('c', 'C'),
    ('cpp', 'C++'),
    ('dart', 'Dart'),
    ('docker', 'Docker'),
    ('go', 'Go'),
    ('graphql', 'GraphQL'),
    ('rust', 'Rust'),
    ('solidity', 'Solidity (Ethereum)'),
    ('typescript', 'TypeScript'),
)

# Recaptcha settings
# This key only allows localhost. For production, you'll want your own API keys.
# You can get Recaptcha API key from google.com/recaptcha
RECAPTCHA_PUBLIC_KEY = "6LcNrZcUAAAAAADyWEJTIOXKr6x-8POg3Iqp8rEM"
RECAPTCHA_PRIVATE_KEY = "6LcNrZcUAAAAAPISF06kecWBC4EJPXy2uo_penMC"
NOCAPTCHA = True


#LOGIN_URL = '/login/'
#LOGIN_REDIRECT_URL = '/'
#ACCOUNT_AUTHENTICATION_METHOD = "username_email"
#ACCOUNT_CONFIRM_EMAIL_ON_GET = True
#ACCOUNT_EMAIL_REQUIRED = True
#ACCOUNT_EMAIL_VERIFICATION = "mandatory"
#ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
#ACCOUNT_LOGOUT_ON_GET = True
#ACCOUNT_LOGIN_ON_PASSWORD_RESET = True
#ACCOUNT_LOGOUT_REDIRECT_URL = '/login/'
#ACCOUNT_PRESERVE_USERNAME_CASING = False
#ACCOUNT_SESSION_REMEMBER = True
#ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = False
#ACCOUNT_USERNAME_BLACKLIST = ["kalob", "admin", "god"]
#ACCOUNT_USERNAME_MIN_LENGTH = 2

