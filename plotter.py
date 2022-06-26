#!/usr/bin/env python3

# Draw graphs from parsed experiment data

import collections
import datetime
import functools
import json
import math
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import optparse
import re

import config
import legend

class Plotter:
  image_format = 'no'
  show_error_bars = False
  show_legend = 'no'
  show_only = True
  write_timestamp = False

  PLOT_SPEC_DELIMITER = ','
  LINE_SPEC_DELIMITER = '/'

  expr_re = re.compile(
      r'^((?P<expr>\w+(\.\w+)*):)?(?P<bundle>(?P<cc>\w+)(?P<opts>([.-]\w+)*)?)(?P<toggles>(\+\w+)*)$')
  spec_re = re.compile(r'^(?P<name>[^=]+)=((?P<rows>\d+)x(?P<cols>\d+):)?(?P<specs>.+)$')

  def __init__(self, specification, scale='1'):
    '''Create a plotter for a given plot specification.'''
    match = Plotter.spec_re.match(specification)
    assert match, 'Invalid specification detected: {specification}'
    assert (not match.group('rows')) == (not match.group('cols')), \
           'Row and column specifications should either be both set or neither set.'

    self.name = match.group('name')
    self.specs = match.group('specs').split(Plotter.PLOT_SPEC_DELIMITER)
    self.rows = int(match.group('rows') if match.group('rows') else 1)
    self.cols = int(match.group('cols') if match.group('cols') else len(self.specs))

    assert self.rows > 0, 'Must specify at least one row.'
    assert self.cols > 0, 'Must specify at least one column.'
    assert self.rows * self.cols == len(self.specs), \
           'Need exactly {} specifications for {} rows and {} columns.'.format(
               self.rows * self.cols, self.rows, self.cols) + \
           f'\r\n  Currently have {len(self.specs)}: {", ".join(self.specs)}'

    self.specs = np.reshape(self.specs, (self.rows, self.cols))
    self.data = collections.defaultdict(dict)

    self.scale_prefix, self.scale_value = \
        ('auto', 1) if scale == 'auto' else Plotter.compute_scale_pair(scale)

  @staticmethod
  def compute_scale_pair(scale):
    '''Return the (prefix, value) pair of the scale factor.'''
    return {
        '1': ('', 1),
        'K': ('K', 1e3),
        'M': ('M', 1e6),
        'B': ('B', 1e9),
        }[scale]

  def draw_line(self, ax, series, name, toggles=[]):
    '''Plot the data series as a line on ax.'''
    values = {}
    for xval, yvals in series.items():
      if xval.isnumeric():
        xval = float(xval)
      if np.array(yvals).any():
        yvals = [y for y in yvals if y is not None]
        y_med = np.median(yvals) / self.scale_value
        y_min = np.amin(yvals) / self.scale_value
        y_max = np.amax(yvals) / self.scale_value
        values[xval] = (y_min, y_med, y_max)

    values = dict(sorted(values.items()))  # Sort data series
    x_series, y_series, y_error = [], [], []
    for xval, yvals in values.items():
      x_series.append(xval)
      y_series.append(yvals[1])
      y_error.append((yvals[1] - yvals[0], yvals[2] - yvals[1]))

    cc, *opts = name.split('.')
    style = {
        'markeredgewidth': 1.5,
        'markersize': 10,
        }
    style.update(legend.cc_style[cc])
    for opt in opts:
      style.update(legend.cc_opts_style[opt])
    for toggle in toggles:
      style.update(legend.cc_toggle_style[toggle])
    if max(style['color']) > 1:
      style['color'] = tuple(c / 255 for c in style['color'])

    if Plotter.show_error_bars:
      return ax.errorbar(x_series, y_series, y_error, **style)
    return ax.plot(x_series, y_series, **style)

  @property
  def file_timestamp(self):
    '''Get the timestamp part of the output filename.'''
    import datetime
    if Plotter.show_legend == 'only':
      return 'legend'
    elif Plotter.write_timestamp:
      now = datetime.datetime.now()
      return '{:04d}{:02d}{:02d}{:02d}'.format(now.year, now.month, now.day, now.hour)
    return 'latest'

  @staticmethod
  def generate_bundles(specs):
    '''Convert a spec string into individual bundle specs.'''
    last_expr = None
    for bundle in specs.split(Plotter.LINE_SPEC_DELIMITER):
      match = Plotter.expr_re.match(bundle)
      assert match, f'Invalid line {bundle} in plot specification: {specs}'

      expr = match.group('expr')
      bundle = match.group('bundle')
      toggles = match.group('toggles')
      toggles = toggles[1:].split('+') if toggles else []

      assert last_expr or expr, 'First bundle must have an explicit experiment!'
      expr = expr or last_expr
      yield (expr, bundle, toggles)
      last_expr = expr

  def load(self, path):
    '''Load data from a given path.'''
    if not config.quiet:
      print(f'Loading data for plot "{self.name}"...')

    experiments = set()
    for row in self.specs:
      for specs in row:
        for expr, *_ in Plotter.generate_bundles(specs):
          experiments.add(expr)

    for experiment in experiments:
      # Check if already read and cached
      cached = experiment in self.data

      if cached:
        if not config.quiet:
          print(f'  Experiment "{experiment}" is cached.')
      else: # Load from file
        if not config.quiet:
          print(f'  Reading data for experiment "{experiment}".')
        expr_path = experiment.split('.')
        load_path = config.make_path('plotter', path, expr_path[0])
        with open(load_path, 'r') as fin:
          data = json.load(fin)

        # Find experiment part
        src = data
        for p in expr_path:
          src = src.get(p)
          assert src, f'Empty source for experiment path: {experiment}'
        self.data[experiment].update(src)

    # Make sure we have all the data we need
    max_yval = 0
    for row in self.specs:
      for specs in row:
        for expr, bundle, _ in Plotter.generate_bundles(specs):
          for key in config.get_lines(bundle):
            if key not in self.data[expr]:
              # Be helpful and look up the key in other experiments loaded
              other_expr = ()
              for e, d in self.data.items():
                if key in d:
                  other_expr += (e,)
              message = f'Key "{key}" missing in data for "{expr}".'
              if other_expr:
                message += '\r\n  but "{}" exists in these experiments: "{}"'.format(
                    key, '", "'.join(other_expr))
              assert key in self.data[expr], message
            for data in self.data[expr][key].values():
              max_yval = functools.reduce(lambda acc, y: \
                  acc if y is None else max(acc, y), data, max_yval)
    if self.scale_prefix == 'auto':
      if max_yval < 2e3:
        self.scale_prefix, self.scale_value = Plotter.compute_scale_pair('1')
      elif max_yval < 2e6:
        self.scale_prefix, self.scale_value = Plotter.compute_scale_pair('K')
      elif max_yval >= 2e9:
        self.scale_prefix, self.scale_value = Plotter.compute_scale_pair('B')
      else:
        self.scale_prefix, self.scale_value = Plotter.compute_scale_pair('M')

  def plot(self, target):
    '''Plot this figure.'''
    import os

    config.configure_matplotlib(rows=self.rows, target=target)
    subplot_number = config.generate_roman()

    fig_kwargs = {}
    fig_kwargs['figsize'] = config.get_figure_size(
        rows=self.rows, cols=self.cols, target=target)
    fig, ax = plt.subplots(
        self.rows, self.cols,
        gridspec_kw={'wspace': 0.0}, sharey=True,
        **fig_kwargs)

    ax = np.reshape(ax, (self.rows, self.cols))

    labels = []
    lines = []
    ymax = []
    for row in zip(ax, self.specs):
      ymax.append(0)
      for col, (axis, specs) in enumerate(zip(*row)):
        xvals = set()
        for expr, bundle, toggles in Plotter.generate_bundles(specs):
          for key in config.get_lines(bundle):
            for xval, yval in self.data[expr][key].items():
              if xval.isnumeric():
                xvals.add(int(xval))
              nonnull_y = [y for y in yval if y is not None]
              if nonnull_y:
                ymax[-1] = max(ymax[-1], max(nonnull_y))
            line = self.draw_line(axis, self.data[expr][key], key, toggles=toggles)[0]
            if key not in labels and 'secondary' not in toggles:
              labels.append(key)
              lines.append(line)
        axis.ticklabel_format(style='plain', useOffset=False)
        #xvals = tuple(filter(lambda x: x in (1, 16, 32, 48, 64), xvals))
        #xticker = mpl.ticker.FixedLocator(xvals)
        xticker = mpl.ticker.FixedLocator((1, 16, 32, 48, 64))
        axis.xaxis.set_major_locator(xticker)
        axis.xaxis.set_minor_locator(mpl.ticker.MultipleLocator(4))
        axis.xaxis.grid(visible=True, which='major')
        axis.yaxis.grid(visible=True, which='major')
        #axis.set_xlabel('Threads', fontsize=mpl.rcParams['font.size'] - 4)
        #axis.set_title(f'(${next(subplot_number).lower()}$)')
        axis.set_xlabel(f'Threads\r\n(${next(subplot_number).lower()}$)', fontsize=mpl.rcParams['font.size'] - 4)
        if col == 0:
          axis.set_ylabel(f'{self.scale_prefix}txns/sec', fontsize=mpl.rcParams['font.size'] - 4)
        axis.set_ylim(auto=True, ymin=0)

    plt.tight_layout()

    if Plotter.show_legend != 'no':
      # Do some resizing calculations
      legend_colcount, legend_rowcount, legend_height = \
          config.get_legend_specs(self.rows, self.cols, len(labels), target)
      fig.set_figheight(fig.get_figheight() + legend_height)
      fig.subplots_adjust(bottom=(0.6 + legend_height) / fig.get_figheight())

      # Add legend
      labels = [legend.series_to_name(label) for label in labels]
      if Plotter.show_legend == 'only':
        plt.close(fig)
        fig = plt.figure(figsize=(fig_kwargs['figsize'][0], legend_height))
      plt.figlegend(
          lines, labels, fancybox=True, loc='lower center', ncol=legend_colcount)

    #plt.tight_layout()
    if Plotter.show_only:
      plt.show()
    else:
      os.makedirs('figs', exist_ok=True)
      filename = f'{self.name}_{self.file_timestamp}.{Plotter.image_format}'
      filename = os.path.join(os.getcwd(), 'figs', filename)
      if not config.quiet:
        print(f'Saving to {filename}')
      plt.savefig(filename)

    plt.close(fig)

