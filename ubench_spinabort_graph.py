#!/usr/bin/env python

import json
import ubench_spinabort as exp
import bench_color_map as cm
import numpy as np
from matplotlib import pyplot as plt

g_threads = [4,12]
g_systems = exp.systems

display_name = {
    'none': 'Spin-on-locked',
    'abort': 'Abort-on-locked'
}

graph_names = ['Small txns', 'Large txns']

g_wl_ticks = [
    ['l-small-4', 'h-small-4', 'l-small-12', 'h-small-12'], # x-axis of graph-1
    ['l-large-4', 'h-large-4', 'l-large-12', 'h-large-12']  # ... of graph-2
]

g_savenames = ['ubench_spin_10.pdf', 'ubench_spin_50.pdf']

# XXX more software engineering later...
def process(results):
    processed_exp = {}

    for sys in exp.systems:
        for wl in exp.wls:
            for tr in g_threads:
                xput_series = []
                abrts_series = []
                hcos_series = []
                for n in range(exp.ntrails):
                    k = exp.key(sys,wl,tr,n)
                    xput,abrts,hcos = results[k]

                    xput_series.append(xput)
                    abrts_series.append(abrts)
                    hcos_series.append(hcos)

                xput_med = np.median(xput_series)
                xput_min = np.amin(xput_series)
                xput_max = np.amax(xput_series)

                med_idx = xput_series.index(xput_med)

                rec = [[xput_min, xput_med, xput_max],
                       abrts_series[med_idx],
                       hcos_series[med_idx]]

                processed_exp[g_key(sys,wl,tr)] = rec

    return processed_exp

def wl_display_name(wl):
    cont, tsize, nthreads = wl.split('-')
    dname = None
    if cont == 'l':
        dname = 'high'
    else:
        dname = 'low'
    dname += '-contention\n@{} threads'.format(nthreads)
    return dname

def draw(processed_exp):
    for i in range(len(g_savenames)):
        g_wls = g_wl_ticks[i]
        savename = g_savenames[i]

        print '{}:'.format(graph_names[i])

        y = {}
        y_min = {}
        y_max = {}

        for sys in g_systems:
            y[sys] = []
            y_min[sys] = []
            y_max[sys] = []

        for wl in g_wls:
            cont, tsize, thr = wl.split('-')
            print '\n## {}@{}thr ##'.format(cont, thr)
            exp_wl = '-'.join((cont, tsize))
            nthr = int(thr)

            for sys in g_systems:
                xput, abrts, hcos = processed_exp[g_key(sys,exp_wl,nthr)]
                y[sys].append(xput[1]/1000.0)
                y_min[sys].append((xput[1]-xput[0])/1000.0)
                y_max[sys].append((xput[2]-xput[1])/1000.0)
                print '{}: x-{}, a-{}, h-{}'.format(display_name[sys], xput[1], abrts, hcos)

        N = len(g_wls)
        width = 0.1
        ind = np.arange(N) + 2*width

        fig, ax = plt.subplots(figsize=(10,6))
        rects = [ax.bar(ind+width*g_systems.index(sys), y[sys], width,
            color=cm.color_map[sys],
            yerr=[y_min[sys],y_max[sys]], error_kw=cm.ERROR_KW) for sys in g_systems]

        ax.set_ylabel('Throughput (x1000 txns/sec)')
        ax.set_xticks(ind+width*len(g_systems)/2)
        ax.set_xticklabels(wl_display_name(wl) for wl in g_wls)
        if i == 0:
            ax.legend([r[0] for r in rects], [display_name[sys] for sys in g_systems], loc='best')

        plt.savefig(savename)

if __name__ == '__main__':
    with open(exp.RESULT_FILE, 'r') as rf:
        results = json.load(rf)
    processed_exp = process(results)
    draw(processed_exp)
