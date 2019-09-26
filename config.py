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


class MVSTOTPCCStackedFactorsConfig:
    NAME = 'tpcc_stacked_factors'
    DIM1 = [1, 2, 4, 12, 24, 32, 40, 48, 64]
    DIM2 = ['mn', 'mn.a', 'mn.a.r', 'mn.a.r.e', 'mn.a.r.e.h']
    DIM3 = ['1', '4', '0']


class MVSTOTPCCIndexContentionConfig:
    NAME = 'tpcc_index_contention'
    DIM1 = [1, 2, 4, 12, 24, 32, 40, 48, 64]
    DIM2 = ['on', 'o']
    DIM3 = ['1', '4', '0']


class MVSTOYCSBConfig:
    NAME = 'ycsb_mvsto'
    DIM1 = [1, 2, 4, 12, 24, 32, 40, 48, 64]
    DIM2 = ['o','o.c','o.s','o.c.s','m','m.c','m.s','m.c.s']
    DIM3 = ['a', 'b'] # workload type


class YCSBTicTocCompConfig:
    NAME = 'ycsb_tictoc_comp'
    DIM1 = [1, 2, 4, 12, 24, 32, 40, 48, 64]
    DIM2 = ['o','t']
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

barcolor_mapping = {
    'default': 'green',
    'c': 8,
    'm.c.s': 6,
    'm': 0
}

color_mapping = {
    'o': 0,
    'onr': 9,
    'o.c': 2,
    'o.s': 4,
    'o.c.s': 6,
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
    'tictoc.s': 16,
    'tictoc.c': 17,
    'tictoc.c.s': 15,
    'op': 11,
    'op.c': 13,
    'op.s': 15,
    'op.c.s': 17,
    'mf': 11,
    'mf.c': 13,
    'mf.c.s': 15,
    # stacked factors graph
    'mn': 2,
    'mn.a': 4,
    'mn.a.r': 6,
    'mn.a.r.e': 8,
    'mn.a.r.e.h': 0,
    'on.a': 4,
    'on.a.r': 6,
    'on.a.r.e': 8,
    'on.a.r.e.h': 0,
    # index contention graph
    'on': 2,
    # GC graph
    'm.r0': 0,
    'm.r1k': 2,
    'm.r100k': 4,
    'secondary': (0.5,0.5,0.5)
}

marker_mapping = {
    'o':       None,
    'op':      None,
    'onr':     None,
    'o.c':     None,
    'op.c':    None,
    'o.s':     None,
    'op.s':    None,
    'o.c.s':   None,
    'op.c.s':  None,
    'm':       'x',
    'm.c':     'x',
    'm.s':     'x',
    'm.s.i':   'x',
    'm.c.s':   'x',
    'm.c.s.i': 'x',
    'c':       '^',
    'e':       '>',
    'mocc':    'd',
    'tictoc':  'h',
    'tictoc.s':  'h',
    'tictoc.c':  'h',
    'tictoc.c.s':  'h',
    'mf':      'h',
    'mf.c':    'H',
    'mf.c.s':  'x',
    # stacked factors line graph
    'mn': 'p',
    'mn.a': 'p',
    'mn.a.r': 'p',
    'mn.a.r.e': 'p',
    'mn.a.r.e.h': 'x',
    'on.a': 'p',
    'on.a.r': 'p',
    'on.a.r.e': 'p',
    'on.a.r.e.h': 'x',
    # index contention graph
    'on': None,
    # gc graph
    'm.r0':    '^',
    'm.r1k':   '^',
    'm.r100k': '^'
}

linestyle_mapping = {
    'o.c': 'dashed',
    'op.c': 'dashed',
    'm.c': 'dashed',
    'o.s': 'dotted',
    'op.s': 'dotted',
    'm.s': 'dotted',
    'o.c.s': 'dashdot',
    'op.c.s': 'dashdot',
    'm.c.s': 'dashdot',
    'secondary': (0, (1, 3)),
    'default': 'solid',
    'e': (0, (2, 3)),
    'c': (0, (2, 3)),
    'mocc': (0, (2, 3)),
    'tictoc': (0, (2, 3)),
    'tictoc.s': (0, (2, 3)),
    'tictoc.c': (0, (2, 3)),
    'tictoc.c.s': (0, (2, 3)),
}

