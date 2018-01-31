#!/usr/bin/env python

import subprocess,json,os,time,optparse
from sto import profile_parser as parser

TYPE = 'tpcc'
NAME = 'fine_grain'

DRY_RUN = None
RESULT_DIR = 'results/json/'
RESULT_FILE = RESULT_DIR + '{}_{}_results.json'.format(TYPE, NAME)

ntrails = 5

threads = [8,16,24,32,64,96,128]
systems = ['default', 'swiss', 'adaptive', '2pl', 'tictoc']
levels = ['low', 'high']

def cmd_opts(sys, nwhs, thrs):
    opt = './tpcc_bench_fine -t{0} -w{1} --time=10.0 --dbid={2}'
    return opt.format(thrs, nwhs, sys)

def run_single(sys, nwhs, thrs):
    global DRY_RUN

    cmd = cmd_opts(sys, nwhs, thrs)
    print cmd

    if DRY_RUN:
        return (0,0,0)

    out = ""
    while True:
        retries = 0

        try:
            out = subprocess.check_output(cmd.split(' '), stderr=subprocess.STDOUT)
        except:
            retries += 1
            print "Subprocess error, retrying. ({})".format(retries)
            continue
        break

    xput = parser.extract('tpcc_xput', out)
    aborts = parser.extract('aborts', out)
    cabrts = parser.extract('commit_time_aborts', out)

    return (xput,aborts,cabrts)

def key(system_name, workload, nthreads, trail):
    return '/'.join((system_name,workload,str(nthreads),str(trail)))

def run_all(results):
    global DRY_RUN

    for sys in systems:
        for cont in levels:
            for tr in threads:
                for n in range(ntrails):
                    k = key(sys,cont,tr,n)
                    if k in results:
                        continue
                    nwhs = 8
                    if cont == 'low':
                        nwhs = tr
                    res = run_single(sys,nwhs,tr)
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
