#!/usr/bin/env python

import sys_taskset as tsk
import subprocess,json

sys_names = {
    'STO': 'dbtest-sto',
    'TicToc': 'dbtest-tictoc',
    'STO/O': 'dbtest-tl2',
    'STO/O-': 'dbtest-tl2-lesser',
    'STO/O gv7': 'dbtest-gv7',
    'STO/O gv7-': 'dbtest-gv7-lesser'
}

tpcc_opts = ' --runtime 30 --scale-factor=4 -dmbta --bench tpcc'

threads = [4,8,12,16]
systems = ['STO', 'STO/O', 'STO/O-', 'STO/O gv7', 'STO/O gv7-', 'TicToc']
ntrails = 3

cats = threads

DRY_RUN = False
TEST_DIR = './test_dir'

def run_single(sys_name, nthr, ntrail):
    global DRY_RUN
    cmd = tsk.taskset_cmd(nthr)
    cmd += ' {}/'.format(TEST_DIR) + sys_names[sys_name]
    cmd += tpcc_opts
    cmd += ' --num-threads {}'.format(nthr)

    if DRY_RUN:
        print cmd
        return 0

    output = subprocess.check_output(cmd.split(' '))

    outl = output.split(' ')
    xput = float(outl[0])

    return xput

def exp_key(sys_name, nthr, ntrail):
    return '{}/{}/{}'.format(sys_name, nthr, ntrail)

def run_tpcc():
    results = {}
    for thr in threads:
        for sys in systems:
            for trl in range(ntrails):
                xput = run_single(sys, thr, trl)
                results[exp_key(sys, thr, trl)] = xput
    return results

if __name__ == '__main__':
    r = run_tpcc()
    if DRY_RUN:
        exit()
    with open('tpcc_results.json', 'w') as rfile:
        json.dump(r, rfile, indent=4, sort_keys=True)
