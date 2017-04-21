#!/usr/bin/env python

import subprocess,json,os,optparse
import gv7_ubench as ub
import sys_taskset as tsk
from sto import profile_parser as parser

DRY_RUN = None

RESULT_DIR = 'results/json/'
RESULT_FILE = RESULT_DIR + 'ubench_opacity_overhead_results.json'

ntrails = 5
threads = [4,12,13,24]
systems = ['none', 'tl2', 'gv7', 'tictoc', 'tictoc-o']
wls = ['l-small', 'h-small', 'l-large', 'h-large']

def exp_opt(wl):
    opt = ' 11 array --ntrans=10000000 --opspertrans={} --skew={} --timelimit=5'
    wll = wl.split('-')
    skew = None
    size = None

    if wll[0] == 'h':
        skew = 1.2
    else:
        skew = 0.1

    if wll[1] == 'small':
        size = 10
    else:
        size = 50

    return opt.format(size,skew)

def run_single(sys, wl, nthreads):
    global DRY_RUN

    nthreads, p = tsk.get_policy(nthreads)

    cmd = '{}/{}'.format(ub.TEST_DIR, ub.prog_name[sys])
    cmd += exp_opt(wl)
    if sys == 'none' or sys == 'tictoc':
        cmd = cmd.replace('array', 'array-nonopaque')

    cmd += ' --nthreads={}'.format(nthreads)

    cmd = tsk.taskset_cmd(nthreads, p) + ' ' + cmd

    print cmd

    if DRY_RUN:
        return (0,0,0)
    
    out = subprocess.check_output(cmd.split(' '), stderr=subprocess.STDOUT)

    time = parser.extract('time', out)
    commits = parser.extract('commits', out)
    aborts = parser.extract('aborts', out)
    hcos = parser.extract('hcos', out)

    xput = commits/time

    return (xput,aborts,hcos)

def key(sys_name, wkld, nthr, tril):
    return ub.exp_key(sys_name, wkld, nthr, tril)

def run_benchmark(results):
    global DRY_RUN

    for sys in systems:
        for wl in wls:
            for tr in threads:
                for n in range(ntrails):
                    k = key(sys,wl,tr,n)
                    if k in results:
                        continue
                    res = run_single(sys,wl,tr)
                    if DRY_RUN:
                        continue
                    results[k] = res

if __name__ == '__main__':
    psr = optparse.OptionParser()
    psr.add_option('-f', action="store_true", dest="force_update", default=False)
    psr.add_option('-d', action="store_true", dest="dry_run", default=False)
    opts, args = psr.parse_args()
    DRY_RUN = opts.dry_run

    results = {}
    if os.path.exists(RESULT_FILE) and not opts.force_update:
        with open(RESULT_FILE, 'r') as rf:
            results = json.load(rf)

    run_benchmark(results)
    print 'ALL DONE'

    if DRY_RUN:
        exit()

    with open(RESULT_FILE, 'w') as ofile:
        json.dump(results, ofile, indent=4, sort_keys=True)
