# Common methods

import sys
from enum import Enum


class GraphType(Enum):
    LINE = 1
    BAR = 2
    HBAR = 3


def fatal_error(msg):
    print('Fatal error: ' + msg, file=sys.stderr)
    sys.exit(1)


def get_result_file(bench_name):
    return 'results/json/{}_results.json'.format(bench_name)


# Benchmark configurations


class TPCCConfig:
    NAME = 'tpcc'
    #DIM1 = [8, 16, 24, 32, 64, 96, 128]
    DIM1 = [8, 16, 24, 32, 48]
    #DIM2 = ['default', 'swiss', 'adaptive', '2pl', 'tictoc']
    DIM2 = ['default,coarse', 'tictoc,coarse', 'default,fine']
    DIM3 = ['high']


class WikiConfig:
    NAME = 'wiki'
    DIM1 = [8, 16, 24, 32, 48]
    DIM2 = ['default,coarse', 'tictoc,coarse', 'default,fine']
    DIM3 = ['one']


class MVSTOConfig:
    NAME = 'tpcc_mvsto'
    DIM1 = [1, 2, 4, 12, 24, 32, 40, 48, 64]
    DIM2 = ['o','onr','o.c','o.s','o.c.s','m','m.c','m.s','m.c.s','c', 'e', 'mocc']
    DIM3 = ['1', '4', '0'] # number of warehouses


class MVSTOTPCCFactorsConfig:
    NAME = 'tpcc_factors'
    DIM1 = [12]
    DIM2 = ['m', 'm.h', 'm.a', 'm.h,a', 'c', 'm.h.a.c.s']
    DIM3 = ['1']


class MVSTOYCSBConfig:
    NAME = 'ycsb_mvsto'
    DIM1 = [1, 2, 4, 12, 24, 32, 40, 48, 64]
    DIM2 = ['o','o.c','o.s','o.c.s','m','m.c','m.s','m.c.s']
    DIM3 = ['a', 'b'] # workload type


class MVSTOWikiConfig:
    NAME = 'wiki_mvsto'
    DIM1 = [1, 2, 4, 12, 24, 32, 40, 48, 64]
    DIM2 = ['o','o.c','o.s','o.c.s','m','m.c','m.s','m.c.s']
    DIM3 = ['1'] # only one configuration


class MVSTORubisConfig:
    NAME = 'rubis_mvsto'
    DIM1 = [1, 2, 4, 12, 24, 32, 40, 48, 64]
    DIM2 = ['o','o.c','o.s','o.c.s','m','m.c','m.s','m.c.s']
    DIM3 = ['1'] # only one configuration


# Graph config


color_mapping = {
    'o': 1,
    'onr': 9,
    'o.c': 3,
    'o.s': 5,
    'o.c.s': 7,
    'm': 0,
    'm.c': 2,
    'm.s': 4,
    'm.s.i': 4,
    'm.c.s': 6,
    'm.c.s.i': 6,
    'c': 8,
    'e': 10,
    'mocc': 12,
    'tictoc': 14,
    'op': 11,
    'op.c': 13,
    'op.s': 15,
    'op.c.s': 17,
    'mf': 11,
    'mf.c': 13,
    'mf.c.s': 15,
    # GC graph
    'm.r0': 0,
    'm.r1k': 2,
    'm.r100k': 4
}

marker_mapping = {
    'o':       'o',
    'op':      'o',
    'onr':     'o',
    'o.c':     '<',
    'op.c':    '<',
    'o.s':     's',
    'op.s':    's',
    'o.c.s':   '*',
    'op.c.s':  '*',
    'm':       'h',
    'm.c':     'H',
    'm.s':     'D',
    'm.s.i':   'D',
    'm.c.s':   'x',
    'm.c.s.i': 'x',
    'c':       '^',
    'e':       '>',
    'mocc':    'd',
    'tictoc':  'h',
    'mf':      'h',
    'mf.c':    'H',
    'mf.c.s':  'x',
    'm.r0':    '^',
    'm.r1k':   '^',
    'm.r100k': '^'
}


