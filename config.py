# Benchmark configurations

class TPCCConfig:
    def __init__(self):
        self.NAME = 'tpcc'
        self.DIM1 = [8, 16, 24, 32, 64, 96, 128]
        self.DIM2 = ['default', 'swiss', 'adaptive', '2pl', 'tictoc']
        self.DIM3 = ['low,coarse', 'low,fine', 'high,coarse', 'high,fine']


class WikiConfig:
    def __init__(self):
        self.NAME = 'wiki'
        self.DIM1 = [8, 16, 24, 32, 48]
        self.DIM2 = ['coarse', 'fine']
        self.DIM3 = ['one']
