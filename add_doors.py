import csv

from pywell.entry_points import run_from_cli


DESCRIPTION = 'Convert CSV to needed format for Airtable import'

ARG_DEFINITIONS = {
    'IN': 'Input CSV',
    'OUT': 'Output CSV'
}

REQUIRED_ARGS = ['IN', 'OUT']



def add_doors(args):

    with open(args.IN, 'rt') as csvfile:
        csvreader = csv.DictReader(csvfile)
        rows = [row for row in csvreader]

    with open('source.csv', 'rt') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter="\t")
        source_rows = [row for row in csvreader]

    with open(args.OUT, 'w') as csvfile:
        fieldnames = ['County Code', 'State', 'County', 'Name', 'Temp County', 'Address', 'City', 'Zip', 'lat', 'lng', 'Hours', 'Type']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for index, row in enumerate(rows):
            row['Name'] = f"{row['Name']} - {source_rows[index]['Location']}"
            writer.writerow(row)


    return args.OUT


if __name__ == '__main__':
    run_from_cli(add_doors, DESCRIPTION, ARG_DEFINITIONS, REQUIRED_ARGS)
