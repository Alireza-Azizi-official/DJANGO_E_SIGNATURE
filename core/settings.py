from pathlib import Path
import environ
import os 

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, 'core', 'secrets.env'))

SECRET_KEY = 'django-insecure-4+dpvms2z*0po%*^l9t0j6r_0@zqhf&9#unr*&i%6_n)w7otwg'
DEBUG = True
ALLOWED_HOSTS = [
    '2967-2-178-211-85.ngrok-free.app',
    '127.0.0.1',       
    'localhost',            
]


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'contracts'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),  
            os.path.join(BASE_DIR, 'templates', 'contracts'),  
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

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

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = 'create_contract'
LOGOUT_REDIRECT_URL = 'home'
LOGIN_URL = 'login'

EMAIL_BACKEND = 'django.core.email.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')

DOCUSIGN_CLIENT_ID = env('DOCUSIGN_CLIENT_ID')
DOCUSIGN_CLIENT_SECRET = env('DOCUSIGN_CLIENT_SECRET')
DOCUSIGN_REDIRECT_URI = env('DOCUSIGN_REDIRECT_URI')
DOCUSIGN_ACCOUNT_ID = env('DOCUSIGN_ACCOUNT_ID')
DOCUSIGN_AUTH_URL = env('DOCUSIGN_AUTH_URL')
DOCUSIGN_TOKEN_URL = env('DOCUSIGN_TOKEN_URL')
DOCUSIGN_ACCESS_TOKEN = env('DOCUSIGN_ACCESS_TOKEN')
DOCUSIGN_USERNAME = env('DOCUSIGN_USERNAME')
DOCUSIGN_PASSWORD = env('DOCUSIGN_PASSWORD')
DOCUSIGN_INTEGRATOR_KEY = env('DOCUSIGN_INTEGRATOR_KEY')
DOCUSIGN_APP_TOKEN =  env('DOCUSIGN_APP_TOKEN')
DOCUSIGN_ROOT_URL = env('DOCUSIGN_ROOT_URL')
DOCUSIGN_TIMEOUT = env('DOCUSIGN_TIMEOUT') 

ANYSIGN = {
    'BACKENDS': {
        'docusign': 'django_docusign.backend.DocuSignBackend',
    },
    'SIGNATURE_TYPE_MODEL': 'django_docusign_demo.models.SignatureType',
    'SIGNATURE_MODEL': 'django_docusign_demo.models.Signature',
    'SIGNER_MODEL': 'django_docusign_demo.models.Signer',
}

CSRF_TRUSTED_ORIGINS = [
    'https://2967-2-178-211-85.ngrok-free.app',  
]

