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


class MVSTOTPCCNonCumuFactorsConfig:
    NAME = 'tpcc_noncumu_factors'
    DIM1 = [1, 2, 4, 12, 24, 32, 40, 48, 64]
    DIM2 = ['m-a', 'm-e', 'm-r', 'm-h', 'm', 'o-a', 'o-e', 'o-r', 'o-h', 'o']
    DIM3 = ['1', '4', '0']


class MVSTOTPCCStackedFactorsConfig:
    NAME = 'tpcc_stacked_factors'
    DIM1 = [1, 2, 4, 12, 24, 32, 40, 48, 64]
    DIM2 = ['mn', 'mn.a', 'mn.a.e', 'mn.a.r.e', 'mn.a.r.e.h']
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
    'o': 18,
    'o.s': 4,
    'o.c': 2,
    'o.c.s': 6,
    'onr': 9,
    'm': (16, 76, 100),
    'm.c': 2,
    'm.s': 4,
    'm.s.i': 4,
    'm.c.s': 6,
    'm.c.s.i': 6,
    'mvp': (16, 76, 100),
    'mvp.s': 5,
    'mvp.c': 7,
    'mvp.c.s': 9,
    'c': 8,
    'e': 10,
    'mocc': 12,
    'tictoc': 0,
    'tictoc.c': 2,
    'tictoc.s': 4,
    'tictoc.c.s': 6,
    'ttcc-wrong':  3,
    'ttcc-wrong.s': 5,
    'ttcc-wrong.c': 7,
    'ttcc-wrong.c.s': 9,
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
    'mn.a.e': 6,
    'mn.a.r.e': 8,
    'mn.a.r.e.h': 0,
    'm-a': 2,
    'm-e': 4,
    'm-r': 6,
    'm-h': 8,
    'on.a': 4,
    'on.a.e': 6,
    'on.a.r.e': 8,
    'on.a.r.e.h': 0,
    'o-a': 2,
    'o-e': 4,
    'o-r': 6,
    'o-h': 8,
    'o-base': 18,
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
    'mvp': 'x',
    'mvp.s': 'x',
    'mvp.c': 'x',
    'mvp.c.s': 'x',
    'c':       '^',
    'e':       '>',
    'mocc':    'd',
    'tictoc':  '$T$',
    'tictoc.s': '$T$',
    'tictoc.c': '$T$',
    'tictoc.c.s': '$T$',
    'ttcc-wrong':  '$T$',
    'ttcc-wrong.s': '$T$',
    'ttcc-wrong.c': '$T$',
    'ttcc-wrong.c.s': '$T$',
    'mf':      'h',
    'mf.c':    'H',
    'mf.c.s':  'x',
    # stacked factors line graph
    'mn': 'p',
    'mn.a': 'p',
    'mn.a.e': 'p',
    'mn.a.r.e': 'p',
    'mn.a.r.e.h': 'x',
    'on.a': 'p',
    'on.a.e': 'p',
    'on.a.r.e': 'p',
    'on.a.r.e.h': 'x',
    'm-a': 'p',
    'm-e': 'p',
    'm-r': 'p',
    'm-h': 'p',
    'o-a': 'o',
    'o-e': '^',
    'o-r': 'v',
    'o-h': 's',
    'o-base': None,
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
    'tictoc.s': 'dotted',
    'tictoc.c': 'dashed',
    'tictoc.c.s': 'dashdot',
    'ttcc-wrong.s': 'dotted',
    'ttcc-wrong.c': 'dotted',
    'ttcc-wrong.c.s': 'dotted',
}

