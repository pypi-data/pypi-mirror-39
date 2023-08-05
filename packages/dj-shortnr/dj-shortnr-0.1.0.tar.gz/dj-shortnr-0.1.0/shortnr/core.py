from .models import UrlIndex



def shorten_url(url):
    obj, created = UrlIndex.objects.get_or_create(url=url)
    
    if obj:
        return obj
    
    raise Exception('cannot shorten url')


def unshorten_url(key):
    return UrlIndex.objects.get(key=key)