class TPCCGraphConfig:
    INFO = {
        'x_label': '# threads',
        'y_label': 'Throughput (Mtxns/sec)',
        'series_names': ('Coarse', 'TicToc', 'Fine'),
        'fill_colors': ('black', 'white', 'white', 'white', 'white'),
        'hatches': ('', '++', '///', 'xx', ''),
        'l_markers': ('o', '^', 's', '*'),
        'l_colors': ('red', 'blue', 'green', 'orange'),
        'legends_on': True
    }
    NAME = TPCCConfig.NAME
    TYPE = GraphType.BAR
    DIM1 = TPCCConfig.DIM1
    DIM2 = TPCCConfig.DIM2
    DIM3 = TPCCConfig.DIM3
    D3TITLES = ['High contention TPC-C (8 warehouses fixed)']
    D3FNAMES = ['tpcc_bench']


class WikiGraphConfig:
    INFO = {
        'x_label': '# threads',
        'y_label': 'Throughput (Mtxns/sec)',
        'series_names': ('Coarse', 'TicToc', 'Fine'),
        'fill_colors': ('black', 'white', 'white', 'white', 'white'),
        'hatches': ('', '++', '///', 'xx', ''),
        'l_markers': ('o', '^', 's', '*'),
        'l_colors': ('red', 'blue', 'green', 'orange'),
        'legends_on': True
    }
    NAME = WikiConfig.NAME
    TYPE = GraphType.LINE
    DIM1 = WikiConfig.DIM1
    DIM2 = WikiConfig.DIM2
    DIM3 = WikiConfig.DIM3
    D3TITLES = ['Wikipedia benchmark']
    D3FNAMES = ['wiki_bench']


class MVSTOGraphConfig:
    INFO = {
        'x_label': '# threads',
        'y_label': 'Throughput (Mtxns/sec)',
        'series_names': ('OCC', 'OCCNOREG', 'OCC + CU', 'OCC + SV', 'OCC + CU + SV',
                         'MVCC', 'MVCC + CU', 'MVCC + SV', 'MVCC + CU + SV',
                         'Cicada', 'ERMIA', 'MOCC'),
        'legends_on': True
    }
    NAME = MVSTOConfig.NAME
    TYPE = GraphType.LINE
    DIM1 = MVSTOConfig.DIM1
    DIM2 = MVSTOConfig.DIM2
    DIM3 = MVSTOConfig.DIM3
    LEGENDS = [True, False, False]
    D3TITLES = ['TPC-C one warehouse', 'TPC-C four warehouses', 'TPC-C partitioned']
    D3FNAMES = ['tpcc_w1', 'tpcc_w4', 'tpcc_part']


# Scalability graphs:
# Self comparisons, CU + VG with baselines only.
# TPC-C 1 warehouse, Wikipedia, Rubis. 6 subfigures.
class TOCCGraphConfig:
    INFO = {
        'x_label': '# threads',
        'y_label': 'Throughput (Mtxns/sec)',
        'series_names': ('OCC', 'OCC+CU', 'OCC+VG', 'OCC+CU+VG'),
        'legends_on': True
    }
    NAME = MVSTOConfig.NAME
    TYPE = GraphType.LINE
    DIM1 = MVSTOConfig.DIM1
    DIM2 = ['o','o.c','o.s','o.c.s']
    DIM3 = ['1', '4', '0']
    LEGENDS = [True, False, False]
    D3YMAXES = [1.6, 4.1, 4.5]
    D3TITLES = ['', '', '']
    D3FNAMES = ['tpcc_w1_occ', 'tpcc_w4_occ', 'tpcc_part_occ']


class TMVGraphConfig:
    INFO = {
        'x_label': '# threads',
        'y_label': 'Throughput (Mtxns/sec)',
        'series_names': ('MVCC', 'MVCC+CU', 'MVCC+VG', 'MVCC+CU+VG'),
        'legends_on': True
    }
    NAME = MVSTOConfig.NAME
    TYPE = GraphType.LINE
    DIM1 = MVSTOConfig.DIM1
    DIM2 = ['m','m.c','m.s','m.c.s']
    DIM3 = ['1', '4', '0']
    LEGENDS = [True, False, False]
    D3YMAXES = [1.6, 4.1, 4.5]
    D3TITLES = ['', '', '']
    D3FNAMES = ['tpcc_w1_mvcc', 'tpcc_w4_mvcc', 'tpcc_part_mvcc']


