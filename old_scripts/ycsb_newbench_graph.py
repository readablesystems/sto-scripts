#!/usr/bin/env python

import json,plot_helper
import ycsb_newbench as exp
import bench_color_map as cm
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt

FONT_SIZE = 22
    
mpl.rcParams['figure.figsize'] = [10, 6]
mpl.rcParams['figure.dpi'] = 80
mpl.rcParams['savefig.dpi'] = 80

mpl.rcParams['font.size'] = FONT_SIZE
mpl.rcParams['axes.titlesize'] = FONT_SIZE
mpl.rcParams['axes.labelsize'] = FONT_SIZE
mpl.rcParams['xtick.labelsize'] = FONT_SIZE
mpl.rcParams['ytick.labelsize'] = FONT_SIZE
mpl.rcParams['legend.fontsize'] = FONT_SIZE
mpl.rcParams['figure.titlesize'] = 'medium'

#g_threads = exp.threads
g_threads = [8,16,32,64,128]
g_systems = exp.systems
#g_systems = ['default', 'tictoc']

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
    'graph_title': 'YCSB-like workload, {} contention',
    'x_label': '# threads',
    'y_label': 'Throughput (Mtxns/sec)',
    'series_names': ('OCC', 'SwissTM', 'Adaptive', '2PL', 'TicToc'),
    'fill_colors': ('black', 'white', 'white', 'white', 'white'),
    #'edge_colors': ('blue', 'green', 'red', 'purple', 'grey'),
    'hatches': ('', '++', '///', 'xx', ''),
    #'series_names': ('OCC', 'TicToc'),
    #'plot_colors': ('blue', 'grey'),
    'legends_on': True,
    'save_name': '{}_{}_{}.pdf'
}

def pack_plotting_data(processed_results, cont):
    print "xput:"
    meta = graph_info_template.copy()
    if exp.NAME == 'fine_grain':
        meta['legends_on'] = False
    common_x = g_threads
    y_serieses = []
    y_errors = []
    for sys in g_systems:
        print sys
        series_data = []
        series_error_down = []
        series_error_up = []
        for tr in g_threads:
            res = processed_results[g_key(sys,cont,tr)]
            xput = res[0]
            series_data.append(xput[1]/1000000.0)
            series_error_down.append((xput[1]-xput[0])/1000000.0)
            series_error_up.append((xput[2]-xput[1])/1000000.0)
        print series_data
        y_serieses.append(series_data)
        y_errors.append((series_error_down, series_error_up))
    meta['graph_title'] = meta['graph_title'].format(cont)
    meta['save_name'] = meta['save_name'].format(exp.TYPE, exp.NAME, cont)

    return (meta, common_x, y_serieses, y_errors)

def pack_plotting_data_aborts(processed_results, cont):
    print "aborts:"
    meta = graph_info_template.copy()
    common_x = g_threads
    y_serieses = []
    for sys in g_systems:
        print sys
        series_data = []
        for tr in g_threads:
            res = processed_results[g_key(sys,cont,tr)]
            abrts = res[1]
            series_data.append(abrts)
        print series_data
        y_serieses.append(series_data)
    meta['graph_title'] = ''
    meta['y_label'] = 'Aborts (%)'
    meta['save_name'] = '{}_{}_{}_abort.pdf'.format(exp.TYPE, exp.NAME, cont)

    return (meta, common_x, y_serieses)

def draw_bars(meta_info, common_x, y_serieses, y_errors):
    fig, ax = plt.subplots(figsize=(10,6))

    N = len(common_x)
    width = 0.1
    ind = np.arange(N) + 2*width

    rects = []

    for i in range(len(g_systems)):
        r = ax.bar(ind+width*i, y_serieses[i], width,
            color=meta_info['fill_colors'][i],
            edgecolor='black',
            hatch=meta_info['hatches'][i],
            yerr=y_errors[i], error_kw=cm.ERROR_KW)
        rects.append(r)

    ax.set_ylabel(meta_info['y_label'])
    ax.set_ylim(ymin=0, ymax=2.0)
    ax.set_xticks(ind + width*len(g_systems)/2)
    ax.set_xticklabels(['{}'.format(t) for t in common_x])
    ax.set_xlabel(meta_info['x_label'])
    ax.xaxis.set_ticks_position('none')

    if meta_info['legends_on']:
        ax.legend([r[0] for r in rects],
                  [meta_info['series_names'][i] for i in range(len(g_systems))],
                  loc='best')

    plt.tight_layout()
    #plt.show()
    plt.savefig(meta_info['save_name'])

if __name__ == '__main__':
    with open(exp.RESULT_FILE, 'r') as rf:
        results = json.load(rf)
    processed_results = process(results)
    for cont in exp.levels:
        data = pack_plotting_data(processed_results, cont)
        draw_bars(*data)
        pack_plotting_data_aborts(processed_results, cont)
