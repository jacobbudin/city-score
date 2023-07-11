from ..cache import cache
from ..decorators import dimension, scorer
from ..source import Source
from html.parser import HTMLParser
import requests

activities_filter = {
    'Atv': 'ATV',
    'Bike': 'BIKE',
    'Birding': 'BIRD',
    'Cross Country Skiing': 'XSKI',
    'Dog Walking': 'DOG',
    'Fishing': 'FISH',
    'Geocaching': 'GEO',
    'Hiking': 'HIKE',
    'Horseback Riding': 'HORSE',
    'Inline Skating': 'SKTS',
    'Mountain Biking': 'MTBK',
    'Running': 'RUN',
    'Snowmobiling': 'SNOW',
    'Walking': 'WALK',
    'Wheelchair Accessible': 'WHEEL'
}

class TrailLinkMilesParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.found = False
        self.total_trail_miles = 0

    def handle_starttag(self, tag, attrs):
        if tag == 'span':
            for attr in attrs:
                if attr[0] == 'itemprop' and attr[1] == 'distance':
                    self.found = True

    def handle_data(self, data):
        if self.found:
            self.total_trail_miles += float(data.split()[0])

    def handle_endtag(self, tag):
        if tag == 'span' and self.found:
            self.found = False

class TrailLink(Source):
    base_url = 'https://www.traillink.com/trailsearch'

def format_miles(number):
    return f'{number} miles'

def scrap_total_miles(city, activities, min_length_miles):
    """Request TrailLink page and return sum of total trail miles"""
    num_miles = 0

    activity_values = []
    for activity in activities:
        activity_values.append(activities_filter[activity])

    params = {
        'city': city.name,
        'state': city.state,
        'activities': ",".join(activity_values),
        'length': f'{min_length_miles}|99999'
    }
    response = requests.get(TrailLink.base_url, params)

    if response.status_code == 200:
        parser = TrailLinkMilesParser()
        parser.feed(response.text)
        num_miles = int(parser.total_trail_miles)

    return num_miles

@dimension('TrailLink Mileage')
def trail_total_miles(city, activities=[], min_length_miles=0):
    key = 'traillink-%s-%s-%s' % (
        str(city),
        str('-'.join(activity.replace(' ', '') for activity in activities)),
        str(min_length_miles),
    )
    num_miles = cache.get(key)
    if num_miles is not None:
        return format_miles(num_miles)

    num_miles = scrap_total_miles(city, activities, min_length_miles)
    cache.set(key, num_miles)
    return format_miles(num_miles)

@scorer('TrailLink')
def trail_total_miles_scorer(city, lower, upper, activities=[], min_length_miles=0):
    num_miles = scrap_total_miles(city, activities, min_length_miles)
    if num_miles >= upper:
        return 100
    if num_miles >= lower:
        return round(((num_miles - lower) / (upper - lower)) * 100)
    return 0
