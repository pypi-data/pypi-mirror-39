try:
    from django.core.cache import cache
except ImportError:
    class CacheObject(dict):
        def set(self, key, value, timeout=None):
            self[key] = value

    cache = CacheObject()


__all__ = ['cache']
