#!/usr/bin/env python3

from runner import BenchRunner, TPCCRunner, WikiRunner
import config
from config import TPCCConfig, WikiConfig
import optparse, json, os, sys

brm = {
    'tpcc': (TPCCConfig, TPCCRunner),
    'wiki': (WikiConfig, WikiRunner)
}


def get_runner_and_file(bench_name):
    if bench_name in brm:
        cnf = brm[bench_name][0]
        rnr = brm[bench_name][1]
        return (rnr(cnf.NAME, cnf.DIM1, cnf.DIM2, cnf.DIM3),
                config.get_result_file(cnf.NAME))
    else:
        print('Terrible.')
        exit()


if __name__ == '__main__':
    usage = "Usage: %prog [options] benchmark\n\nSupported benchmarks: "
    usage += ', '.join(brm.keys())
    psr = optparse.OptionParser(usage=usage)
    psr.add_option("-f", "--force-update", action="store_true", dest="force_update", default=False,
                   help="Set if force overwriting existing result file. Default is False.")
    psr.add_option("-d", "--dry-run", action="store_true", dest="dry_run", default=False,
                   help="Set if want a dry run (printing out commands only). Default is False.")
    psr.add_option("-n", "--num-trails", action="store", type="int", nargs=1, dest="ntrails", default=[0],
                   help="Set the number of repeated runs for each experiment. Default is 5.")

    opts, args = psr.parse_args()

    if len(args) != 1:
        psr.error("Incorrect number of arguments.")
    BenchRunner.set_dry_run(opts.dry_run)
    if opts.ntrails[0] != 0:
        BenchRunner.set_num_trails(opts.dry_run)

    if not args[0] in brm:
        psr.error("Unknown benchmark: {}.".format(args[0]))

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
        sys.exit(0)

    with open(result_file, 'w') as ofile:
        json.dump(new_results, ofile, indent=4, sort_keys=True)

    print('Result file {} saved/updated.'.format(result_file))
