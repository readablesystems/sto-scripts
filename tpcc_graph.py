#!/usr/bin/env python

from matplotlib import pyplot as plt
import numpy as np
import bench_color_map as cm
import json,tpcc

results = None

def settings():
    global results
    results = []

    with open('tpcc_4wh_results.json', 'r') as input_file:
        results.append(json.load(input_file))
    with open('tpcc_swh_results.json', 'r') as input_file:
        results.append(json.load(input_file))

def graph_all_bars(results, systems, filename):
    y = {}
    y_min = {}
    y_max = {}
    abrts = {}

    for s in systems:
        y[s] = []
        y_min[s] = []
        y_max[s] = []
        abrts[s] = []

        for tr in tpcc.threads:
            series = []
            abrt_series = []
            for n in range(tpcc.ntrails):
                xput = results[tpcc.exp_key(s,tr,n)][0]
                abrt = results[tpcc.exp_key(s,tr,n)][1]
                series.append(xput/1000.0)
                abrt_series.append(abrt)
            xput_min = np.amin(series)
            xput_max = np.amax(series)
            xput_med = np.median(series)

            y[s].append(xput_med)
            y_min[s].append(xput_med - xput_min)
            y_max[s].append(xput_max - xput_med)
            abrts[s].append(abrt_series[series.index(xput_med)])

    N = len(tpcc.threads)
    width = 0.1
    ind = np.arange(N) + 2*width

    print 'graph: {}'.format(filename)
    for i in range(N):
        print '\n{} threads:'.format(tpcc.threads[i])
        for sys in systems:
            print '{}: x-{}, a-{}%'.format(sys, y[sys][i], abrts[sys][i])

    fig, ax = plt.subplots(figsize=(18,6))
    t_rects = [ax.bar(ind+width*systems.index(s), y[s], width,
        color=cm.color_map[s],
        yerr=[y_min[s], y_max[s]], error_kw=cm.ERROR_KW) for s in systems]

    ax.set_ylabel('Throughput (x1000 txns/sec)')
    ax.set_xticks(ind+width*len(systems)/2)
    ax.set_xticklabels(['{} threads'.format(t) for t in tpcc.threads])

    #box = ax.get_position()
    #ax.set_position([box.x0, box.y0, box.width*0.85, box.height])
    ax.legend([r[0] for r in t_rects], systems, loc='best')#, bbox_to_anchor=(1, 0.5))

    fig.tight_layout()

    plt.savefig(filename)

if __name__ == '__main__':
    settings()
    graph_all_bars(results[0], tpcc.systems, 'tpcc_4wh.pdf')
    print ''
    graph_all_bars(results[1], tpcc.systems, 'tpcc_swh.pdf')
    print ''
    graph_all_bars(results[1], tpcc.gtid_systems, 'tpcc_gtid.pdf')
