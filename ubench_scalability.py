#!/usr/bin/env python

import subprocess,json,optparse
import gv7_ubench as ub
import sys_taskset as tsk
from sto import profile_parser as parser

DRY_RUN = None

threads = [4,8,12,16,20,24,28,32]

wls = ['u-tiny', 'u-small', 'u-large', 'c-tiny', 'c-small', 'c-large']

def scalability_opt(wl):
    opt = ' 11 array --ntrans=12000000 --opspertrans={} --readonlypercent=0 --writepercent=1 --skew={}'
    wll = wl.split('-')
    skew = None
    opspertrans = None
    if wll[0] == 'c':
        skew = 1.2
    else:
        skew = 0.1
    if wll[1] == 'tiny':
        opspertrans = 1
    elif wll[1] == 'small':
        opspertrans = 10
    else:
        opspertrans = 50
    return opt.format(opspertrans, skew)

def run_single_scalability(wl, nthreads):
    global DRY_RUN
    cmd = '{}/{}'.format(ub.TEST_DIR, ub.prog_name['tl2'])
    cmd += scalability_opt(wl)
    cmd += ' --nthreads={}'.format(nthreads)

    cmd = tsk.taskset_cmd(nthreads) + ' ' + cmd

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

def run_scalability():
    global DRY_RUN
    results = {}

    for wl in wls:
        for tr in threads:
            for n in range(ub.ntrails):
                k = ub.exp_key('tl2',wl,tr,n)
                res = run_single_scalability(wl,tr)
                if DRY_RUN:
                    continue
                results[k] = res
    return results

if __name__ == '__main__':
    psr = optparse.OptionParser()
    psr.add_option('-d', action="store_true", dest="dry_run", default=False)
    opts, args = psr.parse_args()
    DRY_RUN = opts.dry_run

    r = run_scalability()
    print 'ALL DONE'

    if DRY_RUN:
        exit()

    with open('ubench_scale_results.json', 'w') as ofile:
        json.dump(r,ofile,indent=4,sort_keys=True)