class WikiOCCGraphConfig:
    INFO = {
        'x_label': '# threads',
        'y_label': 'Throughput (Mtxns/sec)',
        'y_max': 0.6,
        'series_names': ('OCC','OCC+CU','OCC+VG','OCC+CU+VG'),
        'legends_on': True
    }
    NAME = MVSTOWikiConfig.NAME
    TYPE = GraphType.LINE
    DIM1 = MVSTOWikiConfig.DIM1
    DIM2 = ['o','o.c','o.s','o.c.s']
    DIM3 = ['1']
    LEGENDS = [True]
    D3TITLES = ['']
    D3FNAMES = ['wiki_occ']


class WikiMVGraphConfig:
    INFO = {
        'x_label': '# threads',
        'y_label': 'Throughput (Mtxns/sec)',
        'y_max': 0.6,
        'series_names': ('MVCC','MVCC+CU','MVCC+VG','MVCC+CU+VG'),
        'legends_on': True
    }
    NAME = MVSTOWikiConfig.NAME
    TYPE = GraphType.LINE
    DIM1 = MVSTOWikiConfig.DIM1
    DIM2 = ['m','m.c','m.s','m.c.s']
    DIM3 = ['1']
    LEGENDS = [True]
    D3TITLES = ['']
    D3FNAMES = ['wiki_mvcc']


class RubisOCCGraphConfig:
    INFO = {
        'x_label': '# threads',
        'y_label': 'Throughput (Mtxns/sec)',
        'y_max': 2.2,
        'series_names': ('OCC','OCC+CU','OCC+VG','OCC+CU+VG'),
        'legends_on': True
    }
    NAME = MVSTORubisConfig.NAME
    TYPE = GraphType.LINE
    DIM1 = MVSTORubisConfig.DIM1
    DIM2 = ['o','o.c','o.s','o.c.s']
    DIM3 = ['1']
    LEGENDS = [True]
    D3TITLES = ['']
    D3FNAMES = ['rubis_occ']


class RubisMVGraphConfig:
    INFO = {
        'x_label': '# threads',
        'y_label': 'Throughput (Mtxns/sec)',
        'y_max': 2.2,
        'series_names': ('MVCC','MVCC+CU','MVCC+VG','MVCC+CU+VG'),
        'legends_on': True
    }
    NAME = MVSTORubisConfig.NAME
    TYPE = GraphType.LINE
    DIM1 = MVSTORubisConfig.DIM1
    DIM2 = ['m','m.c','m.s','m.c.s']
    DIM3 = ['1']
    LEGENDS = [True]
    D3TITLES = ['']
    D3FNAMES = ['rubis_mvcc']


# Overhead bar graph
# Showing TPC-C partitioned workload
# 2 subfigures, OCC vs. +CUVG, MVCC vs. +CUVG
class TW1OCCZoomedGraphConfig:
    INFO = {
        'x_label': '# threads',
        'y_label': 'Throughput (Mtxns/sec)',
        'series_names': ('OCC','OCC+CU','OCC+VG','OCC+CU+VG'),
        'legends_on': True
    }
    NAME = MVSTOConfig.NAME
    TYPE = GraphType.LINE
    DIM1 = [1,2,4]
    DIM2 = ['o','o.c','o.s','o.c.s']
    DIM3 = ['1']
    LEGENDS = [True]
    D3TITLES = ['']
    D3FNAMES = ['tpcc_w1_occ_zoomed']


class TW1MVZoomedGraphConfig:
    INFO = {
        'x_label': '# threads',
        'y_label': 'Throughput (Mtxns/sec)',
        'series_names': ('MVCC','MVCC+CU','MVCC+VG','MVCC+CU+VG'),
        'legends_on': True
    }
    NAME = MVSTOConfig.NAME
    TYPE = GraphType.LINE
    DIM1 = [1,2,4]
    DIM2 = ['m','m.c','m.s','m.c.s']
    DIM3 = ['1']
    LEGENDS = [True]
    D3TITLES = ['']
    D3FNAMES = ['tpcc_w1_mvcc_zoomed']