linewidth_mapping = {
    'secondary': 1.25,
    'default': 2,
    'mocc': 3,
    'c': 3,
    'e': 3,
    'o-base': 4,
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


# TPCC Scalability graphs with merged subfigures
# Sharing y-axes for OCC and MVCC schemes (to get rid of the grey lines)
class TScalabilityMergedGraphConfig:
    INFO = {
        'x_label': '# threads',
        'y_label': 'Throughput (Mtxns/sec)',
        'combine_subfigures': 'share-y',
        'subfigure_series_names': (('OSTO', 'OSTO+CU', 'OSTO+TS', 'OSTO+CU+TS'),
                                   ('MSTO', 'MSTO+CU', 'MSTO+TS', 'MSTO+CU+TS')),
        'legends_on': True,
        'legend_order': (3, 2, 1, 0)
    }
    NAME = MVSTOConfig.NAME
    TYPE = GraphType.LINE
    DIM1 = MVSTOConfig.DIM1
    DIM2 = ('o','o.c','o.s','o.c.s','m','m.c','m.s','m.c.s')
    SUBFIG_DIM2S = (('o','o.c','o.s','o.c.s'),('m','m.c','m.s','m.c.s'))
    DIM3 = ['1', '4', '0']
    LEGENDS = [False, True, True]
    D3YMAXES = [1.6, 4.1, 5.0]
    D3TITLES = ['', '', '']
    D3FNAMES = ['tpcc_om_w1', 'tpcc_om_w4', 'tpcc_om_part']


# TPC-C baselines comparison, OCC vs TicToc vs MVCC
class TPCCBaselinesGraphConfig:
    INFO = {
        'x_label': '# threads',
        'y_label': 'Throughput (Mtxns/sec)',
        'series_names': ('OSTO', 'TSTO', 'MSTO'),
        'legends_on': True
    }
    NAME = MVSTOConfig.NAME
    TYPE = GraphType.LINE
    DIM1 = MVSTOConfig.DIM1
    DIM2 = ['o','tictoc','mvp']
    DIM3 = ['1', '0']
    LEGENDS = [True, False]
    D3YMAXES = [None, None]
    D3TITLES = ['', '']
    D3FNAMES = ['tpcc_baselines_w1', 'tpcc_baselines_part']


# TPC-C Cross-system comparison: OCC, TicToc, MVCC, Cicada, ERMIA, MOCC
class TPCCXSystemGraphConfig:
    INFO = {
        'x_label': '# threads',
        'y_label': 'Throughput (Mtxns/sec)',
        'combine_subfigures': 'share-y',
        'subfigure_series_names': (('OSTO', 'MOCC'), ('TSTO',), ('MSTO', 'Cicada', 'ERMIA', '')),
        'legends_on': True
    }
    NAME = MVSTOConfig.NAME
    TYPE = GraphType.LINE
    LEGEND_FONT_SIZE = 20
    DIM1 = MVSTOConfig.DIM1
    DIM2 = None
    DIM3 = ['1', '0']
    SUBFIG_DIM2S = (('o','mocc'),('tictoc',),('mvp','c','e',None))
    LEGENDS = [True, True]
    D3YMAXES = [0.8, 5]
    D3TITLES = ['', '']
    D3FNAMES = ['tpcc_xsys_w1', 'tpcc_xsys_part']
    WIDE_FIG_SIZE = (12,5)


# TPC-C baseline vs CU+TS comparison graphs, low and high contention
# OCC vs TicToc vs MVCC
class TPCCSemanticOptGraphConfig:
    INFO = {
        'x_label': '# threads',
        'y_label': 'Throughput (Mtxns/sec)',
        'combine_subfigures': 'share-y',
        'subfigure_series_names': (('OSTO', 'OSTO+CU+TS'),
                                   ('TSTO', 'TSTO+CU+TS'),
                                   ('MSTO', 'MSTO+CU+TS')),
        'legends_on': True,
        'legend_order': (1,0)
    }
    NAME = MVSTOConfig.NAME
    TYPE = GraphType.LINE
    LEGEND_FONT_SIZE = 18
    DIM1 = MVSTOConfig.DIM1
    DIM2 = None
    DIM3 = ['1', '4', '0']
    SUBFIG_DIM2S = (('o','o.c.s'),('tictoc','tictoc.c.s'),('mvp','m.c.s'))
    LEGENDS = [True, True, True]
    D3YMAXES = [2.4, None, None]
    D3TITLES = ['','','']
    D3FNAMES = ['tpcc_semopt_w1','tpcc_semopt_w4','tpcc_semopt_part']
    #WIDE_FIG_SIZE = (16,5)


# TPC-C Individual CU/TS improvement graphs
# OCC vs TicToc vs MVCC
class TPCCSemanticIndGraphConfig:
    INFO = {
        'x_label': '# threads',
        'y_label': 'Throughput (Mtxns/sec)',
        'combine_subfigures': 'share-y',
        'subfigure_series_names': (('OSTO+CU', 'OSTO+TS'),('TSTO+CU', 'TSTO+TS'),('MSTO+CU', 'MSTO+TS')),
        'legends_on': True
    }
    NAME = MVSTOConfig.NAME
    TYPE = GraphType.LINE
    DIM1 = MVSTOConfig.DIM1
    DIM2 = None
    DIM3 = ['1', '0']
    SUBFIG_DIM2S = (('o.c','o.s'),('tictoc.c','tictoc.s'),('m.c','m.s'))
    LEGENDS = [True, True]
    D3YMAXES = [1.6, None]
    D3TITLES = ['','']
    D3FNAMES = ['tpcc_semind_w1','tpcc_semind_part']


# Comparing TicToc without and without full phantom protection (leaf node TicToc timestamp)
class TPCCTicTocPhantomProtectionGraphConfig:
    INFO = {
        'x_label': '# threads',
        'y_label': 'Throughput (Mtxns/sec)',
        'combine_subfigures': 'share-y',
        'subfigure_series_names': (('TSTO', 'TSTO-pp'),('TSTO+CU+TS', 'TSTO+CU+TS-pp')),
        'legends_on': True
    }
    NAME = MVSTOConfig.NAME
    TYPE = GraphType.LINE
    DIM1 = MVSTOConfig.DIM1
    DIM2 = None
    SUBFIG_DIM2S = (('tictoc', 'ttcc-wrong'), ('tictoc.c.s', 'ttcc-wrong.c.s'))
    DIM3 = ['1', '4', '0']
    LEGENDS = [True, True, True]
    D3YMAXES = [1.4, 4.0, None]
    D3TITLES = ['', '', '']
    D3FNAMES = ['tpcc_tictoc_ppcost_w1', 'tpcc_tictoc_ppcost_w4', 'tpcc_tictoc_ppcost_part']


# Comparing TS implementation in MVCC: Integrated (current default) vs. Vertical Partitioning
class TPCCMVCCTsImplGraphConfig:
    INFO = {
        'x_label': '# threads',
        'y_label': 'Throughput (Mtxns/sec)',
        'combine_subfigures': 'share-y',
        'subfigure_series_names': (('MSTO+TS', 'MSTO+TS(vp)'),('MSTO+CU+TS', 'TSTO+CU+TS(vp)')),
        'legends_on': True
    }
    NAME = MVSTOConfig.NAME
    TYPE = GraphType.LINE
    DIM1 = MVSTOConfig.DIM1
    DIM2 = None
    SUBFIG_DIM2S = (('m.s', 'mvp.s'), ('m.c.s', 'mvp.c.s'))
    DIM3 = ['1', '4', '0']
    LEGENDS = [True, True, True]
    D3YMAXES = [2.2, 2.2, None]
    D3TITLES = ['', '', '']
    D3FNAMES = ['tpcc_mvcc_tscomp_w1', 'tpcc_mvcc_tscomp_w4', 'tpcc_mvcc_tscomp_part']



class TPCCDramaticGraphConfig:
    INFO = {
        'x_label': '# threads',
        'y_label': 'Throughput (Mtxns/sec)',
        'series_names': ('OCC', 'MVCC', 'OCC+CU+TS'),
        'legends_on': True
    }
    NAME = MVSTOConfig.NAME
    TYPE = GraphType.LINE
    DIM1 = MVSTOConfig.DIM1
    DIM2 = ['o','m']
    DIM3 = ['1']
    LEGENDS = [True]
    D3YMAXES = [1.4]
    D3TITLES = ['']
    D3FNAMES = ['tpcc_dramatic_peek_w1']
    FIG_SIZE = (10.6,6)


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


# YCSB Scalability OCC vs MVCC side-by-side comparison graphs
class YScalabilityMergedGraphConfig:
    INFO = {
        'x_label': '# threads',
        'y_label': 'Throughput (Mtxns/sec)',
        'combine_subfigures': 'share-y',
        'subfigure_series_names': (('OSTO', 'OSTO+CU', 'OSTO+TS', 'OSTO+CU+TS'),
                                   ('MSTO', 'MSTO+CU', 'MSTO+TS', 'MSTO+CU+TS')),
        'legends_on': True,
        'legend_order': (3, 2, 1, 0)
    }
    NAME = MVSTOYCSBConfig.NAME
    TYPE = GraphType.LINE
    DIM1 = MVSTOYCSBConfig.DIM1
    DIM2 = ['o','o.c','o.s','o.c.s','m','m.c','m.s','m.c.s']
    SUBFIG_DIM2S = (('o','o.c','o.s','o.c.s'),('m','m.c','m.s','m.c.s'))
    DIM3 = ['a', 'b']
    LEGENDS = [True, False]
    D3YMAXES = [3.0, 11.0]
    D3TITLES = ['', '']
    D3FNAMES = ['ycsb_om_a', 'ycsb_om_b']


# YCSB Scalability OCC vs MVCC side-by-side comparison graphs
class YCSBSemanticOptGraphConfig:
    INFO = {
        'x_label': '# threads',
        'y_label': 'Throughput (Mtxns/sec)',
        'combine_subfigures': 'share-y',
        'subfigure_series_names': (('OSTO', 'OSTO+CU+TS'), ('TSTO', 'TSTO+CU+TS'),
                                   ('MSTO', 'MSTO+CU+TS')),
        'legends_on': True,
        'legend_order': (1,0)
    }
    NAME = YCSBTicTocCompConfig.NAME
    TYPE = GraphType.LINE
    LEGEND_FONT_SIZE = 18
    DIM1 = YCSBTicTocCompConfig.DIM1
    DIM2 = None
    SUBFIG_DIM2S = (('o','o.c.s'),('tictoc','tictoc.c.s'),('m','m.c.s'))
    DIM3 = ['a', 'b']
    LEGENDS = [True, True]
    D3YMAXES = [3.0, 11.0]
    D3TITLES = ['', '']
    D3FNAMES = ['ycsb_semopt_a', 'ycsb_semopt_b']


# YCSB Scalability OCC vs MVCC side-by-side comparison graphs
class YCSBSemanticIndGraphConfig:
    INFO = {
        'x_label': '# threads',
        'y_label': 'Throughput (Mtxns/sec)',
        'combine_subfigures': 'share-y',
        'subfigure_series_names': (('OSTO', 'OSTO+CU', 'OSTO+TS', 'OSTO+CU+TS'), ('TSTO', 'TSTO+CU', 'TSTO+TS', 'TSTO+CU+TS'),
                                   ('MSTO', 'MSTO+CU', 'MSTO+TS', 'MSTO+CU+TS')),
        'legends_on': True,
        'legend_order': (2,1,0)
    }
    NAME = YCSBTicTocCompConfig.NAME
    TYPE = GraphType.LINE
    DIM1 = YCSBTicTocCompConfig.DIM1
    DIM2 = None
    SUBFIG_DIM2S = (('o','o.c','o.s','o.c.s'),('tictoc','tictoc.c','tictoc.s','tictoc.c.s'),('m','m.c','m.s','m.c.s'))
    DIM3 = ['a', 'b']
    LEGENDS = [True, True]
    D3YMAXES = [3.0, 11.0]
    D3TITLES = ['', '']
    D3FNAMES = ['ycsb_semind_a', 'ycsb_semind_b']


# YCSB baseline graphs OCC vs TicToc vs MVCC
class YCSBBaselinesGraphConfig:
    INFO = {
        'x_label': '# threads',
        'y_label': 'Throughput (Mtxns/sec)',
        'series_names': ('OSTO', 'TSTO', 'MSTO'),
        'legends_on': True,
    }
    NAME = YCSBTicTocCompConfig.NAME
    TYPE = GraphType.LINE
    DIM1 = YCSBTicTocCompConfig.DIM1
    DIM2 = ['o', 'tictoc', 'm']
    DIM3 = ['a', 'b']
    LEGENDS = [True, True]
    D3YMAXES = [None, None]
    D3TITLES = ['', '']
    D3FNAMES = ['ycsb_a_baselines', 'ycsb_b_baselines']


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


# Wikipedia baseline comparisons (OCC, TicToc, MVCC)
class WikiBaselineGraphConfig:
    INFO = {
        'x_label': '# threads',
        'y_label': 'Throughput (Mtxns/sec)',
        'series_names': ('OSTO', 'TSTO', 'MSTO'),
        'legends_on': True,
    }
    NAME = MVSTOWikiConfig.NAME
    TYPE = GraphType.LINE
    DIM1 = MVSTOWikiConfig.DIM1
    DIM2 = ['o', 'tictoc', 'm']
    DIM3 = ['1']
    LEGENDS = [True, True]
    D3YMAXES = [None, None]
    D3TITLES = ['', '']
    D3FNAMES = ['wiki_baselines']


# Wikipedia OCC, MVCC side-by-side comparison graphs
class WikiSideBySideGraphConfig:
    INFO = {
        'x_label': '# threads',
        'y_label': 'Throughput (Mtxns/sec)',
        'combine_subfigures': 'share-y',
        'subfigure_series_names': (('OSTO', 'OSTO+CU+TS'),
                                   ('TSTO', 'TSTO+CU+TS'),
                                   ('MSTO', 'MSTO+CU+TS')),
        'legends_on': True,
        'legend_order': (1,0)
    }
    NAME = MVSTOWikiConfig.NAME
    TYPE = GraphType.LINE
    DIM1 = MVSTOWikiConfig.DIM1
    DIM2 = None
    SUBFIG_DIM2S = (('o','o.c.s'),('tictoc','tictoc.c.s'),('m','m.c.s'))
    DIM3 = ['1']
    LEGENDS = [True]
    D3YMAXES = [0.6]
    D3TITLES = ['']
    D3FNAMES = ['wiki_otm']


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


class RubisBaselineGraphConfig:
    INFO = {
        'x_label': '# threads',
        'y_label': 'Throughput (Mtxns/sec)',
        'series_names': ('OSTO', 'TSTO', 'MSTO'),
        'legends_on': True,
    }
    NAME = MVSTORubisConfig.NAME
    TYPE = GraphType.LINE
    DIM1 = MVSTORubisConfig.DIM1
    DIM2 = ['o', 'tictoc', 'm']
    DIM3 = ['1']
    LEGENDS = [True, True]
    D3YMAXES = [None, None]
    D3TITLES = ['', '']
    D3FNAMES = ['rubis_baselines']


# Rubis OCC, MVCC side-by-side comparison graphs
class RubisSideBySideGraphConfig:
    INFO = {
        'x_label': '# threads',
        'y_label': 'Throughput (Mtxns/sec)',
        'combine_subfigures': 'share-y',
        'subfigure_series_names': (('OSTO', 'OSTO+CU+TS'),
                                   ('TSTO', 'TSTO+CU+TS'),
                                   ('MSTO', 'MSTO+CU+TS')),
        'legends_on': True,
        'legend_order': (1,0)
    }
    NAME = MVSTORubisConfig.NAME
    TYPE = GraphType.LINE
    DIM1 = MVSTORubisConfig.DIM1
    DIM2 = None
    SUBFIG_DIM2S = (('o','o.c.s'),('tictoc','tictoc.c.s'),('m','m.c.s'))
    DIM3 = ['1']
    LEGENDS = [True]
    D3YMAXES = [4.5]
    D3TITLES = ['']
    D3FNAMES = ['rubis_otm']


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


# TPC-C non cumulative factor analysis garphs
class TPCCNonCumuFactorsMVCCGraphConfig:
    INFO = {
        'x_label': '# threads',
        'y_label': 'Throughput (Mtxns/sec)',
        'series_names': ('-RPMalloc', '-NoExcept', '-Backoff', '-HashIdx', 'MSTO'),
        'legends_on': True
    }
    NAME = MVSTOTPCCNonCumuFactorsConfig.NAME
    TYPE = GraphType.LINE
    DIM1 = [1, 2, 4, 12, 24, 32, 40, 48, 64]
    DIM2 = ['m-a', 'm-e', 'm-r', 'm-h', 'm']
    DIM3 = ['1', '4', '0']
    LEGENDS = [True, True, True]
    D3YMAXES = [None, None, None]
    D3TITLES = ['', '', '']
    D3FNAMES = ['tpcc_noncumu_factors_mvcc_w1',
                'tpcc_noncumu_factors_mvcc_w4',
                'tpcc_noncumu_factors_mvcc_part']
    FIG_SIZE = (6, 6)


class TPCCNonCumuFactorsOCCGraphConfig:
    INFO = {
        'x_label': '# threads',
        'y_label': 'Throughput (Mtxns/sec)',
        'series_names': ('Slow allocator', 'Inefficient aborts', 'No contention\nregulation', 'No hash indexes', 'OSTO Baseline                      '),
        'legends_on': True,
        'legend_order': (4,2,0,1,3),
        'markevery': {
            'o-base': 5,
            'o-a': 5,
            'o-e': 5,
            'o-r': 5,
            'o-h': 5
        },
    }
    NAME = MVSTOTPCCNonCumuFactorsConfig.NAME
    TYPE = GraphType.LINE
    DIM1 = [1, 2, 4, 12, 24, 32, 40, 48, 64]
    DIM2 = ['o-a', 'o-e', 'o-r', 'o-h', 'o-base']
    DIM3 = ['1', '0']
    LEGENDS = [True, True]
    LEGEND_SELECT = [(0,3), (3,5)]
    D3YMAXES = [None, None, None]
    D3TITLES = ['', '']
    D3FNAMES = ['tpcc_noncumu_factors_occ_w1',
                'tpcc_noncumu_factors_occ_part']
    #FIG_SIZE = (6, 6)


# TPC-C stacked factor analysis, MVCC only
class TPCCStackedFactorsGraphConfig:
    INFO = {
        'x_label': '# threads',
        'y_label': 'Throughput (Mtxns/sec)',
        'series_names': ('NoOpt', '+Allocator', '+NoExcept', '+Backoff', '+HashIdx'),
        'legends_on': True
    }
    NAME = MVSTOTPCCStackedFactorsConfig.NAME
    TYPE = GraphType.LINE
    DIM1 = [1, 2, 4, 12, 24, 32, 40, 48, 64]
    DIM2 = ['mn', 'mn.a', 'mn.a.e', 'mn.a.r.e', 'mn.a.r.e.h']
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
        'series_names': ('NoOpt', '+Allocator', '+NoExcept', '+Backoff', '+HashIdx (OSTO)'),
        'legends_on': True,
    }
    NAME = MVSTOTPCCStackedFactorsConfig.NAME
    TYPE = GraphType.LINE
    DIM1 = [1, 2, 4, 12, 24, 32, 40, 48, 64]
    DIM2 = ['on', 'on.a', 'on.a.e', 'on.a.r.e', 'on.a.r.e.h']
    DIM3 = ['1', '0']
    LEGENDS = [False, True]
    D3YMAXES = [None, None]
    D3TITLES = ['', '', '']
    D3FNAMES = ['tpcc_stacked_factors_occ_w1', 'tpcc_stacked_factors_occ_part']
    FIG_SIZE = (6.1,6.1)


