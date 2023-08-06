# -*- coding: utf-8 -*-
import os

BASE_DIR = os.getenv('aristotlemdr__BASE_DIR', os.path.dirname(os.path.dirname(__file__)))
SECRET_KEY = os.getenv('aristotlemdr__SECRET_KEY', "OVERRIDE_THIS_IN_PRODUCTION")
STATIC_ROOT = os.getenv('aristotlemdr__STATIC_ROOT', os.path.join(BASE_DIR, "static"))
MEDIA_ROOT = os.getenv('aristotlemdr__MEDIA_ROOT', os.path.join(BASE_DIR, "media"))

# Non overridable base dirs
MDR_BASE_DIR = os.path.dirname(__file__)
# This is only used in development
REPO_BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(MDR_BASE_DIR)))

TEMPLATES_DIRS = [os.path.join(BASE_DIR, 'templates')]
FIXTURES_DIRS = [os.path.join(MDR_BASE_DIR, 'fixtures')]

# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
# This provides for quick easy set up, but should be changed to a production
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'pos.db3'),
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(BASE_DIR, 'caches', 'aristotle-mdr-cache'),
    },
    'aristotle-mdr-invitations': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(BASE_DIR, 'caches', 'aristotle-mdr-invitations'),
        'TIMEOUT': 60 * 60 * 24 * 7,  # sec * min * hours * days
    }
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': TEMPLATES_DIRS,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.request',
                'django.template.context_processors.static',
                'aristotle_mdr.context_processors.settings',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

MEDIA_URL = '/media/'
CKEDITOR_UPLOAD_PATH = 'uploads/'


# Required for admindocs, see: https://code.djangoproject.com/ticket/21386
SITE_ID=None

# This gets called because of the DataElementConcept.property attribute.
# We can resolve this by explicitly adding the parent pointer field, to squash Error E006
# But this will only work for Django 1.10 or above, so we wait until the 1.11 stream
# See: https://code.djangoproject.com/ticket/28563
# Archive: http://archive.is/Zpgru
# _concept_ptr = models.OneToOneField(
#     _concept,
#     on_delete=models.CASCADE,
#     parent_link=True,
#     related_name='property_subclass',
# )

# Not sure how to resolve these yet.

SILENCED_SYSTEM_CHECKS = [
    'models.E006',  # This gets called because of the DataElementConcept.property attribute.
    'models.E023',  # This gets called because we named a model with an underscore
]

ALLOWED_HOSTS: list = []

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'
ARISTOTLE_ASYNC_SIGNALS = os.getenv('ARISTOTLE_ASYNC_SIGNALS', False) == "True"

INSTALLED_APPS = (
    'aristotle_bg_workers',
    'aristotle_mdr.contrib.reviews',
    'aristotle_mdr',
    'aristotle_mdr.contrib.generic',
    'aristotle_mdr.contrib.help',
    'aristotle_mdr.contrib.slots',
    'aristotle_mdr.contrib.identifiers',
    'aristotle_mdr.contrib.browse',
    'aristotle_mdr.contrib.autocomplete',
    'aristotle_mdr.contrib.favourites',
    'aristotle_mdr.contrib.view_history',
    'aristotle_mdr.contrib.user_management',
    'aristotle_mdr.contrib.issues',
    'aristotle_mdr.contrib.publishing',
    'aristotle_mdr.contrib.custom_fields',

    'dal',
    'dal_select2',

    'user_sessions',

    'haystack',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',  # Here for easyaudit compatibility
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    'ckeditor',
    'ckeditor_uploader',

    'bootstrap3',
    'reversion',  # https://github.com/etianen/django-reversion
    'reversion_compare',  # https://github.com/jedie/django-reversion-compare

    'notifications',
    'organizations',

    'constrainedfilefield',
    'django_celery_results',

    'webpack_loader',

    'aristotle_mdr_api',
    'aristotle_mdr_api.token_auth',
    'rest_framework',
    'rest_framework_swagger',
    'django_filters',

    'django_jsonforms',
    'missing'

)

