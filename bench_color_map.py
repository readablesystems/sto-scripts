#!/usr/bin/env python

tableau20 = None

color_map = None

ubench_sys_names = [
    'tl2', 'tl2-lesser',
    'tl2+cb', 'tl2+cb-lesser',
    'tl2+reuse', 'tl2+reuse-lesser',
    'gv7', 'gv7-lesser',
    'tictoc', 'tictoc-o',
    'gtid', 'noopt',
    'none'
]

tpcc_sys_map = {
    'STO': 'none',
    'STO/gTID': 'gtid',
    'STO/O': 'tl2',
    'STO/O-': 'tl2-lesser',
    'STO/O gv7': 'gv7',
    'STO/O gv7-': 'gv7-lesser',
    'TicToc': 'tictoc'
}

def settings():
    global tableau20
    global color_map

    tableau20 = [(31,119,180), (174,199,232), (255,127,14), (255,187,120),
                 (44,160,44), (152,223,138), (214,39,40), (255,152,150),
                 (148,103,189), (197,176,213), (140,86,75), (196,156,148),
                 (227,119,194), (247,182,210), (127,127,127), (199,199,199),
                 (188,189,34), (219,219,141), (23,190,207), (158,218,229)]

    for i in range(len(tableau20)):
        r,g,b = tableau20[i]
        tableau20[i] = (r/255., g/255., b/255.)

    color_map = {}

    for i in range(len(ubench_sys_names)):
        if ubench_sys_names[i] != 'none':
            c = tableau20[i]
        else:
            c = (0.,0.,0.)
        color_map[ubench_sys_names[i]] = c

    for tn in tpcc_sys_map:
        color_map[tn] = color_map[tpcc_sys_map[tn]]

settings()