# Index contention graph, showing throughput of delivery transactions only
# Note the scale factor is different (thousands instead of millions)
class TPCCIndexContentionGraphConfig:
    INFO = {
        'x_label': '# threads',
        'y_label': 'Throughput (Ktxns/sec)',
        'scale_factor': 1000.0,
        'series_names': ('Index contention', 'OSTO'),
        'legends_on': True,
        'legend_order': (1, 0)
    }
    NAME = MVSTOTPCCIndexContentionConfig.NAME
    TYPE = GraphType.LINE
    #LEGEND_FONT_SIZE = 24
    DIM1 = [1, 2, 4, 12, 24, 32, 40, 48, 64]
    DIM2 = ['on', 'o']
    DIM3 = ['1', '0']
    LEGENDS = [True, True]
    D3YMAXES = [None, None]
    D3TITLES = ['', '']
    D3FNAMES = ['tpcc_index_contention_w1', 'tpcc_index_contention_part']
    #FIG_SIZE = (8,5)


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
        'series_names': ('MVCC','MVCC*','MVCC+CU','MVCC+CU*','MVCC+CU+TS','MVCC+CU+TS*'),
        'legends_on': True
    }
    NAME = MVSTOConfig.NAME
    TYPE = GraphType.LINE
    DIM1 = MVSTOConfig.DIM1
    DIM2 = ['m','mf','m.c','mf.c','m.c.s','mf.c.s']
    DIM3 = ['1', '4', '0']
    LEGENDS = [True, True, True]
    D3YMAXES = [None, None, None]
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