USE_L10N = True
USE_TZ = True
USE_I18N = True

MIDDLEWARE = [
    'user_sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'aristotle_mdr.contrib.redirect.middleware.RedirectMiddleware',


    # 'reversion.middleware.RevisionMiddleware',
]

SESSION_ENGINE = 'user_sessions.backends.db'

ROOT_URLCONF = 'aristotle_mdr.urls'
LOGIN_REDIRECT_URL = '/account/home'
LOGOUT_REDIRECT_URL = '/home'
LOGIN_URL = '/login'
LOGOUT_URL = '/logout'

STATIC_URL = '/static/'
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
STATICFILES_DIRS = [
    os.path.join(REPO_BASE_DIR, 'assets/dist')
]

ADMIN_MEDIA_PREFIX = '/static/admin/'

BOOTSTRAP3 = {
    # The Bootstrap base URL
    'base_url': '/static/aristotle_mdr/bootstrap/',
}

ADD_REVERSION_ADMIN = True

# We need this to make sure users can see all extensions.
AUTHENTICATION_BACKENDS = ('aristotle_mdr.backends.AristotleBackend',)

# ARISTOTLE_SETTINGS_STRICT_MODE = True

ARISTOTLE_SETTINGS = {
    'SEPARATORS': {
        'DataElement': ', ',
        'DataElementConcept': u'–'
    },
    'SITE_NAME': 'Default Site Name',  # 'The main title for the site.'
    'SITE_BRAND': 'aristotle_mdr/images/aristotle_small.png',  # URL for the Site-wide logo
    'SITE_INTRO': 'Use Default Site Name to search for metadata...',  # 'Intro text use on the home page as a prompt for users.'
    'SITE_DESCRIPTION': 'About this site',  # 'The main title for the site.'
    'CONTENT_EXTENSIONS': [],
    'PDF_PAGE_SIZE': 'A4',
    'WORKGROUP_CHANGES': [],  # ['admin'] # or manager or submitter,
    'BULK_ACTIONS': [
        'aristotle_mdr.forms.bulk_actions.AddFavouriteForm',
        'aristotle_mdr.forms.bulk_actions.RemoveFavouriteForm',
        'aristotle_mdr.forms.bulk_actions.ChangeStateForm',
        'aristotle_mdr.forms.bulk_actions.ChangeWorkgroupForm',
        # 'aristotle_mdr.forms.bulk_actions.RequestReviewForm',
        'aristotle_mdr.forms.bulk_actions.BulkDownloadForm',
        'aristotle_mdr.contrib.reviews.forms.RequestReviewBulkActionForm',
    ],
    'DASHBOARD_ADDONS': [],
    'METADATA_CREATION_WIZARDS': [
        {
            'app_label': 'aristotle_mdr',
            'model': 'DataElement',
            'class': 'aristotle_mdr.views.wizards.DataElementWizard',
            'link': 'create/wizard/aristotle_mdr/dataelement',
        },
        {
            'app_label': 'aristotle_mdr',
            'model': 'DataElementConcept',
            'class': 'aristotle_mdr.views.wizards.DataElementConceptWizard',
            'link': 'create/wizard/aristotle_mdr/dataelementconcept',
        }
    ],
    "DOWNLOADERS": [
        # (fileType, menu, font-awesome-icon, module)
        # ('csv-vd', 'CSV list of values', 'fa-file-excel-o', 'aristotle_mdr', 'CSV downloads for value domain codelists'),
        'aristotle_mdr.downloader.CSVDownloader'
    ],

    # These settings aren't active yet.
    # "USER_EMAIL_RESTRICTIONS": None,
    "USER_VISIBILITY": ['owner', 'workgroup_manager', 'registation_authority_manager']
    # "SIGNUP_OPTION": 'closed', # or 'closed'
    # "GROUPS_CAN_INVITE": 'closed', # or 'closed'

}