def main():
  import threading
  usage = '''\
Usage: %prog [options] name:[(rows)x(cols):]plot[,plot2,...,plotN]

The (rows)x(cols) specification is optional and defaults to a single row of N
subplots (i.e. 1xN). N must equal (rows * cols) at all times, however.

Examples:
  # Plots line1 in a single plot on a 1x1 grid
  %prog myplot=line1

  # Plots two graphs, one with 3 rows and 2 columns, and a 1x2 version of plot1,plot2
  # The 3x2 contains line11.1 and line11.2 in the first subplot and the rest have
  # only one line.
  %prog my3x2plot=3x2:line11.1/line11.2,line12,line21,line22,line31,line32 my1x2plot=line1,line2
'''
  parser = optparse.OptionParser(usage=usage)
  parser.add_option('-c', '--concurrency', action='store', default=0,
                    dest='concurrency', type='int',
                    help='Concurrency amount. 1 to turn off concurrency, 0 for unlimited.')
  parser.add_option('-e', '--error-bars', action='store_true', default=False,
                    dest='error_bars',
                    help='Toggle to turn on error bars in the plots.')
  parser.add_option('-f', '--format', action='store',
                    choices=('paper', 'thesis'),
                    default='paper', dest='format', type='choice',
                    help='Publication format in which the figure(s) will be used.')
  parser.add_option('-l', '--legend', action='store', default='no',
                    choices=('no', 'yes', 'only'), dest='legend', type='choice',
                    help='Toggle legends in the plots.')
  parser.add_option('-p', '--path', action='store', default='experiments/data/',
                    dest='path', type='str',
                    help='Source directory of stored parsed data.')
  parser.add_option('-q', '--quiet', action='store_true', default=False,
                    dest='quiet',
                    help='Shh don\'t scare the CPUs.')
  parser.add_option('-s', '--save', action='store',
                    choices=('no', 'pdf', 'png'),
                    default='no', dest='save', type='choice',
                    help='Save file type or "no".')
  parser.add_option('-t', '--timestamped', action='store_true', default=False,
                    dest='timestamped',
                    help='Whether to timestamp the file name.')
  parser.add_option('-x', '--scale-factor', action='store',
                    choices=('auto', '1', 'K', 'M', 'B'),
                    default='auto', dest='scale', type='choice',
                    help='Scale factor for the y-axis. The auto option selects '\
                       + 'M by default, but will adjust based on the max Y-value.')

  options, args = parser.parse_args()

  if options.save != 'no':
    Plotter.image_format = options.save
    Plotter.show_only = False
  config.quiet = options.quiet
  Plotter.show_error_bars = options.error_bars
  Plotter.show_legend = options.legend
  Plotter.write_timestamp = options.timestamped

  if len(args) == 0:
    parser.error('Please select at least one plot specification.');

  plotters = [None] * len(args)
  threads = [None] * len(args)
  def plot(arg, index):
    '''Thread runner function.'''
    if options.concurrency > 0 and index >= options.concurrency:
      threads[index - options.concurrency].join()
    plotters[index] = Plotter(arg, options.scale)
    plotters[index].load(options.path)

  for index, arg in enumerate(args):
    threads[index] = threading.Thread(target=plot, args=(arg, index))
    threads[index].start()

  print(f'Spawned {len(threads)} worker threads to load data.')

  for t, plotter in zip(threads, plotters):
    t.join()
    plotter.plot(options.format)  # matplotlib can only plot on main thread
    del plotter

if __name__ == '__main__':
  main()
