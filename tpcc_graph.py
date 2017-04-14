#!/usr/bin/env python

from matplotlib import pyplot as plt
import numpy as np
import json,tpcc

tableau20 = None
results = None

def settings():
    # These are the "Tableau 20" colors as RGB.  
    global tableau20
    global results
    tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),  
                 (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),  
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),  
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),  
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]  
  
    # Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts.  
    for i in range(len(tableau20)):  
        r, g, b = tableau20[i]  
        tableau20[i] = (r / 255., g / 255., b / 255.)

    with open('tpcc_results.json', 'r') as input_file:
        results = json.load(input_file)

def graph_all_bars(results):
    y = {}
    y_min = {}
    y_max = {}

    for s in tpcc.systems:
        y[s] = []
        y_min[s] = []
        y_max[s] = []

        for tr in tpcc.threads:
            series = []
            for n in range(tpcc.ntrails):
                series.append(results[tpcc.exp_key(s,tr,n)]/1000.0)
            xput_min = np.amin(series)
            xput_max = np.amax(series)
            xput_med = np.median(series)

            y[s].append(xput_med)
            y_min[s].append(xput_med - xput_min)
            y_max[s].append(xput_max - xput_med)

    N = len(tpcc.threads)
    width = 0.1
    ind = np.arange(N) + 2*width

    fig, ax = plt.subplots(figsize=(25,6))
    t_rects = [ax.bar(ind+width*tpcc.systems.index(s), y[s], width,
        color=tableau20[tpcc.systems.index(s)],
        yerr=[y_min[s], y_max[s]]) for s in tpcc.systems]

    ax.set_ylabel('Throughput (x1000 txns/sec)')
    ax.set_xticks(ind+width*len(tpcc.systems)/2)
    ax.set_xticklabels(['{} threads'.format(t) for t in tpcc.threads])

    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width*0.85, box.height])
    ax.legend([r[0] for r in t_rects], tpcc.systems, loc='center left', bbox_to_anchor=(1, 0.5))

    plt.show()

if __name__ == '__main__':
    settings()
    graph_all_bars(results)
