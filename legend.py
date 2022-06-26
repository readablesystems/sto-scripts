#!/usr/bin/env python3

# Mapping of labels to plot line specifications and legend generation

import functools
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patheffects
import numpy as np
import os.path

# Mapping from concurrency control protocol to an initial marker
cc = {
    'Cicada': 'cicada',
    'Doppel': 'doppel',
    'ERMIA': 'ermia',
    'MOCC': 'mocc',
    'MVCC': 'msto',
    'OCC': 'osto',
    'TicToc': 'tsto',
    }

# Mapping from marker to style
cc_style = {
    'cicada': {
      'color': (148, 103, 189),
      'linestyle': 'solid',
      'linewidth': 2,
      'marker': '$C$',
      },
    'doppel': {
      'color': (152, 223, 138),
      'linestyle': 'solid',
      'linewidth': 1,
      'marker': '$D$',
      },
    'ermia': {
      'color': (140, 86, 75),
      'linestyle': 'solid',
      'linewidth': 2,
      'marker': '$E$',
      },
    'mocc': {
      'color': (227, 119, 194),
      'linestyle': 'solid',
      'linewidth': 2,
      'marker': '$M$',
      },
    'msto': {
      'color': (16, 76, 100),
      'linestyle': (0, (1, 5)),
      'linewidth': 1,
      'marker': 's',
      },
    'osto': {
      'color': (23, 190, 207),
      'linestyle': (0, (1, 5)),
      'linewidth': 1,
      'marker': '8',
      },
    'tsto': {
      'color': (31, 119, 180),
      'linestyle': (0, (1, 5)),
      'linewidth': 1,
      'marker': 'D',
      },
    }

# Mapping from marker to concurrency control protocol name, if difference from above
cc_name = {
    'msto': 'MSTO',
    'osto': 'OSTO',
    'tsto': 'TSTO',
    }

# Optimization options
cc_opts = {
    '20phases': '20p',
    '90phases': '90p',
    '160phases': '160p',
    'ATS': 'ats',
    'DU': 'du',
    'STS': 'sts',
    }

# Optimization styles
cc_opts_style = {
    '20p': {
      'path_effects': [
        mpl.patheffects.withTickedStroke(spacing=1, angle=45),
        ],
      },
    '90p': {
      'path_effects': [
        mpl.patheffects.withTickedStroke(spacing=4, angle=45),
        ],
      },
    '160p': {
      'path_effects': [
        mpl.patheffects.withTickedStroke(spacing=9, angle=45),
        ],
      },
    'ats': {
      'fillstyle': 'top',
      'markerfacecoloralt': 'white',
      },
    'du': {
      'linestyle': (0, (5, 5)),
      },
    'sts': {
      'fillstyle': 'right',
      'markerfacecoloralt': 'gray',
      },
    }

# Toggle-specific options
cc_toggle_style = {
    'secondary': {
      'color': (0.5, 0.5, 0.5),
      'linestyle': (0, (1, 3)),
      'linewidth': 1.25,
      }
    }

# Converting back into human-readable
def series_to_name(shorthand):
  cclabel, *opts = shorthand.split('.')
  if cclabel in cc_name:
    name = cc_name[cclabel]
  else:
    for name, label in cc.items():
      if label == cclabel:
        break

  for ccopt in opts:
    for opt, label in cc_opts.items():
      if label == ccopt:
        break
    optname = functools.reduce(lambda acc, x: \
        f'{acc} {x}' if acc and (acc[-1].isdigit() != x.isdigit()) else acc + x, opt, '')
    if optname[0].isdigit():
      name += f' ({optname})'
    else:
      name += f'+{optname}'
  return name

# Mapping from filename to prefix
def filename_to_prefix(fname):
  return os.path.basename(fname).split('-', 1)[0].split('_', 1)[0]

# Mapping from prefix to experiment
experiment_prefixes = {
    'adapting': 'adapting',
    'c': 'tpcc',
    'd': 'like',
    'e': 'tpcc',
    'like': 'like',
    'mocc': 'tpcc',
    'rubis': 'rubis',
    'tpcc': 'tpcc',
    'wiki': 'wiki',
    'ycsb': 'ycsb',
    }
def filename_to_experiment(fname):
  return experiment_prefixes[filename_to_prefix(fname)]

# Mapping from prefix to value scale; assumed 1 if not specified
scaling_prefixes = {
    'c': 1e6,
    'mocc': 1e6,
    }
def filename_to_scaling(fname):
  return scaling_prefixes.get(filename_to_prefix(fname), 1)
