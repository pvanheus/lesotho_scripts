#!/usr/bin/env python

import argparse
import sys
import re
from Bio import SeqIO
from Bio.Seq import Seq
from numpy import require


def trim_end_dashes(seq: Seq):
    seq_str = str(seq)
    re.sub(r'^-*([^-].+[^-])-*$', '\1', seq_str)
    return Seq(seq_str)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Filter FASTA files by N content')
    
    max_n_args = parser.add_mutually_exclusive_group(required=True)
    max_n_args.add_argument('--max_n_perc', type=float)
    max_n_args.add_argument('--max_n', type=float)
    parser.add_argument('--keep_gaps', action='store_true', default=False)
    parser.add_argument('--keep_end_dashes', action='store_true', default=False)
    parser.add_argument('input_file', type=argparse.FileType())
    parser.add_argument('output_file', type=argparse.FileType('w'), nargs='?', default=sys.stdout)
    args = parser.parse_args()

    for seq_record in SeqIO.parse(args.input_file, 'fasta'):
        n_count = 0
        write_out = False
        seq_len = len(seq_record.seq)
        if not args.keep_gaps:
            seq_record.seq = seq_record.seq.ungap('-')
        if not args.keep_end_dashes:
            seq_record.seq = trim_end_dashes(seq_record.seq)
        for base in seq_record.seq:
            if base.upper() == 'N':
                n_count += 1
        if args.max_n_perc is not None and (n_count / seq_len) < args.max_n_perc:
            write_out = True
        elif args.max_n is not None and n_count < args.max_n:
            write_out = True
        if write_out:
            SeqIO.write(seq_record, args.output_file, 'fasta')