class TWPOCCGraphConfig:
    INFO = {
        'x_label': '# threads',
        'y_label': 'Throughput (Mtxns/sec)',
        'series_names': ('OCC','OCC+CU','OCC+VG','OCC+CU+VG'),
        'legends_on': True
    }
    NAME = MVSTOConfig.NAME
    TYPE = GraphType.LINE
    DIM1 = MVSTOConfig.DIM1
    DIM2 = ['o','o.c','o.s','o.c.s']
    DIM3 = ['0']
    LEGENDS = [True]
    D3TITLES = ['']
    D3FNAMES = ['tpcc_part_occ']


class TWPMVGraphConfig:
    INFO = {
        'x_label': '# threads',
        'y_label': 'Throughput (Mtxns/sec)',
        'series_names': ('MVCC','MVCC+CU','MVCC+VG','MVCC+CU+VG'),
        'legends_on': True
    }
    NAME = MVSTOConfig.NAME
    TYPE = GraphType.LINE
    DIM1 = MVSTOConfig.DIM1
    DIM2 = ['m','m.c','m.s','m.c.s']
    DIM3 = ['0']
    LEGENDS = [True]
    D3TITLES = ['']
    D3FNAMES = ['tpcc_part_mvcc']


# Alternative: line graph?
class TWPLineGraphConfig:
    INFO = {
        'x_label': '# threads',
        'y_label': 'Throughput (Mtxns/sec)',
        'series_names': ('OCC', 'OCC + CU + VG', 'MVCC', 'MVCC + CU + VG'),
        'legends_on': True
    }
    NAME = MVSTOConfig.NAME
    TYPE = GraphType.LINE
    DIM1 = MVSTOConfig.DIM1
    DIM2 = ['o','o.c.s','m','m.c.s']
    DIM3 = ['0']
    LEGENDS = [True]
    D3TITLES = ['']
    D3FNAMES = ['tpcc_part_line']


# TPC-C factor analysis graph
class TPCCFactorsGraphConfig:
    INFO = {
        'x_label': 'Factors',
        'y_label': 'Throughput (Mtxns/sec)',
        'series_names': ('Unoptimized', '+HT', '+AL', '+HT+AL', 'Cicada', '+HT+AL+CU+FV'),
        'legends_in': True
    }
    NAME = MVSTOTPCCFactorsConfig.NAME
    TYPE = GraphType.HBAR
    DIM1 = [12]
    DIM2 = ['m', 'm.h', 'm.a', 'm.h.a', 'c', 'm.h.a.c.s']
    DIM3 = ['1']
    LEGENDS = [True]
    D3TITLES = ['']
    D3FNAMES = ['tpcc_factors']


# Graphs with opacity results
class TPCCOpacityGraphConfig:
    INFO = {
        'x_label': '# threads',
        'y_label': 'Throughput (Mtxns/sec)',
        'series_names': ('OCC','OCC+O','OCC+CU+VG','OCC+CU+VG+O','OCC+VG','OCC+VG+O'),
        'legends_on': True
    }
    NAME = MVSTOConfig.NAME
    TYPE = GraphType.LINE
    DIM1 = MVSTOConfig.DIM1
    DIM2 = ['o','op','o.c.s','op.c.s','o.s','op.s']
    DIM3 = ['1', '4', '0']
    LEGENDS = [False, True, False]
    D3TITLES = ['', '', '']
    D3FNAMES = ['tpcc_op_w1', 'tpcc_op_w4', 'tpcc_op_part']


# Comparison bar graphs with other systems
class TOCCCompGraphConfig:
    INFO = {
        'x_label': '# threads',
        'y_label': 'Throughput (Mtxns/sec)',
        'series_names': ('OCC','OCC+CU+VG','MOCC','TicToc'),
        'legends_on': True
    }
    NAME = MVSTOConfig.NAME
    TYPE = GraphType.LINE
    DIM1 = MVSTOConfig.DIM1
    DIM2 = ['o','o.c.s','mocc','tictoc']
    DIM3 = ['1', '4', '0']
    LEGENDS = [True, False, False]
    D3YMAXES = [None, None, None]
    D3TITLES = ['', '', '']
    D3FNAMES = ['tpcc_occ_comp_w1', 'tpcc_occ_comp_w4', 'tpcc_occ_comp_part']


