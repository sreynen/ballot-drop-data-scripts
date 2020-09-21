import csv

from pywell.entry_points import run_from_cli

import requests


DESCRIPTION = 'Convert CSV to needed format for Airtable import'

ARG_DEFINITIONS = {
    'IN': 'Input CSV',
    'OUT': 'Output CSV',
    'MAPQUEST_API_KEY': 'API key for MapQuest'
}

REQUIRED_ARGS = ['IN', 'OUT', 'MAPQUEST_API_KEY']


def add_geo(args):

    with open(args.IN, 'rt') as csvfile:
        csvreader = csv.DictReader(csvfile)
        rows = [row for row in csvreader]

    with open(args.OUT, 'w') as csvfile:
        fieldnames = ['County Code', 'State', 'County', 'Name', 'Temp County', 'Address', 'City', 'Zip', 'lat', 'lng', 'Hours', 'Type']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            result = requests.get(
                'http://www.mapquestapi.com/geocoding/v1/address',
                params={
                    'key': args.MAPQUEST_API_KEY,
                    'location': f"{row['Address']} {row['City']}, {row['State']}"
                }
            ).json()
            location = result.get('results')[0].get('locations')[0]
            zip = location.get('postalCode')
            if zip:
                row['Zip'] = zip
            row['lat'] = location.get('latLng').get('lat')
            row['lng'] = location.get('latLng').get('lng')
            writer.writerow(row)


    return args.OUT


if __name__ == '__main__':
    run_from_cli(add_geo, DESCRIPTION, ARG_DEFINITIONS, REQUIRED_ARGS)