linewidth_mapping = {
    'secondary': 1.25,
    'default': 2,
    'mocc': 3,
    'c': 3,
    'e': 3,
    'tictoc': 3,
    'tictoc.s': 3,
    'tictoc.c': 3,
    'tictoc.c.s': 3,
}

errorbar_mapping = {
    'default': True,
    'secondary': False
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
                         'MVCC', 'MSTO + CU', 'MSTO + SV', 'MSTO + CU + SV',
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
        'series_names': ('OSTO', 'OSTO+CU', 'OSTO+TS', 'OSTO+CU+TS'),
        'markevery': {
            'default': (0.5, 1.0),
            'o.c': (0.3, 1.0),
            'secondary': None
        },
        'legends_on': True,
        'legend_order': (3, 2, 1, 0)
    }
    NAME = MVSTOConfig.NAME
    TYPE = GraphType.LINE
    DIM1 = MVSTOConfig.DIM1
    DIM2 = ['o','o.c','o.s','o.c.s','m-secondary','m.c-secondary','m.s-secondary','m.c.s-secondary']
    DIM3 = ['1', '4', '0']
    LEGENDS = [False, True, False]
    D3YMAXES = [1.6, 4.1, 5.0]
    D3TITLES = ['', '', '']
    D3FNAMES = ['tpcc_w1_occ', 'tpcc_w4_occ', 'tpcc_part_occ']


class TMVGraphConfig:
    INFO = {
        'x_label': '# threads',
        'y_label': 'Throughput (Mtxns/sec)',
        'series_names': ('MSTO', 'MSTO+CU', 'MSTO+TS', 'MSTO+CU+TS'),
        'legends_on': True,
        'legend_order': (3, 2, 1, 0)
    }
    NAME = MVSTOConfig.NAME
    TYPE = GraphType.LINE
    DIM1 = MVSTOConfig.DIM1
    DIM2 = ['m','m.c','m.s','m.c.s','o-secondary','o.c-secondary','o.s-secondary','o.c.s-secondary']
    DIM3 = ['1', '4', '0']
    LEGENDS = [False, True, False]
    D3YMAXES = [1.6, 4.1, 5.0]
    D3TITLES = ['', '', '']
    D3FNAMES = ['tpcc_w1_mvcc', 'tpcc_w4_mvcc', 'tpcc_part_mvcc']


# YCSB scalability graphs
# Self comparisons
class YOCCGraphConfig:
    INFO = {
        'x_label': '# threads',
        'y_label': 'Throughput (Mtxns/sec)',
        'series_names': ('OSTO', 'OSTO+CU', 'OSTO+TS', 'OSTO+CU+TS'),
        'markevery': {
            'default': (0.5, 1.0),
            'o.c': (0.3, 1.0),
            'secondary': None
        },
        'legends_on': True,
        'legend_order': (3, 2, 1, 0)
    }
    NAME = MVSTOYCSBConfig.NAME
    TYPE = GraphType.LINE
    DIM1 = MVSTOYCSBConfig.DIM1
    DIM2 = ['o','o.c','o.s','o.c.s','m-secondary','m.c-secondary','m.s-secondary','m.c.s-secondary']
    DIM3 = ['a', 'b']
    LEGENDS = [True, False]
    D3YMAXES = [None, None]
    D3TITLES = ['', '']
    D3FNAMES = ['ycsb_a_occ', 'ycsb_b_occ']
    FIG_SIZE = (7, 5)


# YCSB (A & B) TicToc vs OCC comparison graph
class YTOCompGraphConfig:
    INFO = {
        'x_label': '# threads',
        'y_label': 'Throughput (Mtxns/sec)',
        'series_names': ('OCC', 'TicToc'),
        'legends_on': True,
    }
    NAME = YCSBTicTocCompConfig.NAME
    TYPE = GraphType.LINE
    DIM1 = YCSBTicTocCompConfig.DIM1
    DIM2 = ['o', 'tictoc']
    DIM3 = ['a', 'b']
    LEGENDS = [True, True]
    D3YMAXES = [None, None]
    D3TITLES = ['', '']
    D3FNAMES = ['ycsb_a_tictoc_comp', 'ycsb_b_tictoc_comp']