class TMVCompGraphConfig:
    INFO = {
        'x_label': '# threads',
        'y_label': 'Throughput (Mtxns/sec)',
        'series_names': ('MVCC','MVCC+CU+VG','Cicada','ERMIA'),
        'legends_on': True
    }
    NAME = MVSTOConfig.NAME
    TYPE = GraphType.LINE
    DIM1 = MVSTOConfig.DIM1
    DIM2 = ['m','m.c.s','c','e']
    DIM3 = ['1', '4', '0']
    LEGENDS = [True, False, False]
    D3YMAXES = [None, None, None]
    D3TITLES = ['', '', '']
    D3FNAMES = ['tpcc_mvcc_comp_w1', 'tpcc_mvcc_comp_w4', 'tpcc_mvcc_comp_part']


# Investigating alternative RTID/abort on read-time delta version flattening
# MVCC only
class TMVFlattenGraphConfig:
    INFO = {
        'x_label': '# threads',
        'y_label': 'Throughput (Mtxns/sec)',
        'series_names': ('MVCC','MVCC-','MVCC+CU','MVCC+CU-','MVCC+CU+VG','MVCC+CU+VG-'),
        'legends_on': True
    }
    NAME = MVSTOConfig.NAME
    TYPE = GraphType.LINE
    DIM1 = MVSTOConfig.DIM1
    DIM2 = ['m','mf','m.c','mf.c','m.c.s','mf.c.s']
    DIM3 = ['1', '4', '0']
    LEGENDS = [True, True, True]
    D3TITLES = ['', '', '']
    D3FNAMES = ['tpcc_mvcc_flatten_w1', 'tpcc_mvcc_flatten_w4', 'tpcc_mvcc_flatten_part']


class TMVGCIntervalGraphConfig:
    INFO = {
        'x_label': '# threads',
        'y_label': 'Throughput (Mtxns/sec)',
        'series_names': ('No GC','GC 1ms','GC 100ms'),
        'legends_on': True
    }
    NAME = MVSTOConfig.NAME
    TYPE = GraphType.LINE
    DIM1 = MVSTOConfig.DIM1
    DIM2 = ['m.r0','m.r1k','m.r100k']
    DIM3 = ['1', '0']
    LEGENDS = [True, True]
    D3TITLES = ['', '']
    D3FNAMES = ['tpcc_gc_w1', 'tpcc_gc_part']


# OLD GRPAHS
class MVSTOTPCCOCCGraphConfig:
    INFO = {
        'x_label': '# threads',
        'y_label': 'Throughput (Mtxns/sec)',
        'series_names': ('OCC', 'OCC + CU', 'OCC + SV', 'OCC + CU + SV'),
        'legends_on': True
    }
    NAME = MVSTOConfig.NAME
    DIM1 = MVSTOConfig.DIM1
    DIM2 = ['o', 'o.c', 'o.s', 'o.c.s']
    DIM3 = MVSTOConfig.DIM3
    LEGENDS = [True, False, False]
    D3TITLES = ['TPC-C one warehouse (OCC)', 'TPC-C four warehouses (OCC)', 'TPC-C partitioned (OCC)']
    D3FNAMES = ['tpcc_occ_w1', 'tpcc_occ_w4', 'tpcc_occ_part']


class MVSTOTPCCMVCCGraphConfig:
    INFO = {
        'x_label': '# threads',
        'y_label': 'Throughput (Mtxns/sec)',
        'series_names': ('MVCC', 'MVCC + CU', 'MVCC + SV', 'MVCC + CU + SV',
                         'Cicada', 'ERMIA'),
        'legends_on': True
    }
    NAME = MVSTOConfig.NAME
    DIM1 = MVSTOConfig.DIM1
    DIM2 = ['m', 'm.c', 'm.s', 'm.c.s', 'c', 'e']
    DIM3 = MVSTOConfig.DIM3
    LEGENDS = [True, False, False]
    D3TITLES = ['TPC-C one warehouse (MVCC)', 'TPC-C four warehouses (MVCC)', 'TPC-C partitioned (MVCC)']
    D3FNAMES = ['tpcc_mvcc_w1', 'tpcc_mvcc_w4', 'tpcc_mvcc_part']


