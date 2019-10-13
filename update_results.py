#!/usr/bin/env python3

import csv
import argparse

parser = argparse.ArgumentParser(description='Update select experiments in result files.')
parser.add_argument('result_file', metavar='result_file', type=str, nargs=1,
                    help='Result CSV file to be updated.')
parser.add_argument('-d', '--diff-file', dest='diff_file', type=str, action='store', required=True,
                    help='CSV file containing columns/experiments to update.')
parser.add_argument('-v' '--verbose', dest='verbose', action='store_true', default=False,
                    help='Turn on verbose messages.')

args = parser.parse_args()

def DPrint(string):
    if args.verbose:
        print(string)

def ProcessDiff(result_file, diff_file):
    try:
        rf_dict = {}
        df_dict = {}
        DPrint('Opening file {}...'.format(result_file))
        with open(result_file, 'r') as rf:
            DPrint('Opening file {}...'.format(diff_file))
            with open(diff_file, 'r') as df:
                rf_reader = csv.DictReader(rf)
                df_reader = csv.DictReader(df)

                try:
                    for rf_row in rf_reader:
                        rf_dict[rf_row['# Threads']] = rf_row
                    for df_row in df_reader:
                        df_dict[df_row['# Threads']] = df_row
                except KeyError:
                    print('Format error.')
                    return

        for nthreads, df_row in df_dict.items():
            for k, v in df_row.items():
                if k != '# Threads':
                    try:
                        DPrint('Replacing (T-{}, E-{}), value {} with {}'.format(nthreads, k, rf_dict[nthreads][k], v))
                        rf_dict[nthreads][k] = v
                    except KeyError:
                        print('Experiment (T-{}, E-{}) not found in result file.'.format(nthreads, k))
                        return

        with open('update_csv_tmp', 'w') as wf:
            field_names = None
            for _, rf_row in rf_dict.items():
                field_names = rf_row.keys()
                break
            writer = csv.DictWriter(wf, field_names)
            writer.writeheader()
            for _, rf_row in rf_dict.items():
                writer.writerow(rf_row)

    except (FileNotFoundError, IOError):
        print('File I/O error.')
        return

ProcessDiff(args.result_file[0], args.diff_file)