class YMVGraphConfig:
    INFO = {
        'x_label': '# threads',
        'y_label': 'Throughput (Mtxns/sec)',
        'series_names': ('MSTO', 'MSTO+CU', 'MSTO+TS', 'MSTO+CU+TS'),
        'legends_on': True,
        'legend_order': (3, 2, 1, 0)
    }
    NAME = MVSTOYCSBConfig.NAME
    TYPE = GraphType.LINE
    DIM1 = MVSTOYCSBConfig.DIM1
    DIM2 = ['m','m.c','m.s','m.c.s','o-secondary','o.c-secondary','o.s-secondary','o.c.s-secondary']
    DIM3 = ['a', 'b']
    LEGENDS = [True, False]
    D3YMAXES = [None, None]
    D3TITLES = ['', '']
    D3FNAMES = ['ycsb_a_mvcc', 'ycsb_b_mvcc']
    FIG_SIZE = (7, 5)


# Wikipedia + RUBiS graphs
class WikiOCCGraphConfig:
    INFO = {
        'x_label': '# threads',
        'y_label': 'Throughput (Mtxns/sec)',
        'y_max': 0.6,
        'series_names': ('OSTO','OSTO+CU','OSTO+TS','OSTO+CU+TS'),
        'legends_on': True,
        'legend_order': (3,1,2,0)
    }
    NAME = MVSTOWikiConfig.NAME
    TYPE = GraphType.LINE
    DIM1 = MVSTOWikiConfig.DIM1
    DIM2 = ['o','o.c','o.s','o.c.s','m-secondary','m.c-secondary','m.s-secondary','m.c.s-secondary']
    DIM3 = ['1']
    LEGENDS = [True]
    D3YMAXES = [None]
    D3TITLES = ['']
    D3FNAMES = ['wiki_occ']


class WikiMVGraphConfig:
    INFO = {
        'x_label': '# threads',
        'y_label': 'Throughput (Mtxns/sec)',
        'y_max': 0.6,
        'series_names': ('MSTO','MSTO+CU','MSTO+TS','MSTO+CU+TS'),
        'legends_on': True,
        'legend_order': (3,1,2,0)
    }
    NAME = MVSTOWikiConfig.NAME
    TYPE = GraphType.LINE
    DIM1 = MVSTOWikiConfig.DIM1
    DIM2 = ['m','m.c','m.s','m.c.s','o-secondary','o.c-secondary','o.s-secondary','o.c.s-secondary']
    DIM3 = ['1']
    LEGENDS = [True]
    D3YMAXES = [None]
    D3TITLES = ['']
    D3FNAMES = ['wiki_mvcc']


class RubisOCCGraphConfig:
    INFO = {
        'x_label': '# threads',
        'y_label': 'Throughput (Mtxns/sec)',
        'y_max': 2.2,
        'series_names': ('OSTO','OSTO+CU','OSTO+TS','OSTO+CU+TS'),
        'legends_on': True
    }
    NAME = MVSTORubisConfig.NAME
    TYPE = GraphType.LINE
    DIM1 = MVSTORubisConfig.DIM1
    DIM2 = ['o','o.c','o.s','o.c.s','m-secondary','m.c-secondary','m.s-secondary','m.c.s-secondary']
    DIM3 = ['1']
    LEGENDS = [True]
    D3YMAXES = [None]
    D3TITLES = ['']
    D3FNAMES = ['rubis_occ']


class RubisMVGraphConfig:
    INFO = {
        'x_label': '# threads',
        'y_label': 'Throughput (Mtxns/sec)',
        'y_max': 2.2,
        'series_names': ('MSTO','MSTO+CU','MSTO+TS','MSTO+CU+TS'),
        'legends_on': True
    }
    NAME = MVSTORubisConfig.NAME
    TYPE = GraphType.LINE
    DIM1 = MVSTORubisConfig.DIM1
    DIM2 = ['m','m.c','m.s','m.c.s','o-secondary','o.c-secondary','o.s-secondary','o.c.s-secondary']
    DIM3 = ['1']
    LEGENDS = [True]
    D3YMAXES = [None]
    D3TITLES = ['']
    D3FNAMES = ['rubis_mvcc']


