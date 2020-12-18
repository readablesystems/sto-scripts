#!/usr/bin/env python3

import argparse
import collections
import csv
import statistics

parser = argparse.ArgumentParser(description='Process input data')
parser.add_argument('file', metavar='FILE', type=str,
                    help='Data file to process')
parser.add_argument('-t', '--threads', dest='threads', type=int, default=64,
                    help='Number of threads to look at (default: 64)')

args = parser.parse_args()

data = collections.defaultdict(list)
with open(args.file, 'r') as fin:
  reader = csv.DictReader(fin)
  for row in reader:
    th = int(row['# Threads'])
    if th != args.threads:
      continue
    for key, value in row.items():
      if key == '# Threads':
        continue
      experiment = key[:-5]
      data[experiment] += [float(value)]

results = []
for key, value in data.items():
  results += [[key, statistics.median(value)]]

results.sort()

for r in results:
  print('[{}] median: {}'.format(r[0], r[1]))
