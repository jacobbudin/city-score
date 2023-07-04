from ..decorators import criterion, dimension, scorer
from ..source import Source

from geopy.distance import geodesic
import json

class Snowpak(Source):
    files = {
        'snowpak.json': {
            'url': 'https://www.snowpak.com/usa',
            'start': '[{"slug":"alyeska-resort",',
            'end': '89aaa3e.jpg"}]',
        },
    }
    
    @classmethod
    def populate(cls, cities):
        ski_resort_data = json.load(cls.open('snowpak.json'))

        for city in cities.values():
            ski_resorts = []
            for datum in ski_resort_data:
                if abs(datum['lat'] - city.lat) >= 2: # one degree is approx. 69 miles
                    continue

                if abs(datum['lng'] - city.lng) >= 2:
                    continue

                distance = geodesic(city.coordinates, (datum['lat'], datum['lng']))
                ski_resorts.append({
                    'name': datum['name'],
                    'miles': distance.miles
                })

            city.update({
                'ski_resorts': ski_resorts
            })

@dimension('Nearby ski resorts')
def nearby_ski_resorts(city, compact=False, miles=100, exclude=[]):
    if ski_resorts := city.data.get('ski_resorts'):
        if len(ski_resorts) == 0:
            return None

        ski_resorts = tuple(filter(lambda r: r['miles'] <= miles and r['name'] not in exclude, sorted(ski_resorts, key=lambda r: r['miles'])))
        f = '{resort[name]} ({resort[miles]:.0f} miles)'
        if compact:
            closest_resort = ski_resorts[0]
            s = f.format(resort=closest_resort)
            if len(ski_resorts) > 1:
                s += ' and %d more' % (len(ski_resorts) - 1)
            return s

        l = [f.format(resort=resort) for resort in ski_resorts]
        return '\n'.join(l)

    return None

@criterion('Minimum ski resorts')
def minimum_ski_resorts(city, count, miles=100, default=False, exclude=[]):
    if 'ski_resorts' not in city.data:
        return default

    nearby_ski_resorts = tuple(filter(lambda r: r['miles'] <= miles and r['name'] not in exclude, city.data['ski_resorts']))
    return len(nearby_ski_resorts) >= count

@scorer('Closest ski resort score')
def closest_ski_resort_scorer(city, lower, upper, exclude=[]):
    if ski_resorts := city.data.get('ski_resorts'):
        if len(ski_resorts) == 0:
            return 0
        
        ski_resorts = tuple(filter(lambda r: r['name'] not in exclude, sorted(ski_resorts, key=lambda r: r['miles'])))
        closest_resort_miles = ski_resorts[0]['miles']

        if closest_resort_miles <= lower:
            return 100
        if closest_resort_miles <= upper:
            return round((1 - (closest_resort_miles - lower) / (upper - lower)) * 100)
    
    return 0