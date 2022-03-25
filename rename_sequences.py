#!/usr/bin/env python

import argparse
import csv
import sys
import re

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('id_mapping_file', type=argparse.FileType())
    parser.add_argument('fasta_file', type=argparse.FileType())
    parser.add_argument('output_file', nargs='?', default=sys.stdout, type=argparse.FileType('w'))
    args = parser.parse_args()

    mapping_reader = csv.reader(args.id_mapping_file)
    next(mapping_reader)
    barcode_to_sample_id = {}
    for row in mapping_reader:
        (sample_id, barcode) = row
        barcode_to_sample_id[barcode] = sample_id
    
    for row in args.fasta_file:
        if row.startswith('>'):
            match = re.match('>(.*)_single', row)
            barcode = match.group(1)
            virus_name = 'hCoV-19/Lesotho/L' + barcode_to_sample_id[barcode]
            print('>' + virus_name, file=args.output_file)
        else:
            print(row, end='', file=args.output_file)
