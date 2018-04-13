# Common methods

import sys


def fatal_error(msg):
    print('Fatal error: ' + msg, file=sys.stderr)
    sys.exit(1)


def get_result_file(bench_name):
    return 'results/json/{}_results.json'.format(bench_name)


# Benchmark configurations


class TPCCConfig:
    NAME = 'tpcc'
    DIM1 = [8, 16, 24, 32, 64, 96, 128]
    DIM2 = ['default', 'swiss', 'adaptive', '2pl', 'tictoc']
    DIM3 = ['low,coarse', 'low,fine', 'high,coarse', 'high,fine']


class WikiConfig:
    NAME = 'wiki'
    DIM1 = [8, 16, 24, 32, 48]
    DIM2 = ['coarse', 'fine']
    DIM3 = ['one']


# Graph config


class TPCCGraphConfig:
    INFO = {
        'x_label': '# threads',
        'y_label': 'Throughput (Mtxns/sec)',
        'series_names': ('Coarse', 'Fine'),
        'fill_colors': ('black', 'white', 'white', 'white', 'white'),
        'hatches': ('', '++', '///', 'xx', ''),
        'legends_on': True
    }
    DIM1 = TPCCConfig.DIM1
    DIM2 = TPCCConfig.DIM2
    DIM3 = TPCCConfig.DIM3
    D3TITLES = ['High contention TPC-C (8 warehouses fixed)']
    D3FNAMES = ['tpcc_bench']


class WikiGraphConfig:
    INFO = {
        'x_label': '# threads',
        'y_label': 'Throughput (Mtxns/sec)',
        'series_names': ('Coarse', 'Fine'),
        'fill_colors': ('black', 'white', 'white', 'white', 'white'),
        'hatches': ('', '++', '///', 'xx', ''),
        'legends_on': True
    }
    DIM1 = WikiConfig.DIM1
    DIM2 = WikiConfig.DIM2
    DIM3 = WikiConfig.DIM3
    D3TITLES = ['untitled']
    D3FNAMES = ['wiki_bench']
