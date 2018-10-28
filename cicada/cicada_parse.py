#!/usr/bin/env python3

import numpy as np
import json
import optparse

def print_result_median(name, array):
    print("Experiment {} ({} trials)".format(name, len(array)))
    med = np.median(array)
    max = np.max(array)
    min = np.min(array)
    print("  min={:.3f}, med={:.3f}, max={:.3f}".format(min, med, max))

if __name__ == '__main__':
    usage = "Usage:"
    psr = optparse.OptionParser(usage=usage)
    psr.add_option("-f", "--input-file", action="store", dest="input_file",
                   default="cicada.json", help="Specify input file (default is cicada.json).")
    opts, args = psr.parse_args()
    if len(args) != 0:
        psr.error("Too many arguments.")
    
    with open(opts.input_file, 'r') as f:
        exp = json.load(f)

    results = exp['results']
    for name, datapoints in results.items():
        print_result_median(name, datapoints)
