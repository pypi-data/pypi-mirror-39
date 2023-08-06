#!/usr/bin/env python3

import csv
import argparse
from io import StringIO
import boto3


parser = argparse.ArgumentParser(epilog='''\
To save to a file:
    matillion-columns [OPTIONS] csv_file.csv > outfile.txt

To copy to clipboard (Mac):
    matillion-columns csv_file.csv | pbcopy
''', formatter_class=argparse.RawDescriptionHelpFormatter)

parser.add_argument('csv_file', help='Path to CSV file in S3 to extract headers from (excluding bucket name).')
parser.add_argument('--bucket', '-b', default='translatingdata-dev', help='Bucket to get CSV from.')
args = parser.parse_args()


def generate_line(csv_header):
    line = [csv_header, 'VARCHAR', '', '', '', 'No', 'No', 'VARCHAR', '', '']
    return '\t'.join(line)


def main():
    client = boto3.client('s3')
    csv_obj = client.get_object(Bucket=args.bucket, Key=args.csv_file)
    body = csv_obj['Body'].read().decode('utf-8')
    reader = csv.reader(StringIO(body))
    headers = next(reader)
    columns = ''
    for header in headers:
        columns += generate_line(header) + '\n'
    print(columns)
