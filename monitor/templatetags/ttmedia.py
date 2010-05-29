from django.template import Library
from django.utils.encoding import iri_to_uri

register = Library()

def tt_media_prefix():
    """
    Returns the string contained in the setting ADMIN_MEDIA_PREFIX.
    """
    try:
        from monitor import settings
    except ImportError:
        return ''
    return iri_to_uri(settings.SITE_MEDIA)
admin_media_prefix = register.simple_tag(tt_media_prefix)
