import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-ne*-in^bkh%-8z$vj5kgl!^_s54-&aqe9919*1*)8lwv#pb4!f'

ALLOWED_HOSTS = []


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'ninja_extra',
    'ninja_jwt.token_blacklist',
    
    'account.apps.AccountConfig'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
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
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'
ASGI_APPLICATION = 'core.asgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB'),
        'USER': os.environ.get('POSTGRES_USER'),  
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': os.environ.get('POSTGRES_HOST'),                
        'PORT': os.environ.get('POSTGRES_PORT'),             
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

AUTH_USER_MODEL = 'account.User'

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STORAGES = {

    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "session"

CACHES = {
    "session": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://accountredis:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "SOCKET_CONNECT_TIMEOUT": 2,  # seconds
            "SOCKET_TIMEOUT": 2,          # seconds
            "IGNORE_EXCEPTIONS": True,     # Prevents cache failures from breaking requests
            "PICKLE_VERSION": 4,          # Faster serialization
            "COMPRESSOR": "django_redis.compressors.zlib.ZlibCompressor",
            "COMPRESS_LEVEL": 3,          # Balance between CPU and size
        }
    },
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://accountredis:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "SOCKET_CONNECT_TIMEOUT": 2,  # seconds
            "SOCKET_TIMEOUT": 2,          # seconds
            "IGNORE_EXCEPTIONS": True,     # Prevents cache failures from breaking requests
            "PICKLE_VERSION": 4,          # Faster serialization
            "COMPRESSOR": "django_redis.compressors.zlib.ZlibCompressor",
            "COMPRESS_LEVEL": 3,          # Balance between CPU and size
        }
    }
}
SESSION_COOKIE_AGE = 3600
SESSION_COOKIE_NAME = 'admin_sessionid'  # Rename to avoid conflicts with APIs
SESSION_COOKIE_PATH = '/admin/'
# Important for session sharing
# SESSION_COOKIE_DOMAIN = ".yourdomain.com"  # For cross-subdomain
# CSRF_COOKIE_DOMAIN = ".yourdomain.com"

CUSTOM_VALIDATION_MESSAGES = {
    'Input should be 0, 1 or 2': 'نقش غیرقابل قبول است!',
    'Field required': 'نمی تواند خالی باشد',
    'String should have at least 4 characters': 'حداقل 4 حرف نیاز است',
    'String should have at most 64 characters': 'حداکثر 64 حرف می توانید وارد کنید',
    'Input should be greater than 0': 'مقدار ورودی باید بزرگتر از 0 باشد',
    'Input should be less than or equal to 20': 'این مقدار نمی تواند بزرگتر از 20 باشد',
    'Decimal input should have no more than 2 digits in total': 'مقدار مورد نظر می تواند بین 0 و 9 با یک رقم ممیز باشد'
}