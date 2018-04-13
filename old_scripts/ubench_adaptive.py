#!/usr/bin/env python

import subprocess,json,os,time,optparse
from sto import profile_parser as parser

TYPE = 'ubench'
NAME = 'adaptive'

DRY_RUN = None
RESULT_DIR = 'results/json/'
RESULT_FILE = RESULT_DIR + '{}_{}_results.json'.format(TYPE, NAME)

ntrails = 5

threads = [4,8,12,16,20,24]
systems = ['array-adaptive', 'array-nonopaque', 'swissarray']
levels = ['med', 'high', 'low']

skew_vals = {'low':0.0, 'med':0.8, 'high':1.0}

def cmd_opts(sys, skew, thrs):
    opt = './concurrent 4 {0} --opspertrans=20 --ntrans=5000000 --nthreads={1} --skew={2}'
    return opt.format(sys, thrs, skew)

def run_single(sys, skew, thrs):
    global DRY_RUN

    cmd = cmd_opts(sys, skew, thrs)
    print cmd

    if DRY_RUN:
        return (0,0,0)

    out = subprocess.check_output(cmd.split(' '), stderr=subprocess.STDOUT)

    time = parser.extract('time', out)
    commits = parser.extract('commits', out)
    aborts = parser.extract('aborts', out)
    cabrts = parser.extract('commit_time_aborts', out)

    xput = commits/time

    return (xput,aborts,cabrts)

def key(system_name, workload, nthreads, trail):
    return '{}/{}/{}/{}'.format(system_name,workload,nthreads,trail)

def run_all(results):
    global DRY_RUN

    for sys in systems:
        for cont in levels:
            for tr in threads:
                for n in range(ntrails):
                    k = key(sys,cont,tr,n)
                    if k in results:
                        continue
                    res = run_single(sys, skew_vals[cont], tr)
                    if DRY_RUN:
                        continue
                    results[k] = res
                    print "--gap--"
                    time.sleep(1)
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

    r = run_all(old_results)
    print 'ALL DONE'

    if DRY_RUN:
        exit()

    with open(RESULT_FILE, 'w') as ofile:
        json.dump(r,ofile,indent=4,sort_keys=True)
