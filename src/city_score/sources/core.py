from ..decorators import criterion, dimension
from ..source import Source

class Core(Source):
    files = {
        'cities.csv': {'url': 'https://raw.githubusercontent.com/kelvins/US-Cities-Database/main/csv/us_cities.csv'},
    }

@dimension('Population')
def population(city):
    if population := city.data.get('population'):
        return f'{population:,}'

    return None

@criterion('Maximum population')
def maximum_population(city, size, default=False):
    if 'population' not in city.data:
        return default

    return city.data['population'] <= size

@criterion('Minimum population')
def minimum_population(city, size, default=False):
    if 'population' not in city.data:
        return default

    return city.data['population'] >= size

@criterion('Allowed states')
def allowed_states(city, states):
    for state in states:
        if city.state == state.upper():
            return True

    return False

@criterion('Prohibited states')
def prohibited_states(city, states):
    for state in states:
        if city.state == state.upper():
            return False

    return True