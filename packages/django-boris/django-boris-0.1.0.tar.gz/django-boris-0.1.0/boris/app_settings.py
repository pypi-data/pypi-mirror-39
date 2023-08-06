from django.conf import settings
from django.utils.module_loading import import_string

BORIS_SETTINGS = getattr(settings, 'BORIS', {})


def get_setting(setting_name, default):
    return BORIS_SETTINGS.get(setting_name) or default


ACTIVE_SPIDERS = [
    import_string(spider_path) for spider_path in
    get_setting('SPIDERS', ['boris.spiders.readability.ReadabilitySpider'])
]
