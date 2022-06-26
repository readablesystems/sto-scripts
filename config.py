import matplotlib as mpl

quiet = False

# Common configuration information

if __name__ == '__main__':
  import sys
  print('config.py cannot be run directly as a Python script.')
  sys.exit(1)

# Preconfigured bundles of lines
bundles = {
    'ats': ('osto.ats', 'tsto.ats', 'msto.ats'),
    'ats-du': ('osto.ats.du', 'tsto.ats.du', 'msto.ats.du'),
    'doppel': ('doppel.20p', 'doppel.90p', 'doppel.160p'),
    'msto-all': ('msto', 'msto.du', 'msto.sts', 'msto.sts.du', 'msto.ats', 'msto.ats.du'),
    'nts': ('osto', 'tsto', 'msto'),
    'nts-du': ('osto.du', 'tsto.du', 'msto.du'),
    'osto-all': ('osto', 'osto.du', 'osto.sts', 'osto.sts.du', 'osto.ats', 'osto.ats.du'),
    'sts': ('osto.sts', 'tsto.sts', 'msto.sts'),
    'sts-du': ('osto.sts.du', 'tsto.sts.du', 'msto.sts.du'),
    'tpcc-base': ('osto', 'msto', 'tsto', 'cicada', 'ermia', 'mocc'),
    'tsto-all': ('tsto', 'tsto.du', 'tsto.sts', 'tsto.sts.du', 'tsto.ats', 'tsto.ats.du'),
    }
def get_lines(bundle):
  '''Return a tuple of lines related to the bundle. By default, just (bundle).'''
  if bundle in bundles:
    if not quiet:
      print(f'Using bundle "{bundle}": {bundles[bundle]}')
    return bundles[bundle]
  return (bundle,)

def make_path(method, path, experiment):
  '''Create a filepath based on the method, path, and experiment.'''
  import os
  import sys
  if method in ('plotter', 'vldb'):
    return os.path.join(path, f'{experiment}_data.json')
  print('Invalid method: ', method)
  sys.exit(1)

def configure_matplotlib(
    font_face='Roboto', font_size=20, legend_font_size=14, rows=1, target='paper'):
  '''Configure matplotlib.'''
  mpl.rcParams['axes.titlesize'] = font_size
  mpl.rcParams['axes.labelsize'] = font_size
  mpl.rcParams['figure.dpi'] = 80
  mpl.rcParams['figure.titlesize'] = 'medium'
  mpl.rcParams['font.family'] = font_face
  mpl.rcParams['font.size'] = font_size
  mpl.rcParams['legend.fontsize'] = legend_font_size
  mpl.rcParams['lines.markeredgewidth'] = 1.5
  mpl.rcParams['lines.markersize'] = 9
  mpl.rcParams['mathtext.fontset'] = 'cm'
  mpl.rcParams['savefig.dpi'] = 80
  mpl.rcParams['xtick.labelsize'] = font_size
  mpl.rcParams['ytick.labelsize'] = font_size

def format_roman(number):
  '''Convert a number into Roman numerals.'''
  table = {
      1000: 'M',
      900: 'CM',
      500: 'D',
      400: 'CD',
      100: 'C',
      90: 'XC',
      50: 'L',
      40: 'XL',
      10: 'X',
      9: 'IX',
      5: 'V',
      4: 'IV',
      1: 'I',
      }
  numerals = ''
  while number > 0:
    for denomination, string in table.items():
      if number >= denomination:
        numerals += string * (number // denomination)
        number %= denomination
        break
  return numerals

def generate_roman(start=1):
  '''Generate Roman numerals.'''
  while True:
    yield format_roman(start)
    start += 1

def get_figure_size(rows=1, cols=1, target='paper'):
  '''Generate the figure size given the parameters.'''
  if cols > 1:
    return (12, 5 * rows)
  return {
      'paper': (5, 5 * rows),
      'thesis': (25./3, 5 * rows),
      }[target]

def get_legend_specs(rows, cols, labels, target):
  '''Generate the legend specs given the parameters.'''
  legend_colcount = 5 if cols > 1 else {
      'paper': 2,
      'thesis': 4,
      }[target]
  legend_rowcount = (labels + legend_colcount - 1) // legend_colcount;
  legend_height = 0.3 * legend_rowcount + 0.6
  return legend_colcount, legend_rowcount, legend_height
