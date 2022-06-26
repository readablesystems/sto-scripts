#!/usr/bin/env python3

# Parse experiment data into raw data points

import collections
import csv
import json
import optparse
import os

import config
import legend

def recursive_update(accumulator, updates):
  '''Merge updates into the accumulator.'''
  for key, value in updates.items():
    key = str(key)
    if key in accumulator and isinstance(value, dict):
      recursive_update(accumulator[key], value)
    else:
      accumulator[key] = value

def vldb_parse(filename):
  '''Parse the file using VLDB '20 submission data format.'''
  experiment = legend.filename_to_experiment(filename)
  scale_factor = legend.filename_to_scaling(filename)
  data = collections.defaultdict(
      lambda: collections.defaultdict(
        lambda: collections.defaultdict(
          lambda: collections.defaultdict())))
  with open(filename, 'r') as fin:
    cin = csv.DictReader(fin)
    for row in cin:
      threads = int(row['# Threads'])
      for column, value in row.items():
        if column == '# Threads':
          continue
        colparts = column.split(' ')
        cc = colparts[0]  # Concurrency control scheme
        opts = ()
        subexperiment = None
        trial = None

        index = 1
        while index < len(colparts):
          part = colparts[index]
          if part == '+':  # Appending opts
            index += 1
            opts += (legend.cc_opts[colparts[index]],)
          elif part[0] == '(':
            assert part[-1] == ')'
            assert not subexperiment
            subexperiment = part[1:-1]
          elif part[:2] == '[T':
            assert part[-1] == ']'
            assert not trial
            trial = int(part[2:-1])
          else:
            assert False, f'Invalid header part: {part}'
          index += 1

        try:
          value = float(value) * scale_factor
        except:
          value = None

        graph_key = '.'.join((legend.cc[cc],) + opts)
        if subexperiment:
          bucket = data[experiment][subexperiment][graph_key]
        else:
          bucket = data[experiment][graph_key]

        if threads not in bucket:
          bucket[threads] = []
        if len(bucket[threads]) < trial:
          bucket[threads] += [None] * (trial - len(bucket[threads]))
        bucket[threads][trial - 1] = value

  return experiment, data

def main():
  parsing_methods = ('vldb',)
  parser = optparse.OptionParser(
      description='Parse experiment data into raw data points for graph generation.',
      usage='Usage: %prog [options] file1 file2...',
      )
  parser.add_option('-m', '--method', action='store',
                    choices=parsing_methods,
                    dest='method', type='choice',
                    help='Parsing method, one of: ' + ', '.join(parsing_methods))
  parser.add_option('-p', '--path', action='store', default='experiments/data/',
                    dest='path', type='str',
                    help='Target directory for storing parsed data.')

  (options, args) = parser.parse_args()

  required = ('method',)
  for req in required:
    if not options.__dict__[req]:
      print('Missing required argument:', req)
      print()
      parser.print_help()
      return

  method = options.method

  for filename in args:
    data = {}
    if method == 'vldb':
      experiment, data = vldb_parse(filename)

    datafile = config.make_path(method, options.path, experiment)

    if data:
      os.makedirs(options.path, exist_ok=True)
      if not os.path.isfile(datafile):
        with open(datafile, 'w') as fdata:
          json.dump({}, fdata)

      with open(datafile, 'r') as fdata:
        dataset = json.load(fdata)

      recursive_update(dataset, data)

      with open(datafile, 'w') as fdata:
        json.dump(dataset, fdata, indent=4, sort_keys=True)

if __name__ == '__main__':
  main()
