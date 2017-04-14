#!/usr/bin/env python

import subprocess,json,optparse
import numpy as np
import sys_taskset as tsk
from matplotlib import pyplot as plt
from sto import profile_parser as parser
from time import sleep as sys_sleep

DRY_RUN = False
TEST_DIR = 'test_dir'

# Experiment configuration
ntrails = 5

exp_names = ['singleton', 'reorder']

opacity_types = {
    'singleton': ['tl2', 'tl2+cb', 'tl2+reuse', 'gv7'],
    'reorder': ['none', 'tl2', 'noopt', 'tl2-lesser', 'tl2+reuse', 'tl2+reuse-lesser', 'tictoc', 'tictoc-o']
}
contention = {
    'singleton': ['singleton low', 'singleton high'],
    'reorder': ['low-small', 'low-large', 'high-small', 'high-large']
}

draw_types = {
    'singleton': ['tl2', 'tl2+cb', 'tl2+reuse', 'gv7'],
    'reorder': ['none', 'tl2', 'tl2-lesser', 'tictoc', 'tictoc-o']
}

threads = [4,8,12]

color_map = {
    'none': (0,0,0),
    'tl2': (153,216,201),
    'tl2+cb': (152,78,163),
    'tl2+reuse': (251,180,174),
    'tl2+reuse-lesser': (44, 160, 44),
    'gv7': (227,26,28),
    'tl2-lesser': (31,119,180),
    'gv7-lesser': (255, 127, 14),
    'tictoc': (174, 199, 232),
    'tictoc-o': (74,59,276),
    'noopt': (152, 223, 138)
}

for key, value in color_map.iteritems():
    r, g, b = value
    color_map[key] = (r/255., g/255., b/255.)

prog_name = {
    'none'        : 'concurrent-tl2',
    'tl2'         : 'concurrent-tl2',
    'tl2+cb'      : 'concurrent-cb',
    'tl2+reuse'   : 'concurrent-rt',
    'tl2+reuse-lesser' : 'concurrent-rt-lesser',
    'gv7'         : 'concurrent-gv7',
    'noopt'       : 'concurrent-tl2-noopt',
    'tl2-lesser'  : 'concurrent-tl2-lesser',
    'gv7-lesser'  : 'concurrent-gv7-lesser',
    'tictoc'      : 'concurrent-tictoc',
    'tictoc-o'    : 'concurrent-tictoc'
}

opts_contention = {
    'low-small': ' 11 array --ntrans=10000000 --opspertrans=10 --skew=0.1 --readonlypercent=0.9',
    'low-large': ' 11 array --ntrans=10000000 --opspertrans=10 --opspertrans_ro=50 --skew=0.1 --readonlypercent=0.9',
    'singleton low': ' 10 array --ntrans=10000000 --skew=0.0',
    'singleton med': ' 10 array --ntrans=10000000 --skew=1.0',
    'singleton high': ' 10 array --ntrans=10000000 --skew=1.2',
    'high-small': ' 8 array --ntrans=10000000 --opspertrans=9 --readonlypercent=0.9',
    'high-large': ' 8 array --ntrans=10000000 --opspertrans=9 --opspertrans_ro=49 --readonlypercent=0.9'
}

def run_single(opacity_type, contention, nthreads):
    global DRY_RUN
    cmd = '{}/{}'.format(TEST_DIR, prog_name[opacity_type])
    cmd += opts_contention[contention]

    if opacity_type == 'none' or opacity_type == 'tictoc':
        cmd = cmd.replace('array', 'array-nonopaque')

    cmd += ' --nthreads={}'.format(nthreads)
    cmd = tsk.taskset_cmd(nthreads) + ' ' + cmd

    print cmd

    if DRY_RUN:
        return (0.0, 0.0, 0.0)

    sys_sleep(1)

    out = subprocess.check_output(cmd.split(' '), stderr=subprocess.STDOUT)

    time = parser.extract('time', out)
    aborts = parser.extract('aborts', out)
    hcos = parser.extract('hcos', out)

    return (time, aborts, hcos)

def exp_key(opacity, contention, nthreads, ntrail):
    return '{}/{}/{}/{}'.format(opacity, contention, nthreads, ntrail)

