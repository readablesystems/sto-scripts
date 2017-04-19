#!/usr/bin/env python

from matplotlib import pyplot as plt
import numpy as np
import gv7_ubench as ub
import bench_color_map as cm
import json

draw_types = {
    'singleton': ['tl2', 'tl2+cb', 'tl2+reuse', 'gv7'],
    'reorder': ['none', 'tl2', 'tl2-lesser', 'tictoc', 'tictoc-o']
}

display_name = {
    'none'        : 'No Opacity',
    'tl2'         : 'TL2/O',
    'tl2+cb'      : 'TL2/O+CachedBound',
    'tl2+reuse'   : 'TL2/O+TIDReuse',
    'tl2+reuse-lesser' : 'TL2+TIDReuse-',
    'gv7'         : 'GV7/O',
    'noopt'       : 'TL2/O-ROOpt',
    'tl2-lesser'  : 'TL2-',
    'gv7-lesser'  : 'GV7-',
    'tictoc'      : 'TicToc',
    'tictoc-o'    : 'TicToc/O'
}

def exp_key_graph(sys,wl,nthr):
    return '{}/{}/{}'.format(sys,wl,nthr)

def process(results):
    processed_exps = {}
    for exp in ub.exp_names:
        wls = ub.contention[exp]
        sys_names = ub.opacity_types[exp]
        for sys in sys_names:
            for wl in wls:
                for nthr in ub.threads:
                    xput_series = []
                    abrts_series = []
                    hcos_series = []
                    for i in range(ub.ntrails):
                        t, a, h = results[ub.exp_key(sys,wl,nthr,i)]
                        xput_series.append(10.0/t)
                        abrts_series.append(a)
                        hcos_series.append(h)
                    xput_med = np.median(xput_series)
                    med_idx = xput_series.index(xput_med)
                    xput_min = np.amin(xput_series)
                    xput_max = np.amax(xput_series)

                    processed_exps[exp_key_graph(sys,wl,nthr)] = [[xput_min,xput_med,xput_max],
                        abrts_series[med_idx],
                        hcos_series[med_idx]]
    return processed_exps

def graph_opacity_ubench(processed_exps):
    save_names = {
        'singleton low': 'ubench_singleton_low.pdf',
        'singleton high': 'ubench_singleton_high.pdf',
        'low-small': 'lo-10.pdf',
        'low-large': 'lo-50.pdf',
        'high-small': 'hi-10.pdf',
        'high-large': 'hi-50.pdf'
    }

    for exp in ub.exp_names:

        wls = ub.contention[exp]

        for wl in wls:
            print 'Opacity -- {}'.format(wl)
            y = {}
            y_min = {}
            y_max = {}

            for sys in draw_types[exp]:
                y[sys] = []
                y_min[sys] = []
                y_max[sys] = []

            for nthr in ub.threads:
                print '\n{} threads:'.format(nthr)
                for sys in ub.opacity_types[exp]:
                    xput, abrts, hcos = processed_exps[exp_key_graph(sys,wl,nthr)]
                    if sys in draw_types[exp]:
                        y[sys].append(xput[1])
                        y_min[sys].append(xput[1]-xput[0])
                        y_max[sys].append(xput[2]-xput[1])
                    print '{}: x-{},a-{},h-{}'.format(display_name[sys], xput[1], abrts, hcos)

            N = len(ub.threads)
            width = 0.1
            ind = np.arange(N) + 2*width

            fig, ax = plt.subplots(figsize=(10, 6))
            rects = [ax.bar(ind+width*draw_types[exp].index(sys), y[sys], width,
                color=cm.color_map[sys], yerr=[y_min[sys], y_max[sys]]) for sys in draw_types[exp]]

            ax.set_ylabel('Throughput (Mtxns/sec)')
            ax.set_xticks(ind+width*len(draw_types[exp])/2)
            ax.set_xticklabels(['{} threads'.format(t) for t in ub.threads])

            ax.legend([r[0] for r in rects], [display_name[sys] for sys in draw_types[exp]], loc='best')
            plt.savefig(save_names[wl])

if __name__ == '__main__':
    with open('ubench_results.json', 'r') as infile:
        results = json.load(infile)
    processed_exps = process(results)
    graph_opacity_ubench(processed_exps)
