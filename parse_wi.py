import csv

from pywell.entry_points import run_from_cli


DESCRIPTION = 'Convert HTML to CSV for WI data'

ARG_DEFINITIONS = {
    'IN': 'Input HTML',
    'OUT': 'Output CSV'
}

REQUIRED_ARGS = ['IN', 'OUT']


def format(args):
    pages = []
    with open(args.IN, 'rt') as html:
        line = html.readline()
        while line:
            div = line.split('>')[0]
            rest = '>'.join(line.split('>')[1:])
            content = rest.split('</div')[0]
            style = div.split(';')
            left = float(style[1].split(':')[1].split('p')[0])
            top = float(style[2].split(':')[1].split('p')[0])
            entry = {
                'content': content,
                'left': left,
                'top': top
            }
            if left == 0 and top == 0:
                pages.append([])
            else:
                pages[len(pages) - 1].append(entry)
            line = html.readline()
    sets = []
    for entries in pages:
        hindis = [entry for entry in entries if entry.get('left') == 145.3]
        hindis.sort(key=lambda hindi: hindi.get('top'))
        for index, hindi in enumerate(hindis):
            if index + 1 < len(hindis):
                max_top = hindis[index + 1].get('top')
                set_entries = [
                    entry for entry in entries
                    if entry.get('top') >= hindi.get('top')
                    and entry.get('top') < max_top
                ]
            else:
                set_entries = [
                    entry for entry in entries
                    if entry.get('top') >= hindi.get('top')
                ]
            sets.append(set_entries)
    rows = []
    for entries in sets:
        column_one = ' '.join([
            entry.get('content') for entry in entries
            if entry.get('left') < 145
        ])
        hindi = [
            entry.get('content') for entry in entries
            if entry.get('left') > 145 and entry.get('left') < 190
        ][0]
        column_three = [
            entry.get('content') for entry in entries
            if entry.get('left') > 190 and entry.get('left') < 380
        ]
        column_four = ' '.join([
            entry.get('content') for entry in entries
            if entry.get('left') > 380 and entry.get('left') < 520
        ])
        last_updated = ' '.join([
            entry.get('content') for entry in entries
            if entry.get('left') > 520
        ])
        website = ''
        if column_four:
            if len(column_four.split('"')) > 1:
                website = column_four.split('"')[1].split('"')[0]
            else:
                website = column_four
        (city, county) = column_one.split('-')
        column_three_dict = {}
        for row in column_three:
            if len(row.split(':')) == 2:
                key = row.split(':')[0].strip()
                value = row.split(':')[1].strip()
                column_three_dict[key] = value
            else:
                column_three_dict[key] += ' ' + row
        row = {
            'hindi': hindi,
            'city': city.strip(),
            'county': county.strip(),
            'website': website,
            'last_updated': last_updated,
        }
        row.update(column_three_dict)
        rows.append(row)

    all_keys = set()
    for row in rows:
        all_keys.update(list(row.keys()))

    with open(args.OUT, 'w') as csvfile:
        fieldnames = list(all_keys)
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)

    return args.OUT


if __name__ == '__main__':
    run_from_cli(format, DESCRIPTION, ARG_DEFINITIONS, REQUIRED_ARGS)
