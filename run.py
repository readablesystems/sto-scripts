#!/usr/bin/env python3

from runner import BenchRunner
from runner import TPCCRunner
from runner import WikiRunner
import optparse, json, os
import config as bc

bm = {
    'tpcc': bc.TPCCConfig(),
    'wiki': bc.WikiConfig()
}

rm = {
    'tpcc': TPCCRunner,
    'wiki': WikiRunner
}


def result_file_name(name):
    return 'results/json/{}_results.json'.format(name)


def get_runner_and_file(bench_name):
    if bench_name in bm:
        return (rm[bench_name](bm[bench_name].NAME, bm[bench_name].DIM1, bm[bench_name].DIM2, bm[bench_name].DIM3),
                result_file_name(bm[bench_name].NAME))
    else:
        print('unknown benchmark: {}'.format(bench_name))
        exit()


if __name__ == '__main__':
    psr = optparse.OptionParser()
    psr.add_option("-f", "--force-update", action="store_true", dest="force_update", default=False)
    psr.add_option("-d", "--dry-run", action="store_true", dest="dry_run", default=False)
    psr.add_option("-n", "--num-trails", action="store", type="int", nargs=1, dest="ntrails", default=[0])

    opts, args = psr.parse_args()

    if len(args) != 1:
        psr.error("Incorrect number of arguments")

    BenchRunner.set_dry_run(opts.dry_run)
    if opts.ntrails[0] != 0:
        BenchRunner.set_num_trails(opts.dry_run)

    (runner, result_file) = get_runner_and_file(args[0])

    old_results = None
    if os.path.exists(result_file) and not opts.force_update:
        with open(result_file, 'r') as rf:
            old_results = json.load(rf)
    else:
        old_results = {}

    new_results = runner.run_all(old_results)
    print('ALL DONE')

    if opts.dry_run:
        exit()

    with open(result_file, 'w') as ofile:
        json.dump(new_results, ofile, indent=4, sort_keys=True)

    print('Result file {} saved/updated.'.format(result_file))
