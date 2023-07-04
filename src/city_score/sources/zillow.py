from ..city import City
from ..decorators import criterion, dimension, scorer
from ..source import Source

import csv

class Zillow(Source):
    files = {
        'zillow-zhvi.csv': {'url': 'https://files.zillowstatic.com/research/public_csvs/zhvi/City_zhvi_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv'},
        'zillow-zori.csv': {'url': 'https://files.zillowstatic.com/research/public_csvs/zori/City_zori_sm_month.csv'},
    }

    @classmethod
    def populate(cls, cities):
        with cls.open('zillow-zhvi.csv') as f:
            reader = csv.DictReader(f)
            for datum in reader:
                key = City.generate_key(datum['RegionName'], datum['State'])
                if city := cities.get(key):
                    if zhvi := datum['2023-05-31']:
                        city.update({
                            'zhvi': round(float(zhvi)),
                        })
        with cls.open('zillow-zori.csv') as f:
            reader = csv.DictReader(f)
            for datum in reader:
                key = City.generate_key(datum['RegionName'], datum['State'])
                if city := cities.get(key):
                    if zori := datum['2023-05-31']:
                        city.update({
                            'zori': round(float(zori)),
                        })

@dimension('Zillow® ZHVI')
def median_home_price(city):
    if zhvi := city.data.get('zhvi'):
        return f'${zhvi:,}'

    return None

@dimension('Zillow® ZORI')
def median_rent(city):
    if zori := city.data.get('zori'):
        return f'${zori:,}'

    return None

@criterion('Maximum Zillow® ZHVI')
def maximum_median_home_price(city, price, default=False):
    if 'zhvi' not in city.data:
        return default

    return city.data['zhvi'] <= price

@scorer('Zillow® ZHVI score')
def median_home_price_scorer(city, lower, upper):
    if zhvi := city.data.get('zhvi'):
        if zhvi <= lower:
            return 100
        if zhvi <= upper:
            return round((1 - (zhvi - lower) / (upper - lower)) * 100)
    return 0