CKEDITOR_CONFIGS = {
    'default': {
        # 'toolbar': 'full',
        'toolbar': [
            {'name': 'clipboard', 'items': ['Cut', 'Copy', 'Paste', 'PasteText', '-', 'Undo', 'Redo']},
            {'name': 'basicstyles', 'items': ['Bold', 'Italic', 'Subscript', 'Superscript', '-', 'RemoveFormat']},
            {'name': 'links', 'items': ['Link', 'Unlink']},
            {'name': 'paragraph', 'items': ['NumberedList', 'BulletedList', '-', 'Blockquote']},
            {'name': 'insert', 'items': ['Image', 'Table', 'HorizontalRule', 'SpecialChar']},
            {'name': 'document', 'items': ['Maximize', 'Source']},
        ],
        'width': "",
        "removePlugins": "stylesheetparser",
    },
}

HAYSTACK_SIGNAL_PROCESSOR = 'aristotle_mdr.contrib.help.signals.AristotleHelpSignalProcessor'
# HAYSTACK_SEARCH_RESULTS_PER_PAGE = 10
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'aristotle_mdr.contrib.search_backends.facetted_whoosh.FixedWhooshEngine',
        'PATH': os.path.join(os.path.dirname(__file__), 'whoosh_index'),
        'INCLUDE_SPELLING': True,
    },
}

ORGS_SLUGFIELD = 'autoslug.fields.AutoSlugField'

# User Model
AUTH_USER_MODEL = 'aristotle_mdr_user_management.User'

AUTH_PREFIX = 'django.contrib.auth.password_validation.'
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': AUTH_PREFIX + 'UserAttributeSimilarityValidator',
        'OPTIONS': {
            'user_attributes': ('email', 'full_name', 'short_name')
        },
    },
    # include other password validators here
]

# GeoIP
GEOIP_PATH = os.path.join(BASE_DIR, 'aristotle_mdr/vendor/geoip')

# Webpack loading
WEBPACK_LOADER = {
    'DEFAULT': {
        'CACHE': True,
        'BUNDLE_DIR_NAME': 'bundles/',
        'POLL_INTERVAL': 0.1,
        'STATS_FILE': os.path.join(MDR_BASE_DIR, 'manifests/webpack-stats.json'),
        'TIMEOUT': None,
    }
}

# Django manifest location
MANIFEST_DIR = os.path.join(MDR_BASE_DIR, 'manifests')

# Caching
CACHE_ITEM_PAGE = False

# Sanitization
BLEACH_ALLOWED_TAGS = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'em',
                       'i', 'li', 'ol', 'strong', 'ul', 'table', 'tbody', 'thead',
                       'tr', 'th', 'td', 'img', 'p', 'h1', 'h2', 'h3', 'h4',
                       'h5', 'h6', 'sub', 'sup', 'br', 'u']

BLEACH_ALLOWED_ATTRIBUTES = {
    'a': ['href', 'title', 'class', 'data-aristotle-concept-id'],
    'abbr': ['title'],
    'acronym': ['title'],
    'img': ['src', 'height', 'width', 'alt']
}

# Validators
ARISTOTLE_VALIDATION_RUNNER = 'aristotle_mdr.contrib.validators.runner'
ARISTOTLE_VALIDATION_FILERUNNER_PATH = os.getenv('aristotlemdr__FILE_VALIDATION_RUNNER_PATH', None)

ARISTOTLE_VALIDATORS = {
    'RegexValidator': 'aristotle_mdr.contrib.validators.RegexValidator',
    'StatusValidator': 'aristotle_mdr.contrib.validators.StatusValidator',
    'RelationValidator': 'aristotle_mdr.contrib.validators.RelationValidator',
}

# Serialization
SERIALIZATION_MODULES = {'mdrjson': 'aristotle_mdr_api.serializers.idjson'}

# API
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'aristotle_mdr_api.token_auth.authentication.AristotleTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    )
}