# Overhead bar graph
# Showing TPC-C partitioned workload
# 2 subfigures, OCC vs. +CUVG, MVCC vs. +CUVG
class TW1OCCZoomedGraphConfig:
    INFO = {
        'x_label': '# threads',
        'y_label': 'Throughput (Mtxns/sec)',
        'series_names': ('OSTO','OSTO+CU','OSTO+TS','OSTO+CU+TS'),
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
        'series_names': ('MSTO','MSTO+CU','MSTO+TS','MSTO+CU+TS'),
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
        'series_names': ('OSTO','OSTO+CU','OSTO+TS','OSTO+CU+TS'),
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
        'series_names': ('MSTO','MSTO+CU','MSTO+TS','MSTO+CU+TS'),
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
        'series_names': ('OSTO', 'OSTO + CU + VG', 'MSTO', 'MSTO + CU + VG'),
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
        'series_names': ('-Mem-Hash-Backoff', '-Mem', '-Backoff', '-Hash', 'Baseline (MSTO)', 'Cicada', 'MSTO+CU+TS'),
        'legends_in': True
    }
    NAME = MVSTOTPCCFactorsConfig.NAME
    TYPE = GraphType.HBAR
    DIM1 = [24]
    DIM2 = ['m.a.r.h', 'm.a', 'm.r', 'm.h', 'm', 'c', 'm.c.s']
    DIM3 = ['1']
    LEGENDS = [True]
    D3YMAXES = [None]
    D3TITLES = ['']
    D3FNAMES = ['tpcc_factors']


# TPC-C stacked factor analysis, MVCC only
class TPCCStackedFactorsGraphConfig:
    INFO = {
        'x_label': '# threads',
        'y_label': 'Throughput (Mtxns/sec)',
        'series_names': ('NoOpt', '+Allocator', '+Backoff', '+NoExcept', '+HashIdx'),
        'legends_on': True
    }
    NAME = MVSTOTPCCStackedFactorsConfig.NAME
    TYPE = GraphType.LINE
    DIM1 = [1, 2, 4, 12, 24, 32, 40, 48, 64]
    DIM2 = ['mn', 'mn.a', 'mn.a.r', 'mn.a.r.e', 'mn.a.r.e.h']
    DIM3 = ['1', '4', '0']
    LEGENDS = [False, False, True]
    D3YMAXES = [None, None, None]
    D3TITLES = ['', '', '']
    D3FNAMES = ['tpcc_stacked_factors_w1', 'tpcc_stacked_factors_w4', 'tpcc_stacked_factors_part']


# TPC-C stacked factor analysis, OCC only
class TPCCOCCStackedFactorsGraphConfig:
    INFO = {
        'x_label': '# threads',
        'y_label': 'Throughput (Mtxns/sec)',
        'series_names': ('NoOpt', '+Allocator', '+Backoff', '+NoExcept', '+HashIdx'),
        'legends_on': True
    }
    NAME = MVSTOTPCCStackedFactorsConfig.NAME
    TYPE = GraphType.LINE
    DIM1 = [1, 2, 4, 12, 24, 32, 40, 48, 64]
    DIM2 = ['on', 'on.a', 'on.a.r', 'on.a.r.e', 'on.a.r.e.h']
    DIM3 = ['1', '4', '0']
    LEGENDS = [False, False, True]
    D3YMAXES = [None, None, None]
    D3TITLES = ['', '', '']
    D3FNAMES = ['tpcc_stacked_factors_occ_w1', 'tpcc_stacked_factors_occ_w4', 'tpcc_stacked_factors_occ_part']


# Index contention graph, showing throughput of delivery transactions only
# Note the scale factor is different (thousands instead of millions)
class TPCCIndexContentionGraphConfig:
    INFO = {
        'x_label': '# threads',
        'y_label': 'Throughput (Ktxns/sec)',
        'scale_factor': 1000.0,
        'series_names': ('NoOpt', '+CAIndex'),
        'legends_on': True
    }
    NAME = MVSTOTPCCIndexContentionConfig.NAME
    TYPE = GraphType.LINE
    DIM1 = [1, 2, 4, 12, 24, 32, 40, 48, 64]
    DIM2 = ['on', 'o']
    DIM3 = ['1', '4', '0']
    LEGENDS = [True, True, True]
    D3YMAXES = [None, None, None]
    D3TITLES = ['', '', '']
    D3FNAMES = ['tpcc_index_contention_w1', 'tpcc_index_contention_w4', 'tpcc_index_contention_part']