# Compare results at 4, 8, 16 threads
def run_benchmark():
    global DRY_RUN
    all_results = {}

    for e in exp_names:
        for o in opacity_types[e]:
            for c in contention[e]:
                for t in threads:
                    for n in range(ntrails):
                        result = run_single(o,c,t)
                        if DRY_RUN:
                            continue
                        all_results[exp_key(o,c,t,n)] = result

    return all_results

def graph_all_bars(all_results, contention, metric_func, y_title, title, filename):
    c = contention
    y = {}
    y_min = {}
    y_max = {}

    for o in opacity_types:
        for t in threads:
            metric_series = []
            for n in range(ntrails):
                metric_series.append(metric_func(all_results[exp_key(o,c,t,n)]))
            metric_min = np.amin(metric_series)
            metric_max = np.amax(metric_series)
            metric_med = np.median(metric_series)

            if not o in y:
                y[o] = []
            if not o in y_min:
                y_min[o] = []
            if not o in y_max:
                y_max[o] = []
            y[o].append(metric_med)
            y_min[o].append(metric_med - metric_min)
            y_max[o].append(metric_max - metric_med)

    N = len(threads)
    width = 0.1
    ind = np.arange(N) + 2*width

    fig, ax = plt.subplots(figsize=(10, 6))
    t_rects = [ax.bar(ind+width*opacity_types.index(o), y[o], width, color=color_map[o], yerr=[y_min[o], y_max[o]]) for o in opacity_types]

    ax.set_title(title)
    ax.set_ylabel(y_title)
    ax.set_xticks(ind+width*len(opacity_types)/2)
    ax.set_xticklabels(['{} threads'.format(t) for t in threads])

    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width*0.85, box.height])
    ax.legend([r[0] for r in t_rects], opacity_types, loc='center left', bbox_to_anchor=(1, 0.5))

    #plt.show()
    plt.savefig(filename)

def calc_throughput(input_tuple):
    time, aborts, hcos = input_tuple
    return (10.0 / time)

def calc_aborts(input_tuple):
    time, aborts, hcos = input_tuple
    return aborts

def calc_hcos(input_tuple):
    time, aborts, hcos = input_tuple
    return hcos

def graph_throughput(all_results, contention):
    graph_all_bars(all_results, contention, calc_throughput,
        y_title='Throughput (Mtxns/sec)',
        title='Throughput comparison of reordering schemes\n{} contention -- large RO txns'.format(contention),
        filename='throughput-{}-contention.png'.format(contention.replace(' ','')))

def graph_aborts(all_results, contention):
    graph_all_bars(all_results, contention, calc_aborts,
        y_title='Abort rate (%)',
        title='Abort rates of reordering schemes (lowers are better)\n{} contention'.format(contention),
        filename='aborts-{}-contention.png'.format(contention.replace(' ','')))

def graph_hcos(all_results, contention):
    graph_all_bars(all_results, contention, calc_hcos,
        y_title='# HCOs',
        title='Number of Hard Checks (HCOs)\n{} contention'.format(contention),
        filename='hcos-{}-contention.png'.format(contention.replace(' ','')))

def main():
    global DRY_RUN

    parser = optparse.OptionParser()
    parser.add_option('-l', action="store", dest="load_file", default='')
    parser.add_option('-d', action="store_true", dest="dry_run", default=False)
    parser.add_option('-a', action="store_true", dest="add_to_file", default=False)

    options, args = parser.parse_args()

    DRY_RUN = options.dry_run

    results_f = {}
    results_r = {}

    if options.load_file != '':
        with open(options.load_file, 'r') as input_file:
            results_f = json.load(input_file)

    if options.add_to_file or options.load_file == '':
        results_r = run_benchmark()
        print 'ALL DONE'
        if DRY_RUN:
            exit()

        results = results_f.copy()
        results.update(results_r)
        with open('gv7_results.json', 'w') as outfile:
            json.dump(results, outfile, indent=4, sort_keys=True)
    else:
        results = results_f

    # plot graph(s)
    #for c in contention:
    #    graph_throughput(results, c)
    #    graph_aborts(results, c)

if __name__ == '__main__':
    main()
