from ..cache import cache
from ..decorators import dimension, scorer
from ..source import Source
from html.parser import HTMLParser
import requests

class TrailLinkMilesParser(HTMLParser):
    def __init__(self, class_names):
        super().__init__()
        self.class_names = class_names
        self.capture_data = False
        self.total_trail_miles = 0

    def handle_starttag(self, tag, attrs):
        if tag == "span":
            for attr in attrs:
                if attr[0] == "itemprop" and attr[1] == "distance":
                    self.capture_data = True

    def handle_data(self, data):
        if self.capture_data:
            self.total_trail_miles += float(data.split()[0])

    def handle_endtag(self, tag):
        if tag == "span" and self.capture_data:
            self.capture_data = False


class TrailLink(Source):
    base_url = "https://www.traillink.com/trailsearch"

@dimension('TrailLink')
def trail_total_miles(city):
    key = 'traillink-%s' % (str(city))
    count = cache.get(key)
    if count is not None:
        return count
    
    response = requests.get(TrailLink.base_url, params={
        "city": city.name,
        "state": city.state
    })

    if response.status_code == 200:
        parser = TrailLinkMilesParser()
        parser.feed(response.text)
        count = int(parser.total_trail_miles)
        cache.set(key, count)
        return count

@scorer('TrailLink')
def trail_total_miles_scorer(city, lower, upper):
    count = trail_total_miles(city)
    if count >= upper:
        return 100
    if count >= lower:
        return round(((count - lower) / (upper - lower)) * 100)
    return 0
