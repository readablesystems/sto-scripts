#!/usr/bin/env python

import os

prog_name = {
    'none'        : 'concurrent-tl2',
    'tl2'         : 'concurrent-tl2',
    'tl2+cb'      : 'concurrent-cb',
    'tl2+reuse'   : 'concurrent-rt',
    'tl2+reuse-lesser' : 'concurrent-rt-lesser',
    'gv7'         : 'concurrent-gv7',
    'noopt'       : 'concurrent-tl2-noopt',
    'tl2-lesser'  : 'concurrent-tl2-lesser',
    'gv7-lesser'  : 'concurrent-gv7-lesser',
    'tictoc'      : 'concurrent-tictoc',
    'tictoc-o'    : 'concurrent-tictoc',
    'gtid'        : 'concurrent-gtid',
    'abort'       : 'concurrent-abort'
}

common_make_args = 'PROFILE_COUNTERS=1'

main_extra_make_args = {
    'tl2':              'ABORT_ON_LOCKED=0',
    'tl2+cb':           'ABORT_ON_LOCKED=0 CACHE_BOUND=1',
    'tl2+reuse':        'ABORT_ON_LOCKED=0 REUSE_TID=1',
    'tl2+reuse-lesser': 'ABORT_ON_LOCKED=0 REUSE_TID=1 LESSER_OPACITY=1',
    'gv7':              'ABORT_ON_LOCKED=0 GV7_OPACITY=1',
    'noopt':            'ABORT_ON_LOCKED=0 NO_READONLY_OPT=1',
    'tl2-lesser':       'ABORT_ON_LOCKED=0 LESSER_OPACITY=1',
    'gv7-lesser':       'ABORT_ON_LOCKED=0 GV7_OPACITY=1 LESSER_OPACITY=1',
    'gtid':             'ABORT_ON_LOCKED=0 GLOBAL_TID=1',
    'abort':            'ABORT_ON_LOCKED=1'
}

tictoc_extra_make_args = {
    'tictoc': 'ABORT_ON_LOCKED=0'
}

def build_bag(bag):
    for sys in bag:
        cmd = 'make clean && '
        cmd += 'make {} {} concurrent -j && '.format(common_make_args, bag[sys])
        cmd += 'cp concurrent test_dir/{}'.format(prog_name[sys])
        print cmd
        while True:
            ret = os.system(cmd)
            if ret == 0:
                break

os.system('git checkout gv7_opacity')

build_bag(main_extra_make_args)

os.system('git checkout tictoc')

build_bag(tictoc_extra_make_args)

os.system('make clean && git checkout gv7_opacity')
