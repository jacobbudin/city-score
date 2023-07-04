import csv
import json
import html
from io import StringIO
from rich.console import Console
from rich.table import Table

def print_pretty(cities, dimensions):
    console = Console()
    table = Table(show_header=True)

    table.add_column('City')
    for dimension in dimensions:
        table.add_column(dimension.title)
    table.add_column('Score')

    for city in cities:
        row = [str(city)]
        for dimension in dimensions:
            value = str(city.get(dimension))
            row.append(value)
        row.append(str(city.last_score))
        table.add_row(*row)

    console.print(table)

def print_html(cities, dimensions):
    print('<table>')
    print('    <thead>')
    print('        <tr>')
    print('            <th>City</th>')
    for dimension in dimensions:
        print('            <th>%s</th>' % html.escape(dimension.title))
    print('            <th>Score</th>')
    print('        </tr>')
    print('    </thead>')
    print('    <tbody>')
    for city in cities:
        print('        <tr>')
        print('             <th scope="row">%s</th>' % html.escape(str(city)))
        for dimension in dimensions:
            print('             <td>%s</td>' % html.escape(str(city.get(dimension))))
            
        print('             <td>%s</td>' % html.escape(str(city.last_score)))
        print('        </tr>')
    print('    </tbody>')
    print('</table>')

def print_csv(cities, dimensions):
    data = StringIO()
    writer = csv.writer(data)
    
    header = ['City']
    for dimension in dimensions:
        header.append(dimension.title)
    header.append('Score')
    writer.writerow(header)

    for city in cities:
        row = [str(city)]
        for dimension in dimensions:
            row.append(city.get(dimension))
        row.append(str(city.last_score))
        writer.writerow(row)

    data.seek(0)
    print(data.read())

def data(cities, dimensions):
    data = []

    keys = ['City']
    for dimension in dimensions:
        keys.append(dimension.title)
    keys.append('Score')

    for city in cities:
        values = [str(city)]
        for dimension in dimensions:
            values.append(city.get(dimension))
        values.append(str(city.last_score))
        
        data.append({k: v for k, v in zip(keys, values)})
    
    return data

def print_json(cities, dimensions):
    print(json.dumps(data(cities, dimensions)))

def print_jsonl(cities, dimensions):
    for item in data(cities, dimensions): 
        print(json.dumps(item))

printers = {
    'pretty': print_pretty,
    'csv': print_csv,
    'json': print_json,
    'jsonl': print_jsonl,
    'html': print_html,
}