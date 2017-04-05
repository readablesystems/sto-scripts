#!/usr/bin/env python

import subprocess,json
import numpy as np
from matplotlib import pyplot as plt
from sto import profile_parser as parser

DRY_RUN = False

# Experiment configuration
ntrails = 5
opacity_types = ['tl2', 'gv7']
contention = ['low', 'high']
threads = [4,8,16]

color_map = {
    'tl2': (153,216,201),
    'gv7': (227,26,28)
}
    #(152,78,163),
    #(251,180,174)

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
    'tl2': './concurrent',
    'gv7': './concurrent-gv7'
}

opts_contention = {
    'low': ' 3 array --ntrans=10000000 --opspertrans=10',
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
    return 'taskset -c {}'.format(','.join(get_cpu_list('single-cpu', nthreads)))

def run_single(opacity_type, contention, nthreads):
    cmd = prog_name[opacity_type]
    cmd += opts_contention[contention]

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
    all_results = {}

    for o in opacity_types:
        for c in contention:
            for t in threads:
                for n in range(ntrails):
                    result = run_single(o,c,t)
                    if not DRY_RUN:
                        all_results[exp_key(o,c,t,n)] = result

    return all_results

def graph_throughput(all_results, contention):
    c = contention
    y = {}
    y_min = {}
    y_max = {}
    for o in opacity_types:
        for t in threads:
            throughput_series = []
            for n in range(ntrails):
                time, aborts, hcos = all_results[exp_key(o,c,t,n)]
                t = 10.0 / time # throughput in Mtxns/sec
                throughput_series.append(t)
            throughput_min = np.amin(throughput_series)
            throughput_max = np.amax(throughput_series)
            throughput_med = np.median(throughput_series)

            if not o in y:
                y[o] = []
            if not o in y_min:
                y_min[o] = []
            if not o in y_max:
                y_max[o] = []
            y[o].append(throughput_med)
            y_min[o].append(throughput_min)
            y_max[o].append(throughput_max)

    N = len(threads)
    ind = np.arange(N)
    width = 0.2

    fig, ax = plt.subplots(figsize=(10, 6))
    t_rects = [ax.bar(ind+width*opacity_types.index(o), y[o], width, color=color_map[o], yerr=[y_min[o], y_max[o]]) for o in opacity_types]

    ax.set_title('Throughput comparision of GV7 and TL2 opacity\n{} contention'.format(contention))
    ax.set_ylabel('Throughput (Mtxns/sec)')
    ax.set_xticks(ind+width*len(threads)/2)
    ax.set_xticklabels(['{} threads'.format(t) for t in threads])
    ax.legend([r[0] for r in t_rects], opacity_types)

    plt.show()

#def graph_aborts(all_results):

#def graph_hco_passthrough(all_results):

if __name__ == '__main__':
    results = run_benchmark()
    print 'ALL DONE'
    if DRY_RUN:
        exit()

    with open('gv7_results.json', 'w') as outfile:
        json.dump(results, outfile)
