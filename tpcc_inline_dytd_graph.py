#!/usr/bin/env python

import json,plot_helper
import tpcc_inline_dytd as exp
import bench_color_map as cm
import numpy as np
from matplotlib import pyplot as plt

g_threads = exp.threads
g_systems = exp.systems

def g_key(sys_name, workload, nthreads):
    return '/'.join((sys_name, workload, str(nthreads)))

def process(results):
    processed_exp = {}

    for sys in exp.systems:
        for cont in exp.levels:
            for tr in g_threads:
                xput_series = []
                abrts_series = []
                cabrts_series = []
                for n in range(exp.ntrails):
                    k = exp.key(sys,cont,tr,n)
                    xput,abrts,cabrts = results[k]

                    xput_series.append(xput)
                    abrts_series.append(abrts)
                    cabrts_series.append(cabrts)

                xput_med = np.median(xput_series)
                xput_min = np.amin(xput_series)
                xput_max = np.amax(xput_series)

                med_idx = xput_series.index(xput_med)

                rec = [[xput_min, xput_med, xput_max],
                       abrts_series[med_idx],
                       cabrts_series[med_idx]]

                processed_exp[g_key(sys,cont,tr)] = rec

    return processed_exp

graph_info_template = {
    'graph_title': 'TPC-C, {} contention',
    'x_label': '# threads',
    'y_label': 'Throughput (1000 txns/sec)',
    'series_names': ('TNonopaque', 'TSwiss', 'TAdaptive', 'TicToc'),
    'plot_colors': ('blue', 'green', 'red', 'grey'),
    'legends_on': True,
    'save_name': 'tpcc_inline_dytd_{}.pdf'
}

def pack_plotting_data(processed_results, cont):
    meta = graph_info_template.copy()
    common_x = g_threads
    y_serieses = []
    y_errors = []
    for sys in g_systems:
        series_data = []
        series_error_down = []
        series_error_up = []
        for tr in g_threads:
            res = processed_results[g_key(sys,cont,tr)]
            xput = res[0]
            series_data.append(xput[1]/1000.0)
            series_error_down.append((xput[1]-xput[0])/1000.0)
            series_error_up.append((xput[2]-xput[1])/1000.0)
        y_serieses.append(series_data)
        y_errors.append((series_error_down, series_error_up))
    meta['graph_title'] = meta['graph_title'].format(cont)
    meta['save_name'] = meta['save_name'].format(cont)

    return (meta, common_x, y_serieses, y_errors)

def draw_bars(meta_info, common_x, y_serieses, y_errors):
    fig, ax = plt.subplots(figsize=(10,6))

    N = len(common_x)
    width = 0.1
    ind = np.arange(N) + 2*width

    rects = []

    for i in range(len(g_systems)):
        r = ax.bar(ind+width*i, y_serieses[i], width,
            color=meta_info['plot_colors'][i],
            yerr=y_errors[i], error_kw=cm.ERROR_KW)
        rects.append(r)

    ax.set_title(meta_info['graph_title'])
    ax.set_ylabel(meta_info['y_label'])
    ax.set_xticks(ind + width*len(g_systems)/2)
    ax.set_xticklabels(['{} threads'.format(t) for t in common_x])
    ax.set_xlabel(meta_info['x_label'])

    if meta_info['legends_on']:
        ax.legend([r[0] for r in rects],
                  [meta_info['series_names'][i] for i in range(len(g_systems))],
                  loc='best')

    #plt.show()
    plt.savefig(meta_info['save_name'])

if __name__ == '__main__':
    with open(exp.RESULT_FILE, 'r') as rf:
        results = json.load(rf)
    processed_results = process(results)
    for cont in ('low', 'high'):
        data = pack_plotting_data(processed_results, cont)
        draw_bars(*data)
