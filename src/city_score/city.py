import csv
from dataclasses import dataclass, field
from functools import cached_property
from .sources.core import Core

state_names = {
    "AL":"Alabama",
    "AK":"Alaska",
    "AZ":"Arizona",
    "AR":"Arkansas",
    "CA":"California",
    "CO":"Colorado",
    "CT":"Connecticut",
    "DE":"Delaware",
    "FL":"Florida",
    "GA":"Georgia",
    "HI":"Hawaii",
    "ID":"Idaho",
    "IL":"Illinois",
    "IN":"Indiana",
    "IA":"Iowa",
    "KS":"Kansas",
    "KY":"Kentucky",
    "LA":"Louisiana",
    "ME":"Maine",
    "MD":"Maryland",
    "MA":"Massachusetts",
    "MI":"Michigan",
    "MN":"Minnesota",
    "MS":"Mississippi",
    "MO":"Missouri",
    "MT":"Montana",
    "NE":"Nebraska",
    "NV":"Nevada",
    "NH":"New Hampshire",
    "NJ":"New Jersey",
    "NM":"New Mexico",
    "NY":"New York",
    "NC":"North Carolina",
    "ND":"North Dakota",
    "OH":"Ohio",
    "OK":"Oklahoma",
    "OR":"Oregon",
    "PA":"Pennsylvania",
    "RI":"Rhode Island",
    "SC":"South Carolina",
    "SD":"South Dakota",
    "TN":"Tennessee",
    "TX":"Texas",
    "UT":"Utah",
    "VT":"Vermont",
    "VA":"Virginia",
    "WA":"Washington",
    "WV":"West Virginia",
    "WI":"Wisconsin",
    "WY":"Wyoming"
}

@dataclass
class City:
    name: str
    state: str
    lat: float
    lng: float
    data: dict = field(default_factory=dict)
    last_score: int = -1

    def __str__(self):
        return '%s, %s' % (self.name, self.state)

    @staticmethod
    def generate_key(name, state):
        return name.replace(' ','').replace('\'', '').replace('-', '').upper().removesuffix('CITY').strip() + ' ' + state.upper()

    @cached_property
    def key(self):
        return self.generate_key(self.name, self.state)

    @property
    def coordinates(self):
        return (self.lat, self.lng)
    
    @property
    def state_name(self):
        return state_names[self.state]

    def update(self, data):
        self.data.update(data)

    def get(self, f):
        return f(self)

    def qualify(self, criteria):
        """Check whether this city meets minimum criteria"""
        for criterion in criteria:
            if not criterion(self):
                return False

        return True

    def score(self, scorers):
        """Generate a score"""
        scores = []

        for scorer in scorers:
            scores.append(scorer(self))

        self.last_score = sum(scores)
        return self.last_score
    
def get_cities():
    """Generate a list of all US cities"""
    city_strs = set()

    with Core.open('cities.csv') as f:
        city_reader = csv.DictReader(f)
        for city_row in city_reader:
            city = City(city_row['CITY'], city_row['STATE_CODE'], float(city_row['LATITUDE']), float(city_row['LONGITUDE']))
            city_str = str(city)

            if city_str in city_strs:
                continue
            city_strs.add(city_str)
            yield city