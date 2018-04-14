# benchrunner base class for all benchmark runners

import subprocess, time
from sto import ProfileParser as parser


class BenchRunner:
    # We have three dimensions for each data point in our experimental data
    # (d1, d2, d3)
    # d1 is the x-axis in the graphs (e.g. number of threads)
    # d2 is the system under test (i.e. different lines/data series/color)
    # d3 is for different graph-level configs (e.g. high/low contention)

    # class variables
    dry_run = False
    num_trails = 5
    sleep_time = 2

    @classmethod
    def set_num_trails(cls, num):
        cls.num_trails = num

    @classmethod
    def set_dry_run(cls, dr):
        cls.dry_run = dr

    @classmethod
    def set_sleep_interval(cls, t):
        cls.sleep_time = t

    @classmethod
    # generate a key uniquely identifying an experiment
    # n is the trail id
    def key(cls, d1, d2, d3, n):
        return '{0}/{1}/{2}/{3}'.format(d3, d2, d1, n)

    def __init__(self, name, config_1, config_2, config_3):
        self.benchmark_name = name
        self.dimension1 = config_1
        self.dimension2 = config_2
        self.dimension3 = config_3

    # This method is for override
    def cmd_opts(self, d1, d2, d3):
        return './example-program'

    # returns triple (xput, aborts, commit-time aborts)
    def run_single(self, d1, d2, d3):
        cmd = self.cmd_opts(d1, d2, d3)
        print(cmd)

        if BenchRunner.dry_run:
            return (0, 0, 0)

        out = ''
        while True:
            retries = 0
            try:
                bytes_out = subprocess.check_output(cmd.split(' '), stderr=subprocess.STDOUT)
                out = bytes_out.decode('utf-8')
            except:
                retries += 1
                print('Subprocess error, retrying... ({})'.format(retries))
                time.sleep(BenchRunner.sleep_time)
                continue
            break

        xput = parser.extract('bench_xput', out)
        abrts = parser.extract('aborts', out)
        cabrts = parser.extract('commit_time_aborts', out)
        return (xput, abrts, cabrts)

    def run_all(self, results):
        for cnf in self.dimension3:
            for sys in self.dimension2:
                for trs in self.dimension1:
                    for n in range(BenchRunner.num_trails):
                        k = BenchRunner.key(trs, sys, cnf, n)
                        if k in results:
                            continue
                        res = self.run_single(trs, sys, cnf)
                        if BenchRunner.dry_run:
                            continue
                        results[k] = res
                        print('--gap--')
                        time.sleep(BenchRunner.sleep_time)
        return results


class TPCCRunner(BenchRunner):
    def __init__(self, *args, **kwargs):
        BenchRunner.__init__(self, *args, **kwargs)

    def cmd_opts(self, trs, sys, cnf):
        (s1, s2) = sys.split(',')
        if cnf == 'low':
            whs = trs
        else:
            whs = 8
        if s2 == 'coarse':
            exe = 'tpcc_bench_coarse'
        else:
            exe = 'tpcc_bench_fine'

        return './{0} -t{1} -w{2} --time=15.0 --dbid={3}'.format(exe, trs, whs, s1)


class WikiRunner(BenchRunner):
    def __init__(self, *args, **kwargs):
        BenchRunner.__init__(self, *args, **kwargs)

    def cmd_opts(self, trs, sys, cnf):
        # ignore cnf
        if sys == 'coarse':
            exe = 'wiki_bench_coarse'
        else:
            exe = 'wiki_bench_fine'
        return './{0} -t{1} --time=15.0'.format(exe, trs)
