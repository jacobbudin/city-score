from ..cache import cache
from ..decorators import criterion, dimension, scorer
from ..source import Source
from html.parser import HTMLParser
import requests

class InputValueAttributeParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.value_attribute = None

    def handle_starttag(self, tag, attrs):
        if tag == "input":
            attrs_dict = dict(attrs)
            if attrs_dict.get("name") == "ResultsCount":
                self.results_count_value = attrs_dict.get("value")

class TrailLink(Source):
    base_url = "https://www.traillink.com/trailsearch"

@criterion("Minimum TrailLink count")
def minimum_trail_count(city, min_count):
    _count = trail_count(city)
    return _count >= min_count

@dimension('TrailLink')
def trail_count(city):
    key = 'traillink-%s' % (str(city))
    count = cache.get(key)
    if count is not None:
        return int(count)
    
    response = requests.get(TrailLink.base_url, params={
        "city": city.name,
        "state": city.state
    })

    if response.status_code == 200:
        parser = InputValueAttributeParser()
        parser.feed(response.text)
        count = parser.results_count_value
        cache.set(key, int(count))
        return int(count)

@scorer('TrailLink')
def trail_count_scorer(city, lower, upper):
    count = trail_count(city)
    if count >= upper:
        return 100
    if count >= lower:
        return round(((count - lower) / (upper - lower)) * 100)
    return 0
