from django.template import Library, Node
from django.template.defaulttags import url
from django.conf import settings

from hashed_url.utilities import get_hashed_url

register = Library()

class UrlNodeWrapper(Node):
    def __init__(self, baseObject):
        baseObject.baseObject = baseObject
        self.__class__ = type(baseObject.__class__.__name__,
                              (self.__class__, baseObject.__class__),
                              {})
        self.__dict__ = baseObject.__dict__

    def render(self, context):
        url = self.baseObject.render(context)
        
        # Make the URL absolute
        root_url = getattr(settings, "ROOT_URL", None)
        if not root_url:
            raise ValueError("Config setting 'ROOT_URL' must be defined, and must be the sites root url")
        
        root_url = root_url.rstrip("/")
        url = get_hashed_url(root_url + url)
        
        return url
        

@register.tag
def hashedurl(*args, **kwargs):
    node = url(*args, **kwargs)
    return UrlNodeWrapper(node) 