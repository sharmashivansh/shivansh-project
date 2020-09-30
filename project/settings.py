

import configparser
import os

import configparser
import os
import pymysql



pymysql.install_as_MySQLdb()



# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR_SETTING = BASE_DIR + '/project/setting_ini/setting.ini'

config = configparser.ConfigParser()

config.read(BASE_DIR_SETTING)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY =  '#iesb=6!-!3_ys4+j@!9=b*27lkg@w%+*7haak1=wj+@*53h$$'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

AUTH_USER_MODEL = "accounts.User"

# Application definition

INSTALLED_APPS = [
    'jet.dashboard',
    'jet',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'django.contrib.sites',
   
    'django.contrib.flatpages',
    "accounts",
   
    'api',
   
    'inline_actions',
    'ckeditor',
    'ckeditor_uploader',
    # 'channels',
 

]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        'rest_framework.authentication.TokenAuthentication',
    ],
   
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    'social_django.middleware.SocialAuthExceptionMiddleware'
]
#
# SESSION_EXPIRE_AT_BROWSER_CLOSE = True
# SESSION_FILE_PATH = os.getenv("HOME") + '/sessions'

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n'
            ],
        },
    },
]

# WSGI_APPLICATION = 'project.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',

        'NAME': 'shivansh_project',
        'USER': 'root',
        'PASSWORD': '',

        'HOST': 'localhost',
        "PORT": '3306',
        "CONN_MAX_AGE": 600
    }
}





LOGIN_URL = "/accounts/login/"
LOGOUT_REDIRECT_URL = "/"

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    #     {
    #         'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    #     },
    #     {
    #         'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    #     },
    #     {
    #         'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    #     },
    #     {
    #         'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    #     },
]

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

SITE_ID = 1

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'static/')


if not DEBUG:
    STATICFILES_DIRS = (
        os.path.join(BASE_DIR, "static", "admin"),
    )

    STATIC_ROOT = os.path.join(BASE_DIR, 'static')
else:

    STATICFILES_DIRS = (
        os.path.join(BASE_DIR, "static", "admin"),
        os.path.join(BASE_DIR, 'static'),
    )
JET_THEMES = [
    {
        'theme': 'default',  # theme folder name
        'color': '#47bac1',  # color of the theme's button in user menu
        'title': 'Default'  # theme title
    },
    {
        'theme': 'green',
        'color': '#44b78b',
        'title': 'Green'
    },
    {
        'theme': 'light-green',
        'color': '#2faa60',
        'title': 'Light Green'
    },
    {
        'theme': 'light-violet',
        'color': '#a464c4',
        'title': 'Light Violet'
    },
    {
        'theme': 'light-blue',
        'color': '#5EADDE',
        'title': 'Light Blue'
    },
    {
        'theme': 'light-gray',
        'color': '#222',
        'title': 'Light Gray'
    }

]



JET_SIDE_MENU_COMPACT = True

AUTH_USER_MODEL = "accounts.User"

# JET_CHANGE_FORM_SIBLING_LINKS = True
CKEDITOR_UPLOAD_PATH = 'uploads/'
CKEDITOR_CONFIGS = {
    'default': {
        'width': 850,
        'height': 350,
        'filebrowserWindowWidth': 975,
        'filebrowserWindowHeight': 550,
    },
    'small': {
        'width': 850,
        'height': 200,
        'filebrowserWindowWidth': 975,
        'filebrowserWindowHeight': 550,
    },
}



API_PATH = "/api/"
DATECHECK = "2020-04-27"
