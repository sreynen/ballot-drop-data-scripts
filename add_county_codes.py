import csv

from pywell.entry_points import run_from_cli


DESCRIPTION = 'Convert CSV to needed format for Airtable import'

ARG_DEFINITIONS = {
    'IN': 'Input CSV',
    'OUT': 'Output CSV',
    'COUNTIES': 'County CSV'
}

REQUIRED_ARGS = ['IN', 'OUT', 'COUNTIES']



def add_county_codes(args):

    county_name_to_code = {}
    with open(args.COUNTIES, 'rt') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter="\t")
        for row in csvreader:
            county_name_to_code[row['name'].upper()] = row['code']

    with open(args.IN, 'rt') as csvfile:
        csvreader = csv.DictReader(csvfile)
        rows = [row for row in csvreader]

    with open(args.OUT, 'w') as csvfile:
        fieldnames = ['County Code', 'State', 'County', 'Name', 'Temp County', 'Address', 'City', 'Zip', 'lat', 'lng', 'Hours', 'Type']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            row['County Code'] = county_name_to_code.get(row['County'].upper(), county_name_to_code.get(f"{row['County'].upper()} COUNTY",''))
            writer.writerow(row)


    return args.OUT


if __name__ == '__main__':
    run_from_cli(add_county_codes, DESCRIPTION, ARG_DEFINITIONS, REQUIRED_ARGS)
