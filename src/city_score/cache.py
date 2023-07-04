from diskcache import Cache
import os

path = os.path.dirname(os.path.abspath(__file__))
cache_path = os.path.join(path, 'cache')
cache = Cache(cache_path)