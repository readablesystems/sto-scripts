#!/usr/bin/env python3

import csv
import argparse
import numpy

parser = argparse.ArgumentParser(description='Read experiment results.')
parser.add_argument('files', metavar='file', type=str, nargs='+',
                    help='CSV files to parse.')
parser.add_argument('-s', '--system-name', dest='system_name', type=str, action='store', required=True,
                    help='Specify the name of the system to inspect (e.g. \"MVCC + ST (W0)\")')
parser.add_argument('-t', '--num-threads', dest='num_threads', type=int, action='store', required=True,
                    help='Specify the number of threads in the experiment.')
parser.add_argument('-n', '--num-trials', dest='num_trials', type=int, action='store', default=5,
                    help='Specify the number of trials in the experiment (default is 5).')
parser.add_argument('-v' '--verbose', dest='verbose', action='store_true', default=False,
                    help='Turn on verbose messages.')

args = parser.parse_args()

ntrials = args.num_trials

def process_file(filename):
    try:
        with open(filename, 'r') as rf:
            reader = csv.DictReader(rf)
            xput_data = []
            for row in reader:
                if int(row['# Threads']) != args.num_threads:
                    continue
                for i in range(ntrials):
                    col_key = '{} [T{}]'.format(args.system_name, i+1)
                    try:
                        xput = float(row[col_key])
                        xput_data.append(xput)
                    except KeyError:
                        if args.verbose:
                            print('System name \"{}\" not found'.format(col_key))
                        return None
            return xput_data
    except (FileNotFoundError, IOError):
        if args.verbose:
            print('Input file {} not found.'.format(filename))
        return None

for f in args.files:
    data = process_file(f)
    if data is None:
        continue
    results = {}
    results['min'] = numpy.min(data)
    results['med'] = numpy.median(data)
    results['max'] = numpy.max(data)
    print(results)
