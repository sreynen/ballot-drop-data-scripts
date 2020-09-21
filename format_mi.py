import csv

from pywell.entry_points import run_from_cli


DESCRIPTION = 'Convert CSV to needed format for Airtable import'

ARG_DEFINITIONS = {
    'IN': 'Input CSV',
    'OUT': 'Output CSV'
}

REQUIRED_ARGS = ['IN', 'OUT']



def format(args):
    rows = []
    with open(args.IN, 'rt') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter="\t")
        for row in csvreader:
            rows.append({
                'County Code': '',
                'State': 'Michigan',
                'County': row['County'],
                'Name': row['Township'],
                'Temp County': '',
                'Address': row['Street'],
                'City': row['City'],
                'Zip': '',
                'lat': '',
                'lng': '',
                'Hours': row['Hours'],
                'Type': 'Drop Box'
            })

    with open(args.OUT, 'w') as csvfile:
        fieldnames = ['County Code', 'State', 'County', 'Name', 'Temp County', 'Address', 'City', 'Zip', 'lat', 'lng', 'Hours', 'Type']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


    return args.OUT


if __name__ == '__main__':
    run_from_cli(format, DESCRIPTION, ARG_DEFINITIONS, REQUIRED_ARGS)
