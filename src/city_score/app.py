from .city import City, get_cities
from .printers import printers

import argparse

def run(sources=(), criteria=(), scorers=(), dimensions=()):
    parser = argparse.ArgumentParser(prog='City Score', description='Caculate a city\'s score based on your personal preferences')
    parser.add_argument('-s', '--sort', choices=('alphabetical', 'score'), default='alphabetical', help='Result order')
    parser.add_argument('-f', '--format', choices=('pretty', 'csv', 'json', 'jsonl', 'html'), default='pretty', help='Output format')
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('--scale-scores', action='store_true', help='Scale scores such that the top score is 100')
    args = parser.parse_args()

    # Generate City instances
    cities = {city.key: city for city in get_cities()}

    # Populate, qualify, and score
    for source in sources:
        source.populate(cities)

    qualified_cities = []
    for city in cities.values():
        if city.qualify(criteria):
            qualified_cities.append(city)

    for city in qualified_cities:
        city.score(scorers)

    if args.sort == 'alphabetical':
        qualified_cities = sorted(qualified_cities, key=lambda c: c.name)
    elif args.sort == 'score':
        qualified_cities = sorted(qualified_cities, key=lambda c: c.last_score, reverse=True)

    if args.scale_scores:
        scores = (c.last_score for c in qualified_cities)
        top_score = max(scores)
        scale = 100 / top_score
        for city in qualified_cities:
            city.last_score = round(city.last_score * scale)

    printer = printers[args.format]
    printer(qualified_cities, dimensions)