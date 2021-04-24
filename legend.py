#!/usr/bin/env python3

import matplotlib as mpl
import numpy as np
from matplotlib import pyplot as plt

import config
from plotter import GraphGlobalConstants

datasets ={
    'baselines': {
        'o': 'OSTO',
        'tictoc': 'TSTO',
        'm': 'MSTO',
        #'o.scale': 'OSTO perfect scalability',
        #'tictoc.scale': 'TSTO perfect scalability',
        #'m.scale': 'MSTO perfect scalability',
        },
    'factors': {
        'o-base': 'Baseline',
        'o-r': 'No contention regulation',
        'o-a': 'Slow allocator',
        'o-e': 'Inefficient aborts',
        'o-h': 'No hash indexes',
        },
    }
dataset = datasets['factors']
columns = 5

handles = [
    plt.plot(
      [], [], marker=config.marker_mapping[key],
      color=GraphGlobalConstants.color(config.color_mapping[key]),
      ls='dotted' if key[-len('scale'):] == 'scale' else 'solid')[0]
    for key in dataset.keys()]
labels = list(dataset.values())
for spine in plt.subplots()[1].spines.values():
  spine.set_visible(False)
legend = plt.legend(handles, labels, ncol=columns, frameon=False)

legend.figure.canvas.draw()
window = legend.get_window_extent()
window = window.transformed(legend.figure.dpi_scale_trans.inverted())
legend.figure.savefig('legend.pdf', dpi='figure', bbox_inches=window)
