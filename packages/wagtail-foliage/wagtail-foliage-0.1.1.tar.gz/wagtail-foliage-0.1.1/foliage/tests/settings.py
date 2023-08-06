from wagtail import VERSION

SECRET_KEY = 'NOTSECRET'

DATABASES = {
    'default': {
        'NAME': 'test.db',
        'ENGINE': 'django.db.backends.sqlite3',
    }
}

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'taggit',
    'foliage.tests.testapp',
)

MIDDLEWARE = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
            ],
        },
    },
]

ROOT_URLCONF = 'foliage.tests.testapp.urls'

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
# Wagtail version-specific settings added below

if VERSION >= (2, 0):
    INSTALLED_APPS += (
        'wagtail.core',
        'wagtail.documents',
        'wagtail.images',
        'wagtail.admin',
        'wagtail.sites',
        'wagtail.users',
    )
    MIDDLEWARE += (
        'wagtail.core.middleware.SiteMiddleware',
    )
else:
    INSTALLED_APPS += (
        'wagtail.wagtailcore',
        'wagtail.wagtaildocs',
        'wagtail.wagtailimages',
        'wagtail.wagtailadmin',
        'wagtail.wagtailsites',
        'wagtail.wagtailusers',
    )
    MIDDLEWARE += (
        'wagtail.wagtailcore.middleware.SiteMiddleware',
    )
