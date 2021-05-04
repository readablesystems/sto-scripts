#!/usr/bin/env python3

import matplotlib as mpl
import numpy as np
from matplotlib import pyplot as plt

import config
from plotter import GraphGlobalConstants

datasets ={
    'tpcc_baselines': {
        'o': 'OSTO',
        'tictoc': 'TSTO',
        'm': 'MSTO',
        #'o.scale': 'OSTO perfect scalability',
        #'tictoc.scale': 'TSTO perfect scalability',
        #'m.scale': 'MSTO perfect scalability',
        },
    'tpcc_mvcc': {
        'm': 'MSTO',
        'm.c': 'MSTO+CU',
        'm.s': 'MSTO+TS',
        'm.c.s': 'MSTO+CU+TS',
        },
    'tpcc_noncumu_factors': {
        'o-base': 'Baseline',
        'o-r': 'No contention regulation',
        'o-a': 'Slow allocator',
        'o-e': 'Inefficient aborts',
        'o-h': 'No hash indexes',
        },
    'semopt': {
        'o': 'OSTO',
        'o.c': 'OSTO+CU',
        'o.s': 'OSTO+TS',
        'o.c.s': 'OSTO+CU+TS',
        'tictoc': 'TSTO',
        'tictoc.c': 'TSTO+CU',
        'tictoc.s': 'TSTO+TS',
        'tictoc.c.s': 'TSTO+CU+TS',
        'm': 'MSTO',
        'm.c': 'MSTO+CU',
        'm.s': 'MSTO+TS',
        'm.c.s': 'MSTO+CU+TS',
        },
    }
columns = {
    'tpcc_baselines': 3,
    'tpcc_mvcc': 4,
    'tpcc_noncumu_factors': 5,
    'semopt': 6,
    }

for key in datasets:
    dataset = datasets[key]
    ncols = columns[key]
    handles = [
        plt.plot(
          [], [], marker=config.marker_mapping[key],
          color=GraphGlobalConstants.color(config.color_mapping[key]),
          ls='dotted' if key[-len('scale'):] == 'scale' else \
             config.linestyle_mapping.get(key, 'solid'))[0]
        for key in dataset.keys()]
    labels = list(dataset.values())
    for spine in plt.subplots()[1].spines.values():
      spine.set_visible(False)
    legend = plt.legend(handles, labels, ncol=ncols, frameon=False)

    legend.figure.canvas.draw()
    window = legend.get_window_extent()
    window = window.transformed(legend.figure.dpi_scale_trans.inverted())
    legend.figure.savefig('{}_legend.pdf'.format(key), dpi='figure', bbox_inches=window)
