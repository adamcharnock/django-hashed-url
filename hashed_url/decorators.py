from django.core.exceptions import PermissionDenied

from hashed_url.utilities import is_valid_url

def require_hash_url():
    def decorator(f):
        def wrapper(request, *args, **kwargs):
            url = request.build_absolute_uri()
            if is_valid_url(url):
                return f(request, *args, **kwargs)
            else:
                raise BadHashedUrl("Invalid hashed URL specified")
            
        return wrapper
    
    return decorator

class BadHashedUrl(PermissionDenied): pass