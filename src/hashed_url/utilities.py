import urllib
import urlparse
import hashlib
import datetime
import time

from django.conf import settings
# settings = {}

HASH_PARAM = getattr(settings, "HASHED_URL_HASH_PARAM", "_h")
TIME_PARAM = getattr(settings, "HASHED_URL_TIME_PARAM", "_t")

def get_hashed_url(url, valid_until=None):
    valid_until = _as_timestamp(valid_until)
    url_with_hash = append_param(url, TIME_PARAM, valid_until or "")
    url_with_hash = append_param(url_with_hash, HASH_PARAM, get_hash(url, valid_until))
    
    return url_with_hash

def is_valid_url(url):
    parsed = urlparse.urlparse(url)
    query_dict = urlparse.parse_qs(parsed.query)
    
    hash_,  = query_dict.get(HASH_PARAM, (None,)) or (None,)
    valid_until,  = query_dict.get(TIME_PARAM, ("",)) or ("",)
    
    if not hash_:
        return False
    
    if valid_until:
        try:
            valid_until = int(valid_until)
        except ValueError:
            return False
    
    if valid_until < _as_timestamp(datetime.datetime.now()):
        return False
    
    if get_hash(url, valid_until) != hash_:
        return False
    
    return True

def get_hash(url, valid_until=None):
    valid_until = _as_timestamp(valid_until)
    
    # Remove parts of the QS used to make the hash
    url = remove_params(url, [HASH_PARAM, TIME_PARAM])
    
    hash_data = "\0".join((url, str(valid_until or "") or "", settings.SECRET_KEY))
    hash_ = hashlib.sha1(hash_data).hexdigest()
    
    return hash_

def append_param(url, key, value):
    parsed = urlparse.urlparse(url)
    query = urlparse.parse_qsl(parsed.query, keep_blank_values=True)
    query.append((key, value))
    
    parsed_list = list(parsed)
    parsed_list[4] = urllib.urlencode(query)
    del parsed_list[3]
    
    return urlparse.urlunsplit(parsed_list)

def remove_params(url, keys):
    parsed = urlparse.urlparse(url)
    query = urlparse.parse_qsl(parsed.query, keep_blank_values=True)
    
    query = filter(lambda kv: kv[0] not in keys, query)
    
    parsed_list = list(parsed)
    parsed_list[4] = urllib.urlencode(query)
    del parsed_list[3]
    
    return urlparse.urlunsplit(parsed_list)

def _as_timestamp(t):
    if hasattr(t, "timetuple"):
        t = int(time.mktime(t.timetuple()))
    return t