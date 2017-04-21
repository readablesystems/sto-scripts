#!/usr/bin/env python

import subprocess,json,os,optparse
import gv7_ubench as ub
import sys_taskset as tsk
from sto import profile_parser as parser

DRY_RUN = None
RESULT_DIR = 'results/json/'
RESULT_FILE = RESULT_DIR + 'ubench_gtid_results.json'

ntrails = 5
threads = [4,12,13,24]
systems = ['none', 'gtid']
wls = ['u-tiny', 'u-small', 'c-tiny', 'c-small']

def gtid_opt(wl):
    opt = ' 11 array-nonopaque --ntrans=12000000 --opspertrans={} --readonlypercent=0.0 --writepercent=1.0 --skew={} --timelimit=5'
    wll = wl.split('-')
    skew = None
    opspertrans = None
    if wll[0] == 'c':
        skew = 1.0
    else:
        skew = 0.1
    if wll[1] == 'tiny':
        opspertrans = 1
    elif wll[1] == 'small':
        opspertrans = 10
    else:
        opspertrans = 50
    return opt.format(opspertrans, skew)

def run_single_gtid(sys, wl, nthreads):
    global DRY_RUN

    nthreads, p = tsk.get_policy(nthreads)

    cmd = '{}/{}'.format(ub.TEST_DIR, ub.prog_name[sys])
    cmd += gtid_opt(wl)
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

def key(system_name, workload, nthreads, trail):
    return ub.exp_key(system_name, workload, nthreads, trail)

def run_gtid(results):
    global DRY_RUN

    for sys in systems:
        for wl in wls:
            for tr in threads:
                for n in range(ntrails):
                    k = key(sys,wl,tr,n)
                    if k in results:
                        continue # experiment done before
                    res = run_single_gtid(sys,wl,tr)
                    if DRY_RUN:
                        continue
                    results[k] = res
    return results

if __name__ == '__main__':
    psr = optparse.OptionParser()
    psr.add_option('-f', action="store_true", dest="force_update", default=False)
    psr.add_option('-d', action="store_true", dest="dry_run", default=False)
    opts, args = psr.parse_args()
    DRY_RUN = opts.dry_run

    old_results = None
    if os.path.exists(RESULT_FILE) and not opts.force_update:
        with open(RESULT_FILE, 'r') as rf:
            old_results = json.load(rf)
    else:
        old_results = {}

    r = run_gtid(old_results)
    print 'ALL DONE'

    if DRY_RUN:
        exit()

    with open(RESULT_FILE, 'w') as ofile:
        json.dump(r,ofile,indent=4,sort_keys=True)
