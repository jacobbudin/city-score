from ..cache import cache
from ..decorators import dimension, scorer
from ..source import Source
from html.parser import HTMLParser
import requests

class TrailLinkMilesParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.found = False
        self.total_trail_miles = 0

    def handle_starttag(self, tag, attrs):
        if tag == "span":
            for attr in attrs:
                if attr[0] == "itemprop" and attr[1] == "distance":
                    self.found = True

    def handle_data(self, data):
        if self.found:
            self.total_trail_miles += float(data.split()[0])

    def handle_endtag(self, tag):
        if tag == "span" and self.found:
            self.found = False


class TrailLink(Source):
    base_url = "https://www.traillink.com/trailsearch"

def format(number):
    return f"{number} miles"

@dimension('TrailLink Mileage')
def trail_total_miles(city):
    key = 'traillink-%s' % (str(city))
    count = cache.get(key)
    if count is not None:
        return format(count)
    
    response = requests.get(TrailLink.base_url, params={
        "city": city.name,
        "state": city.state
    })

    if response.status_code == 200:
        parser = TrailLinkMilesParser()
        parser.feed(response.text)
        count = int(parser.total_trail_miles)
        cache.set(key, count)
        return format(count)

@scorer('TrailLink')
def trail_total_miles_scorer(city, lower, upper):
    count = float(trail_total_miles(city).split(' ')[0])
    if count >= upper:
        return 100
    if count >= lower:
        return round(((count - lower) / (upper - lower)) * 100)
    return 0
