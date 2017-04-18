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

threads = [4,8,12]

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
    'tictoc-o'    : 'concurrent-tictoc,',
    'gtid'        : 'concurrent-gtid'
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
    commits = parser.extract('commits', out)
    aborts = parser.extract('aborts', out)
    hcos = parser.extract('hcos', out)

    xput = commits/time

    return (time, aborts, hcos)

def exp_key(opacity, contention, nthreads, ntrail):
    return '{}/{}/{}/{}'.format(opacity, contention, nthreads, ntrail)

# Compare results at 4, 8, 12 threads
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
        with open('ubench_results.json', 'w') as outfile:
            json.dump(results, outfile, indent=4, sort_keys=True)
    else:
        results = results_f

if __name__ == '__main__':
    main()
