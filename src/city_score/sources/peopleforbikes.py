from ..city import City
from ..decorators import criterion, dimension, scorer
from ..source import Source

import json

class PeopleForBikes(Source):
    files = {
        'peopleforbikes.json': {
            'url': 'https://cityratings.peopleforbikes.org/_next/static/chunks/pages/_app-f9bf24502780edb0.js',
            'start': '[{"city":"Canberra","state":"ACT",',
            'end': '"citySlug":"swansea-swa"}]',
        },
    }

    @classmethod
    def populate(cls, cities):
        bike_data = json.load(cls.open('peopleforbikes.json'))
        for datum in bike_data:
            key = City.generate_key(datum['city'], datum['state'])
            if city := cities.get(key):
                city.update({
                    'bike_score': int(datum['bnaRoundedScore']),
                    'population': int(datum['censusPopulation'])
                })

@dimension('PeopleForBikes')
def bike_score(city):
    if bike_score := city.data.get('bike_score'):
        return bike_score

    return None

@criterion('Minimum PeopleForBikes score')
def minimum_bike_score(city, score, default=False):
    if 'bike_score' not in city.data:
        return default

    return city.data['bike_score'] >= score

@scorer('PeopleForBikes score')
def bike_score_scorer(city, lower, upper):
    if bike_score := city.data.get('bike_score'):
        if bike_score >= upper:
            return 100
        if bike_score >= lower:
            return round(((bike_score - lower) / (upper - lower)) * 100)
    return 0