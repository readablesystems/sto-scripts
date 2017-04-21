#!/usr/bin/env python

import sys_taskset as tsk
import subprocess,json,os,optparse

sys_names = {
    'STO': 'dbtest-sto',
    'STO/gTID': 'dbtest-gtid',
    'TicToc': 'dbtest-tictoc',
    'TicToc/O': 'dbtest-tictoc-o',
    'STO/O': 'dbtest-tl2',
    'STO/O-': 'dbtest-tl2-lesser',
    'STO/O gv7': 'dbtest-gv7',
    'STO/O gv7-': 'dbtest-gv7-lesser'
}

tpcc_opts = ' --runtime 30 -dmbta --bench tpcc'

threads = [4,12,13,24]
systems = ['STO', 'STO/O', 'STO/O-', 'STO/O gv7', 'TicToc', 'TicToc/O']
gtid_systems = ['STO', 'STO/gTID']
ntrails = 3

cats = threads

DRY_RUN = None
TEST_DIR = './test_dir'

RESULT_DIR = 'results/json/'
RESULT_FILES = [RESULT_DIR + 'tpcc_4wh_results.json', RESULT_DIR + 'tpcc_swh_results.json']

def run_single(sys_name, nthr, ntrail, scale_wh):
    global DRY_RUN

    nthr, p = tsk.get_policy(nthr)

    cmd = tsk.taskset_cmd(nthr, p)
    cmd += ' {}/'.format(TEST_DIR) + sys_names[sys_name]
    cmd += tpcc_opts
    cmd += ' --num-threads {}'.format(nthr)
    if scale_wh:
        cmd += ' --scale-factor {}'.format(nthr)
    else:
        cmd += ' --scale-factor 4'

    print cmd
    if DRY_RUN:
        return 0

    output = subprocess.check_output(cmd.split(' '))

    outl = output.split(' ')
    xput = float(outl[0])
    abrt = float(outl[4])

    return (xput, abrt*100.0/(xput+abrt))

def exp_key(sys_name, nthr, ntrail):
    return '{}/{}/{}'.format(sys_name, nthr, ntrail)

def run_tpcc(results):
    results_4wh = results[0]
    results_scale_wh = results[1]
    for thr in threads:
        for sys in systems:
            for trl in range(ntrails):
                k = exp_key(sys, thr, trl)
                if k in results_4wh:
                    continue
                res = run_single(sys, thr, trl, scale_wh=False)
                results_4wh[k] = res
    for thr in threads:
        for sys in systems:
            for trl in range(ntrails):
                k = exp_key(sys, thr, trl)
                if k in results_scale_wh:
                    continue
                res = run_single(sys, thr, trl, scale_wh=True)
                results_scale_wh[k] = res

def run_tpcc_gtid(results_scale_wh):
    for thr in threads:
        for sys in gtid_systems:
            for trl in range(ntrails):
                k = exp_key(sys,thr,trl)
                if k in results_scale_wh:
                    continue
                res = run_single(sys,thr,trl,scale_wh=True)
                results_scale_wh[k] = res

if __name__ == '__main__':
    results = []

    psr = optparse.OptionParser()
    psr.add_option('-f', action="store_true", dest="force_update", default=False)
    psr.add_option('-d', action="store_true", dest="dry_run", default=False)

    opts, args = psr.parse_args()

    DRY_RUN = opts.dry_run

    for resfile in RESULT_FILES:
        if os.path.exists(resfile) and not opts.force_update:
            with open(resfile, 'r') as f:
                results.append(json.load(f))
        else:
            results.append({})

    run_tpcc(results)
    #run_tpcc_gtid(results[1])

    if DRY_RUN:
        exit()

    for i in range(len(results)):
        with open(RESULT_FILES[i], 'w') as rfile:
            json.dump(results[i], rfile, indent=4, sort_keys=True)
