from django.conf import settings

def settings_context(request):
    """
    Context processor that injects Django settings into templates.
    Only includes non-sensitive settings.
    """
    safe_settings = {
        'DEBUG': settings.DEBUG,
        'LANGUAGE_CODE': settings.LANGUAGE_CODE,
        'TIME_ZONE': settings.TIME_ZONE,
        'USE_I18N': settings.USE_I18N,
        'USE_TZ': settings.USE_TZ,
        'STATIC_URL': settings.STATIC_URL,
        'MEDIA_URL': settings.MEDIA_URL,
        'INSTALLED_APPS': settings.INSTALLED_APPS,
        'MIDDLEWARE': settings.MIDDLEWARE,
        'TEMPLATES': [{
            'BACKEND': template['BACKEND'],
            'DIRS': template['DIRS'],
            'APP_DIRS': template['APP_DIRS'],
        } for template in settings.TEMPLATES],
    }
    return {'settings': safe_settings} 