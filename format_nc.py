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
            city_parts = row['City'].split(' ')
            rows.append({
                'County Code': '',
                'State': 'North Carolina',
                'County': row['County'],
                'Name': row['Name'],
                'Temp County': '',
                'Address': row['Street'],
                'City': city_parts[0][:-1],
                'Zip': city_parts[2],
                'lat': '',
                'lng': '',
                'Hours': f"{row['Date']} {row['Hours']}",
                'Type': 'Drop Box'
            })

    rows_by_location = {}
    for row in rows:
        location = f"{row['Name']}-{row['County']}"
        if not location in rows_by_location:
            rows_by_location[location] = row
        else:
            rows_by_location[location]['Hours'] += ', ' + row['Hours']
    rows = rows_by_location.values()

    with open(args.OUT, 'w') as csvfile:
        fieldnames = ['County Code', 'State', 'County', 'Name', 'Temp County', 'Address', 'City', 'Zip', 'lat', 'lng', 'Hours', 'Type']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


    return args.OUT


if __name__ == '__main__':
    run_from_cli(format, DESCRIPTION, ARG_DEFINITIONS, REQUIRED_ARGS)
