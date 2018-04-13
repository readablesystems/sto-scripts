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
