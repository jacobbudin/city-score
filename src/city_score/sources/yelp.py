from ..decorators import criterion, dimension, scorer
from ..source import Source
from ..cache import cache

from yelpapi import YelpAPI
import json

class Yelp(Source):
    def __init__(self, credentials):
        self.__class__.API_KEY = credentials['API_KEY']


@dimension('Yelp "{q}"')
def nearby(city, q="", miles=10, exact=True):
    q = q.lower()
    key = 'yelp-%s-%s-%s-%s' % (str(q.replace(' ', '-')), str(city), str(miles), str(exact))
    count = cache.get(key)
    if count is not None:
        return count
    
    with YelpAPI(Yelp.API_KEY) as yelp_api:
        results = yelp_api.search_query(term=q, location=str(city), radius=miles*1609, limit=50)
        if not exact:
            count = len(results['businesses'])
        else:
            count = 0
            for business in results['businesses']:
                count += len([c for c in business['categories'] if c['title'].lower() == q])

        cache.set(key, count)
        return count
    
    return None

@scorer('Yelp "{q}"')
def nearby_scorer(city, q, lower, upper, miles=10, exact=True):
    count = nearby(city, q=q, miles=miles, exact=exact)

    if count >= upper:
        return 100
    if count >= lower:
        return round(((count - lower) / (upper - lower)) * 100)
    
    return 0