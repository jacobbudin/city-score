from ..cache import cache
from ..decorators import dimension, scorer
from ..source import Source
from html.parser import HTMLParser
import requests

class TrustForPublicLand(Source):
    pass

class TrustForPublicLandResultParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.found = False
        self.text_content = ""

    def handle_starttag(self, tag, attrs):
        if tag == "div" and ("class", "bold-statement__heading") in attrs:
            self.found = True
        elif tag == "b" and self.found:
            self.found = True

    def handle_data(self, data):
        if self.found:
            self.text_content = data

    def handle_endtag(self, tag):
        if tag == "div" and self.found:
            self.found = False
        elif tag == "b" and self.found:
            self.found = False

@dimension("TrustForPublicLand")
def nearby_parks_accessibility(city):
    """Percentage of residents who live within a 10-minute walk of a park"""
    key = 'tpl-%s' % (str(city))
    result = cache.get(key)
    if result is not None:
        return result

    city_name = city.name.lower().replace(' ', '-')
    state_name = city.state_name.lower().replace(' ', '-')
    url = f"https://www.tpl.org/city/{city_name}-{state_name}"
    response = requests.get(url)

    if response.status_code == 200:
        parser = TrustForPublicLandResultParser()
        parser.feed(response.text)
        cache.set(key, parser.text_content)
        return parser.text_content
    return '?'

@scorer("TrustForPublicLand")
def nearby_parks_accessibility_scorer(city, lower, upper):
    data = nearby_parks_accessibility(city)
    perc = int(data.strip("%"))
    if perc >= upper:
        return 100
    if perc >= lower:
        return round(((perc - lower) / (upper - lower)) * 100)
    return 0
