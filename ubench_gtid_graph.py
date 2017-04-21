#!/usr/bin/env python

import json,plot_helper
import ubench_gtid as exp
import sys_taskset as tsk
import bench_color_map as cm
import numpy as np
from matplotlib import pyplot as plt

g_threads = exp.threads
g_systems = exp.systems

display_name = {
    'none': 'w/o global counter',
    'gtid': 'w/ global counter'
}

graph_names = ['Tiny txns', 'Small txns']

g_wl_ticks = [
    [], # x-axis of graph-1
    []  # ...    of graph-2
]

for c in ['u', 'c']:
    for t in g_threads:
        g_wl_ticks[0].append('{}-tiny-{}'.format(c, t))
        g_wl_ticks[1].append('{}-small-{}'.format(c, t))
    if c == 'u':
        g_wl_ticks[0].append('sep')
        g_wl_ticks[1].append('sep')

g_savenames = ['ubench_gtid_singleton.pdf', 'ubench_gtid_10.pdf']

def g_key(system_name, workload, nthreads):
    return '/'.join((system_name, workload, str(nthreads)))

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
    if wl == 'sep':
        return ''
    cont, tsize, nthreads = wl.split('-')
    return tsk.print_real_threads(int(nthreads))

def draw(processed_exp):
    for i in range(len(g_savenames)):
        g_wls = g_wl_ticks[i]
        savename = g_savenames[i]

        if i > 0:
            print '@'
        print savename

        y = {}
        y_min = {}
        y_max = {}

        for sys in g_systems:
            y[sys] = []
            y_min[sys] = []
            y_max[sys] = []

        for wl in g_wls:
            if wl == 'sep':
                separator = True
            else:
                separator = False
            
            if not separator:
                cont, tsize, thr = wl.split('-')
                print '{}@{}thr'.format(cont, thr)
                exp_wl = '-'.join((cont, tsize))
                nthr = int(thr)

            for sys in g_systems:
                if separator:
                    xput = [0,0,0]
                else:
                    xput, abrts, hcos = processed_exp[g_key(sys,exp_wl,nthr)]
                y[sys].append(xput[1]/1000000.0)
                y_min[sys].append((xput[1]-xput[0])/1000000.0)
                y_max[sys].append((xput[2]-xput[1])/1000000.0)
                if not separator:
                    print '{}: x-{}, a-{}, h-{}'.format(display_name[sys], xput[1], abrts, hcos)

        N = len(g_wls)
        width = 0.1
        ind = np.arange(N) + 2*width

        fig, ax = plt.subplots(figsize=(7,4))
        rects = [ax.bar(ind+width*g_systems.index(sys), y[sys], width,
            color=cm.color_map[sys],
            yerr=[y_min[sys],y_max[sys]], error_kw=cm.ERROR_KW) for sys in g_systems]

        first_tick_locations = ind+width*len(g_systems)/2
        ax.set_ylabel('Throughput (Mtxns/sec)')
        ax.set_xticks(first_tick_locations)
        ax.set_xticklabels(wl_display_name(wl) for wl in g_wls)

        plot_helper.second_xtick_labels(fig, ax, first_tick_locations, ['low contention', 'high contention'])

        if i == 0:
            ax.legend([r[0] for r in rects], [display_name[sys] for sys in g_systems], loc='best')

        plt.savefig(savename)

if __name__ == '__main__':
    with open(exp.RESULT_FILE, 'r') as rf:
        results = json.load(rf)
    processed_exp = process(results)
    draw(processed_exp)
