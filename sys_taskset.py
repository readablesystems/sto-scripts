#!/usr/bin/env python
sys_info = {
    'cpu_lists': [[0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,38,40,42,44,46],
        [1,3,5,7,9,11,13,15,17,19,21,23,25,27,29,31,33,35,37,39,41,43,45,47]],
    'ncpus': 2,
    'nthreads': 24,
    'ncores': 12
}

VERBOSE = False

def get_cpu_list(policy, nthreads):
    cl = []
    if policy == 'single-cpu':
        if nthreads > sys_info['ncores'] and VERBOSE:
            print 'Info: Hyperthreads are being used'
        if nthreads > sys_info['nthreads'] and VERBOSE:
            print 'Info: Scheduling more than one thread per hardware hyperthread'
            nthreads = sys_info['nthreads']
        cl = sys_info['cpu_lists'][1][0:nthreads]

    elif policy == 'multi-cpu':
        if nthreads > sys_info['ncores'] * sys_info['ncpus'] and VERBOSE:
            print 'Info: Hyperthreads are being used'
        if nthreads > sys_info['nthreads'] * sys_info['ncpus'] and VERBOSE:
            print 'Info: Scheduling more than one thread per hardware hyperthread'
            nthreads = sys_info['nthreads'] * sys_info['ncpus']
        threads_per_cpu = nthreads / sys_info['ncpus']
        leftover = nthreads % sys_info['ncpus']
        for i in range(sys_info['ncpus']):
            cl = cl + sys_info['cpu_lists'][i][0:threads_per_cpu]
        for t in range(leftover):
            cl.append(sys_info['cpu_lists'][t][threads_per_cpu])

    else:
        print 'Unknown policy {}'.format(policy)
        return cl

    if VERBOSE:
        print 'Info: Running {} threads on CPUs {}'.format(nthreads, cl)
    return list(map(lambda x: '{}'.format(x), cl))

def taskset_cmd(nthreads, in_policy=''):
    if in_policy != '':
        policy = in_policy
    else:
        policy = 'single-cpu'
        if nthreads > sys_info['nthreads']:
            policy = 'multi-cpu'
    return 'taskset -c {}'.format(','.join(get_cpu_list(policy, nthreads)))

def get_policy(nthreads):
    if nthreads > 12:
        p = 'multi-cpu'
    else:
        p = 'single-cpu'

    if nthreads == 13:
        return (12, p)
    else:
        return (nthreads, p)
