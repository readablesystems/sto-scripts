#!/usr/bin/env python

import sys_taskset as tsk
import subprocess,json,os

sys_names = {
    'STO': 'dbtest-sto',
    'STO/gTID': 'dbtest-gtid',
    'TicToc': 'dbtest-tictoc',
    'STO/O': 'dbtest-tl2',
    'STO/O-': 'dbtest-tl2-lesser',
    'STO/O gv7': 'dbtest-gv7',
    'STO/O gv7-': 'dbtest-gv7-lesser'
}

tpcc_opts = ' --runtime 30 -dmbta --bench tpcc'

threads = [4,8,12,16]
systems = ['STO', 'STO/O', 'STO/O gv7', 'TicToc']
gtid_systems = ['STO', 'STO/gTID']
ntrails = 3

cats = threads

DRY_RUN = False
TEST_DIR = './test_dir'

def run_single(sys_name, nthr, ntrail, scale_wh):
    global DRY_RUN
    cmd = tsk.taskset_cmd(nthr)
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

def run_tpcc():
    return ({}, {})
    results = {}
    results_scale_wh = {}
    for thr in threads:
        for sys in systems:
            for trl in range(ntrails):
                res = run_single(sys, thr, trl, scale_wh=False)
                results[exp_key(sys, thr, trl)] = res
    for thr in threads:
        for sys in systems:
            for trl in range(ntrails):
                res = run_single(sys, thr, trl, scale_wh=True)
                results_scale_wh[exp_key(sys, thr, trl)] = res
    return (results, results_scale_wh)

def run_tpcc_gtid():
    results_scale_wh = {}

    for thr in threads:
        for sys in gtid_systems:
            for trl in range(ntrails):
                res = run_single(sys,thr,trl,scale_wh=True)
                results_scale_wh[exp_key(sys,thr,trl)] = res

    return results_scale_wh

if __name__ == '__main__':
    old_r = []
    if os.path.exists('tpcc_4wh_results.json'):
        with open('tpcc_4wh_results.json', 'r') as f:
            old_r.append(json.load(f))
    else:
        old_r.append({})

    if os.path.exists('tpcc_swh_results.json'):
        with open('tpcc_swh_results.json', 'r') as f:
            old_r.append(json.load(f))
    else:
        old_r.append({})

    r = run_tpcc()
    r_gtid = run_tpcc_gtid()
    r[1].update(r_gtid)

    if DRY_RUN:
        exit()

    r[0].update(old_r[0])
    r[1].update(old_r[1])
    with open('tpcc_4wh_results.json', 'w') as rfile:
        json.dump(r[0], rfile, indent=4, sort_keys=True)
    with open('tpcc_swh_results.json', 'w') as rfile:
        json.dump(r[1], rfile, indent=4, sort_keys=True)
