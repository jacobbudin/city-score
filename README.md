# City Score
City Score is a command-line application for scoring cities based on your personal preferences. Here's an example:

<table>
    <thead>
        <tr>
            <th>City</th>
            <th>Population</th>
            <th>Zillow® ZHVI</th>
            <th>PeopleForBikes</th>
            <th>Yelp &quot;gay bars&quot;</th>
            <th>Nearby ski resorts</th>
            <th>Score</th>
        </tr>
    </thead>
    <tbody>
        <tr>
             <th scope="row">Portland, OR</th>
             <td>647,176</td>
             <td>$547,999</td>
             <td>56</td>
             <td>9</td>
             <td>Mount Hood Ski Bowl (42 miles) and 2 more</td>
             <td>100</td>
        </tr>
        <tr>
             <th scope="row">Detroit, MI</th>
             <td>645,658</td>
             <td>$64,414</td>
             <td>42</td>
             <td>7</td>
             <td>Mt Brighton, MI (41 miles) and 1 more</td>
             <td>86</td>
        </tr>
        <tr>
             <th scope="row">Cambridge, MA</th>
             <td>116,892</td>
             <td>$959,032</td>
             <td>58</td>
             <td>6</td>
             <td>Wachusett Mountain (40 miles) and 5 more</td>
             <td>84</td>
        </tr>
    </tbody>
</table>

## Technologies
- Python 3

## Features
- Ranks all 29,880 cities and towns in the United States
- Includes multiple built-in data providers
- Designed to allow users to easily add and remix data
- Outputs prettified to the console or to CSV, HTML, JSON, JSONL

## Design
City Score uses a three-step process:
1. Qualification: criteria identify cities that meet your minimum standard.
2. Scoring: scorers score facets of your choosing at various weights.
3. Generation: dimensions appear in the final output.

## Quick start
1. Download City Score from PyPI:
    ```
    $ python3 -m pip install city_score
    ```
2. Create a script (`myscore.py`) like this:
    ```python
    from city_score import run
    from city_score.sources.core import *
    from city_score.sources.peopleforbikes import *
    from city_score.sources.zillow import *

    sources = (
        PeopleForBikes,
        Zillow,
    )

    criteria = (
        minimum_bike_score(25),
        minimum_population(60000),
        maximum_median_home_price(1000000),
        prohibited_states(('TX', 'FL', 'CO', )),
    )

    scorers = (
        median_home_price_scorer(lower=350000, upper=800000),
        bike_score_scorer(lower=40, upper=80, weight=2),
    )

    dimensions = (
        population,
        median_home_price,
        median_rent,
        bike_score,
    )

    run(sources, criteria, scorers, dimensions)
    ```
3. Run your script:
    ```
    $ python3 myscore.py --sort=score --scale-scores
    ```

## Data sources
- 🚲 PeopleForBikes provides a score for biking infrastructure.
- 🏂 Snowpak provides the name and location of most ski resorts.
- 🍕 Yelp provides data on many points of interest, including businesses.
- 🏡 Zillow provides estimates for home and rent prices.

## License
MIT License