# Graphs with opacity results
class TPCCOpacityGraphConfig:
    INFO = {
        'x_label': '# threads',
        'y_label': 'Throughput (Mtxns/sec)',
        'series_names': ('OSTO','OSTO+O','OSTO+CU+TS','OSTO+CU+TS+O','OSTO+TS','OSTO+TS+O'),
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


# OCC vs TicToc comparison graph
class TOTCCCompGraphConfig:
    INFO = {
        'x_label': '# threads',
        'y_label': 'Throughput (Mtxns/sec)',
        'series_names': ('OSTO','OSTO+CU+TS','TicToc','TicToc+TS','TicToc+CU','TicToc+CU+TS'),
        'legends_on': True,
        'legend_order': (1,0,5,4,3,2),
        'markevery': {
            'tictoc': (0.25, 0.01)
        }
    }
    NAME = MVSTOConfig.NAME
    TYPE = GraphType.LINE
    DIM1 = MVSTOConfig.DIM1
    DIM2 = ['o','o.c.s','tictoc','tictoc.s','tictoc.c','tictoc.c.s']
    DIM3 = ['1', '4', '0']
    LEGENDS = [False, True, False]
    D3YMAXES = [None, None, None]
    D3TITLES = ['', '', '']
    D3FNAMES = ['tpcc_ttcc_comp_w1', 'tpcc_ttcc_comp_w4', 'tpcc_ttcc_comp_part']


# Comparison bar graphs with other systems
class TOCCCompGraphConfig:
    INFO = {
        'x_label': '# threads',
        'y_label': 'Throughput (Mtxns/sec)',
        'series_names': ('OSTO','OSTO+CU+TS','MOCC','TicToc'),
        'legends_on': True,
        'legend_order': (1,0,3,2),
        'markevery': {
            'tictoc': (0.25, 0.01)
        }
    }
    NAME = MVSTOConfig.NAME
    TYPE = GraphType.LINE
    DIM1 = MVSTOConfig.DIM1
    DIM2 = ['o','o.c.s','mocc','tictoc']
    DIM3 = ['1', '4', '0']
    LEGENDS = [False, True, False]
    D3YMAXES = [None, None, None]
    D3TITLES = ['', '', '']
    D3FNAMES = ['tpcc_occ_comp_w1', 'tpcc_occ_comp_w4', 'tpcc_occ_comp_part']


class TMVCompGraphConfig:
    INFO = {
        'x_label': '# threads',
        'y_label': 'Throughput (Mtxns/sec)',
        'series_names': ('MSTO','MSTO+CU+TS','Cicada','ERMIA'),
        'legends_on': True,
        'legend_order': (1,2,0,3),
        'markevery': {
            'c': (0.4, 0.01),
            'e': (0.15, 0.01)
        }
    }
    NAME = MVSTOConfig.NAME
    TYPE = GraphType.LINE
    DIM1 = MVSTOConfig.DIM1
    DIM2 = ['m','m.c.s','c','e']
    DIM3 = ['1', '4', '0']
    LEGENDS = [False, True, False]
    D3YMAXES = [None, None, None]
    D3TITLES = ['', '', '']
    D3FNAMES = ['tpcc_mvcc_comp_w1', 'tpcc_mvcc_comp_w4', 'tpcc_mvcc_comp_part']


# Investigating alternative RTID/abort on read-time delta version flattening
# MVCC only
class TMVFlattenGraphConfig:
    INFO = {
        'x_label': '# threads',
        'y_label': 'Throughput (Mtxns/sec)',
        'series_names': ('MVCC','MVCC-','MVCC+CU','MVCC+CU-','MVCC+CU+TS','MVCC+CU+TS-'),
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
        'series_names': ('OSTO', 'OSTO + CU', 'OSTO + SV', 'OSTO + CU + SV'),
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
        'series_names': ('MSTO', 'MSTO + CU', 'MSTO + SV', 'MSTO + CU + SV',
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
        'series_names': ('OSTO', 'OSTO + CU', 'OSTO + SV', 'OSTO + CU + SV',
                         'MSTO', 'MSTO + CU', 'MSTO + SV', 'MSTO + CU + SV'),
        'legends_on': True
    }
    NAME = MVSTOYCSBConfig.NAME
    TYPE = GraphType.LINE
    DIM1 = MVSTOYCSBConfig.DIM1
    DIM2 = MVSTOYCSBConfig.DIM2
    DIM3 = MVSTOYCSBConfig.DIM3
    LEGENDS = [True, True]
    D3YMAXES = [None, None]
    D3TITLES = ['YCSB-A', 'YCSB-B']
    D3FNAMES = ['ycsb_a', 'ycsb_b']


class MVSTOYCSBOCCGraphConfig:
    INFO = {
        'x_label': '# threads',
        'y_label': 'Throughput (Mtxns/sec)',
        'series_names': ('OSTO', 'OSTO + CU', 'OSTO + SV', 'OSTO + CU + SV'),
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