class MVSTOYCSBGraphConfig:
    INFO = {
        'x_label': '# threads',
        'y_label': 'Throughput (Mtxns/sec)',
        'series_names': ('OCC', 'OCC + CU', 'OCC + SV', 'OCC + CU + SV',
                         'MVCC', 'MVCC + CU', 'MVCC + SV', 'MVCC + CU + SV'),
        'legends_on': True
    }
    NAME = MVSTOYCSBConfig.NAME
    TYPE = GraphType.LINE
    DIM1 = MVSTOYCSBConfig.DIM1
    DIM2 = MVSTOYCSBConfig.DIM2
    DIM3 = MVSTOYCSBConfig.DIM3
    LEGENDS = [True, True]
    D3TITLES = ['YCSB-A', 'YCSB-B']
    D3FNAMES = ['ycsb_a', 'ycsb_b']


class MVSTOYCSBOCCGraphConfig:
    INFO = {
        'x_label': '# threads',
        'y_label': 'Throughput (Mtxns/sec)',
        'series_names': ('OCC', 'OCC + CU', 'OCC + SV', 'OCC + CU + SV'),
        'legends_on': True
    }
    NAME = MVSTOYCSBConfig.NAME
    DIM1 = MVSTOYCSBConfig.DIM1
    DIM2 = ['o', 'o.c', 'o.s', 'o.c.s']
    DIM3 = MVSTOYCSBConfig.DIM3
    LEGENDS = [True]
    D3TITLES = ['YCSB (OCC)']
    D3FNAMES = ['ycsb_occ']


class MVSTOYCSBMVCCGraphConfig:
    INFO = {
        'x_label': '# threads',
        'y_label': 'Throughput (Mtxns/sec)',
        'series_names': ('MVCC', 'MVCC + CU', 'MVCC + SV', 'MVCC + CU + SV'),
        'legends_on': True
    }
    NAME = MVSTOYCSBConfig.NAME
    DIM1 = MVSTOYCSBConfig.DIM1
    DIM2 = ['m', 'm.c', 'm.s', 'm.c.s']
    DIM3 = MVSTOYCSBConfig.DIM3
    LEGENDS = [True]
    D3TITLES = ['YCSB (MVCC)']
    D3FNAMES = ['ycsb_mvcc']


class MVSTOWikiGraphConfig:
    INFO = {
        'x_label': '# threads',
        'y_label': 'Throughput (Mtxns/sec)',
        'series_names': ('OCC', 'OCC + CU', 'OCC + SV', 'OCC + CU + SV',
                         'MVCC', 'MVCC + CU', 'MVCC + SV', 'MVCC + CU + SV'),
        'legends_on': True
    }
    NAME = MVSTOWikiConfig.NAME
    DIM1 = MVSTOWikiConfig.DIM1
    DIM2 = MVSTOWikiConfig.DIM2
    DIM3 = MVSTOWikiConfig.DIM3
    LEGENDS = [True]
    D3TITLES = ['Wikipedia workload']
    D3FNAMES = ['wiki']


class MVSTORubisGraphConfig:
    INFO = {
        'x_label': '# threads',
        'y_label': 'Throughput (Mtxns/sec)',
        'series_names': ('OCC', 'OCC + CU', 'OCC + SV', 'OCC + CU + SV',
                         'MVCC', 'MVCC + CU', 'MVCC + SV', 'MVCC + CU + SV'),
        'legends_on': True
    }
    NAME = MVSTORubisConfig.NAME
    DIM1 = MVSTORubisConfig.DIM1
    DIM2 = MVSTORubisConfig.DIM2
    DIM3 = MVSTORubisConfig.DIM3
    LEGENDS = [True]
    D3TITLES = ['Rubis-like workload']
    D3FNAMES = ['rubis']
