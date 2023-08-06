import csv
import re
import subprocess
import quopri
from datetime import date
from html.parser import HTMLParser

import click
import xlsxwriter


def save_to_csv(filename, rows):
    with open(filename, 'w', newline='') as csvfile:
        friscowriter = csv.writer(csvfile)
        for row in rows:
            friscowriter.writerow(row)


def save_to_xlsx(filename, rows):

    # Create a workbook and add a worksheet.
    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet()

    # Iterate over the data and write it out row by row.
    for i, row in enumerate(rows):
        for col, value in enumerate(row):
            worksheet.write(i, col, value)

    workbook.close()


class FriscoParser(HTMLParser):
    def __init__(self, *args, **kwargs):
        super(FriscoParser, self).__init__(*args, **kwargs)
        self.rows = []

    def handle_starttag(self, tag, attrs):
        if tag == 'tr':
            self.rows.append([])

    def handle_data(self, data):
        if data in ('=20', '23%', '5%', '8%'):
            return
        try:
            processed_data = self.process_data(data)
        except ValueError as e:
            msg = 'skipping data: "{}" because of error: {}'.format(data, e)
            click.secho(msg, fg='yellow')
            return
        try:
            self.rows[-1].append(processed_data)
        except IndexError:
            pass

    def test_data(self):
        if len({len(r) for r in self.rows}) != 1:
            for r in self.rows:
                if len(r) != 4:
                    click.secho('Rows with columns different then 4: {}'.format(r), fg='red')

    @staticmethod
    def process_data(data):
        data = quopri.decodestring(data)
        try:
            data = data.decode('utf-8')
        except UnicodeDecodeError:
            data = data.decode('unicode_escape')
        data = re.sub('\s*zł$', '', data)
        if data.replace('.', '', 1).isdigit():
            try:
                data = int(data)
            except ValueError:
                data = float(data)
        return data


def clear_raw_mail(raw_file):
    tables = re.findall(r'[^\w]table.*?/table[^\w]', raw_file, flags=re.M | re.S)
    filtered_tables = list(filter(lambda x: 'PRODUCT ROW' in x, tables))
    assert len(filtered_tables) == 1, 'More tables with product rows then 1'
    table = filtered_tables[0]
    end_stripped = re.sub('\n +', '', table)
    end_stripped = re.sub('=\n', '', end_stripped)
    return end_stripped


@click.command()
@click.argument('source', type=click.Path(exists=True))
@click.option('--output', default=None, help='Name of output file. Default: frisco_YYYY_MM_DD')
@click.option('--format', 'format_', default='xlsx', help='Format of generated file. Defaults to xlsx')
@click.option('--open', 'open_', is_flag=True, help='Open generated file after program execution')
def main(source, output, format_, open_):

    with open(source, 'r') as file_:
        raw_file = file_.read()

    cleared = clear_raw_mail(raw_file)
    fp = FriscoParser()
    fp.feed(cleared)
    fp.test_data()

    output = output or "frisco_{}".format(date.today())
    output += '.{}'.format(format_)

    if format_ == 'csv':
        save_to_csv(output, fp.rows);
    if format_ == 'xlsx':
        save_to_xlsx(output, fp.rows);

    if open_:
        subprocess.call(['open', output])


if __name__ == '__main__':
    main()
