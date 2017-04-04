#!/usr/bin/env python

import subprocess
from sto import profile_parser as parser

sys_info = {
    "cpu_lists": [[0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,38,40,42,44,46],
        [1,3,5,7,9,11,13,15,17,19,21,23,25,27,29,31,33,35,37,39,41,43,45,47]],
    "ncpus": 2,
    "nthreads": 24,
    "ncores": 12
}

prog_name = {
    "tl2": "./concurrent",
    "gv7": "./concurrent-gv7"
}

opts_low_contention = " 3 array --ntrans=10000000 --opspertrans=10"
opts_high_contention = " 9 array --ntrans=10000000 --opspertrans=8 --readonlypercent=0.9"

def get_cpu_list(policy, nthreads):
    cl = []
    if policy == "single-cpu":
        if nthreads > sys_info["ncores"]:
            print "Info: Hyperthreads are being used"
        if nthreads > sys_info["nthreads"]:
            print "Info: Scheduling more than one thread per hardware hyperthread"
            nthreads = sys_info["nthreads"]
        cl = sys_info["cpu_lists"][1][0:nthreads]

    elif policy == "multi-cpu":
        if nthreads > sys_info["ncores"] * sys_info["ncpus"]:
            print "Info: Hyperthreads are being used"
        if nthreads > sys_info["nthreads"] * sys_info["ncpus"]:
            print "Info: Scheduling more than one thread per hardware hyperthread"
            nthreads = sys_info["nthreads"] * sys_info["ncpus"]
        threads_per_cpu = nthreads / sys_info["ncpus"]
        leftover = nthreads % sys_info["ncpus"]
        for i in range(sys_info["ncpus"]):
            cl = cl + sys_info["cpu_lists"][i][0:threads_per_cpu]
        for t in range(leftover):
            cl.append(sys_info["cpu_lists"][t][threads_per_cpu])

    else:
        print "Unknown policy {}".format(policy)
        return cl

    print "Info: Running {} threads on CPUs {}".format(nthreads, cl)
    return cl

def taskset_cmd(nthreads):
    return 'taskset -c {}'.format(','.join(get_cpu_list("single_cpu", nthreads)))

def run_single(opacity_type, contention, nthreads):
    cmd = prog_name[opacity_type]
    if contention == "low":
        cmd += opts_low_contention

    cmd += " --nthreads={}".format(nthreads)
    cmd = taskset_cmd(nthreads) + ' ' + cmd
    print cmd

    out = subprocess.check_output(cmd.split(' '), stderr=subprocess.STDOUT)

    time = parser.extract('time', out)
    aborts = parser.extract('aborts', out)
    hcos = parser.extract('hcos', out)

    return (time, aborts, hcos)
