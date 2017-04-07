#!/usr/bin/env python

import subprocess,json,optparse
import numpy as np
from matplotlib import pyplot as plt
from sto import profile_parser as parser

DRY_RUN = False

# Experiment configuration
ntrails = 5
opacity_types = ['none', 'tl2', 'gv7', 'tl2-lesser', 'gv7-lesser', 'tictoc']
contention = ['high']
threads = [4,8,16]

color_map = {
    'none': (0,0,0),
    'tl2': (153,216,201),
    'tl2+cb': (152,78,163),
    'tl2+reuse': (251,180,174),
    'gv7': (227,26,28),
    'tl2-lesser': (31,119,180),
    'gv7-lesser': (255, 127, 14),
    'tictoc': (174, 199, 232),
    'noopt': (0,0,0)
}

for key, value in color_map.iteritems():
    r, g, b = value
    color_map[key] = (r/255., g/255., b/255.)

sys_info = {
    'cpu_lists': [[0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,38,40,42,44,46],
        [1,3,5,7,9,11,13,15,17,19,21,23,25,27,29,31,33,35,37,39,41,43,45,47]],
    'ncpus': 2,
    'nthreads': 24,
    'ncores': 12
}

prog_name = {
    'none'        : './concurrent-tl2',
    'tl2'         : './concurrent-tl2',
    'tl2+cb'      : './concurrent-cb',
    'tl2+reuse'   : './concurrent-rt',
    'gv7'         : './concurrent-gv7',
    'noopt'       : './concurrent-noopt',
    'tl2-lesser'  : './concurrent-tl2-lesser',
    'gv7-lesser'  : './concurrent-gv7-lesser',
    'tictoc'      : './concurrent-tictoc'
}

opts_contention = {
    'low': ' 3 array --ntrans=10000000 --opspertrans=10',
    'ultra low': ' 10 array --ntrans=10000000',
    'high': ' 9 array --ntrans=10000000 --opspertrans=8 --readonlypercent=0.9'
}

def get_cpu_list(policy, nthreads):
    cl = []
    if policy == 'single-cpu':
        if nthreads > sys_info['ncores']:
            print 'Info: Hyperthreads are being used'
        if nthreads > sys_info['nthreads']:
            print 'Info: Scheduling more than one thread per hardware hyperthread'
            nthreads = sys_info['nthreads']
        cl = sys_info['cpu_lists'][1][0:nthreads]

    elif policy == 'multi-cpu':
        if nthreads > sys_info['ncores'] * sys_info['ncpus']:
            print 'Info: Hyperthreads are being used'
        if nthreads > sys_info['nthreads'] * sys_info['ncpus']:
            print 'Info: Scheduling more than one thread per hardware hyperthread'
            nthreads = sys_info['nthreads'] * sys_info['ncpus']
        threads_per_cpu = nthreads / sys_info['ncpus']
        leftover = nthreads % sys_info['ncpus']
        for i in range(sys_info['ncpus']):
            cl = cl + sys_info['cpu_lists'][i][0:threads_per_cpu]
        for t in range(leftover):
            cl.append(sys_info['cpu_lists'][t][threads_per_cpu])

    else:
        print 'Unknown policy {}'.format(policy)
        return cl

    print 'Info: Running {} threads on CPUs {}'.format(nthreads, cl)
    return list(map(lambda x: '{}'.format(x), cl))

def taskset_cmd(nthreads):
    policy = 'single-cpu'
    if nthreads > sys_info['nthreads']:
        policy = 'multi-cpu'
    return 'taskset -c {}'.format(','.join(get_cpu_list(policy, nthreads)))

def run_single(opacity_type, contention, nthreads):
    global DRY_RUN
    cmd = prog_name[opacity_type]
    cmd += opts_contention[contention]

    if opacity_type == 'none':
        cmd = cmd.replace('array', 'array-nonopaque')

    cmd += ' --nthreads={}'.format(nthreads)
    cmd = taskset_cmd(nthreads) + ' ' + cmd

    print cmd

    if DRY_RUN:
        return (0.0, 0.0, 0.0)

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

    for o in opacity_types:
        for c in contention:
            for t in threads:
                for n in range(ntrails):
                    result = run_single(o,c,t)
                    if not DRY_RUN:
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
        title='Throughput comparision of reordering schemes',
        filename='throughput-{}-contention.png'.format(contention.replace(' ','')))

def graph_aborts(all_results, contention):
    graph_all_bars(all_results, contention, calc_aborts,
        y_title='Abort rate (%)',
        title='Abort rates of reordering schemes (lowers are better)',
        filename='aborts-{}-contention.png'.format(contention.replace(' ','')))

def graph_hcos(all_results, contention):
    graph_all_bars(all_results, contention, calc_hcos,
        y_title='# HCOs',
        title='Number of Hard Checks (HCOs)',
        filename='hcos-{}-contention.png'.format(contention.replace(' ','')))

def main():
    global DRY_RUN

    parser = optparse.OptionParser()
    parser.add_option('-l', action="store", dest="load_file", default='')
    parser.add_option('-d', action="store_true", dest="dry_run", default=False)

    options, args = parser.parse_args()

    DRY_RUN = options.dry_run

    if options.load_file != '':
        with open(options.load_file, 'r') as input_file:
            results = json.load(input_file)
    else:
        results = run_benchmark()
        print 'ALL DONE'
        if DRY_RUN:
            exit()
        with open('gv7_results.json', 'w') as outfile:
            json.dump(results, outfile)

    # plot graph(s)
    for c in contention:
        graph_throughput(results, c)
        graph_aborts(results, c)

if __name__ == '__main__':
    main()
