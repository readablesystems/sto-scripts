#!/usr/bin/env python

import os,re,subprocess,json,numpy
import optparse
from matplotlib import pyplot as plt

capture_time = 'real time: ([0-9\.]*)'
capture_abort = '[0-9]* \(([0-9\.]*)%\) aborts'

dev_warning_threshold = 0.05

ntrails = 3

skewness = [0.4, 0.8, 1.2]
contention = ['low', 'med', 'high']
data_structures = ['array-nonopaque', 'array']

write_fracs = [0.1, 0.3, 0.5, 0.7, 0.9]
readonly_fracs = [0.0, 0.2, 0.4, 0.6, 0.8]

def run_tictoc(result_group, write_pct, ro_txn_pct):
    # make sure we are on the tictoc branch
    if not os.path.exists('./TicTocVersions.hh'):
        print "No can do tictoc branch please"
        exit()

    # build tictoc uncompressed
    print 'building tictoc'
    subprocess.check_output(['make', 'PROFILE_COUNTERS=1', 'concurrent'], stderr=subprocess.STDOUT)
    results = benchmark_zipf('concurrent', 'tictoc', ntrails, write_pct, ro_txn_pct)
    insert_results(result_group, results)

    subprocess.check_output(['make', 'clean'], stderr=subprocess.STDOUT)

    # ignoring compression for now

    #build tictoc compressed
    #print 'building tictoc compressed'
    #subprocess.check_output(['make', 'PROFILE_COUNTERS=1', 'TICTOC_COMPOUND=1', 'concurrent'], stderr=subprocess.STDOUT)
    #results = benchmark_zipf('concurrent', 'tictoc compressed', ntrails)
    #insert_results(result_group, results)

    #subprocess.check_output(['make', 'clean'], stderr=subprocess.STDOUT)

def run_sto(result_group, write_pct, ro_txn_pct):
    # make sure we are on master branch
    if os.path.exists('./TicTocVersions.hh'):
        print "No can do master branch please"
        exit()

    # build
    print 'building sto'
    subprocess.check_output(['make', 'PROFILE_COUNTERS=1', 'concurrent'], stderr=subprocess.STDOUT)
    results = benchmark_zipf('concurrent', 'sto', ntrails, write_pct, ro_txn_pct)
    insert_results(result_group, results)

    subprocess.check_output(['make', 'clean'], stderr=subprocess.STDOUT)

def benchmark_zipf(program, series_name, ntrails, write_pct, ro_txn_pct):
    results = {}
    default_record = {'time':0.0, 'abort':0.0, 'time_min':0.0, 'time_max':0.0}

    for c in contention:
        r = {}
        r[series_name] = default_record.copy()
        r[series_name+' opaque'] = default_record.copy()
        results[c] = r

    for ds in data_structures:
        for s in skewness:
            subcmd = './{0} 8 {1} --skew={2} --writepercent={3} --readonlypercent={4} --ntrans=10000000 --nthreads=16'.format(program, ds, s, write_pct, ro_txn_pct)
            cmd_string = 'taskset -c 0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,38,40,42,44,46 ' + subcmd
            config_results = {'times':[], 'aborts':[]}
            for n in range(ntrails):
                print '{0}: {1}'.format(n, subcmd)
                out = subprocess.check_output(cmd_string.split(' '), stderr=subprocess.STDOUT)
                time_s = re.search(capture_time, out).group(1)
                abort_s = re.search(capture_abort, out).group(1)
                config_results['times'].append(float(time_s))
                config_results['aborts'].append(float(abort_s))
            if ds == 'array':
                register_results(results[contention[skewness.index(s)]][series_name+' opaque'], config_results)
            else:
                register_results(results[contention[skewness.index(s)]][series_name], config_results)

    return results

def register_results(record, config_results):
    med_time = numpy.median(config_results['times'])
    max_time = numpy.amax(config_results['times'])
    min_time = numpy.amin(config_results['times'])

    record['time']     = med_time
    record['abort']    = config_results['aborts'][config_results['times'].index(med_time)]
    record['time_min'] = min_time
    record['time_max'] = max_time

    if ((max_time-med_time)/med_time > dev_warning_threshold) or ((med_time-min_time)/med_time > dev_warning_threshold):
        print 'Warning: high variation (median {0}, min {1}, max{2})'.format(med_time, min_time, max_time)

def insert_results(result_group, results):
    for c in results.keys():
        for s in results[c].keys():
            if not s in result_group[c]:
                result_group[c][s] = {}
            result_group[c][s]['time']  = results[c][s]['time']
            result_group[c][s]['abort'] = results[c][s]['abort']

def print_result_group(result_group):
    print 'Throughput (x1000 txns/sec/thread):'
    print ',low,med,high,'

    for s in result_group['low']:
        ln = s + ','
        ln += '{:.2f},'.format(10000.0 / 16.0 / result_group['low'][s]['time'])
        ln += '{:.2f},'.format(10000.0 / 16.0 / result_group['med'][s]['time'])
        ln += '{:.2f},'.format(10000.0 / 16.0 / result_group['high'][s]['time'])
        print ln

    print 'Abort rates:'
    print ',low,med,high,'

    for s in result_group['low']:
        ln = s + ','
        ln += '{}%,'.format(result_group['low'][s]['abort'])
        ln += '{}%,'.format(result_group['med'][s]['abort'])
        ln += '{}%,'.format(result_group['high'][s]['abort'])
        print ln

def print_results_contour(overall_results, cont_level, sot_name, base_name):
    ret = []
    print '\n### Overall results (contour -- {} contention) ###'.format(cont_level)
    print 'x-axis: fraction of read-only txns, y-axis: fraction of write ops in non-read-only txns\n'
    print ',{},'.format(','.join(['{}'.format(n) for n in readonly_fracs]))

    for y in range(len(write_fracs)):
        ln = '{},'.format(write_fracs[y])
        larr = []
        for x in range(len(readonly_fracs)):
            sot_throughput = 10000.0/16.0/overall_results[x][y][cont_level][sot_name]['time']
            base_throughput = 10000.0/16.0/overall_results[x][y][cont_level][base_name]['time']
            spdup = (sot_throughput - base_throughput)*100.0 / base_throughput
            ln += '{:.4f},'.format(spdup)
            larr.append(spdup)
        ret.append(larr)
        print ln
    return numpy.array(ret)

def new_result_group():
    result_group = {}
    for c in contention:
        result_group[c] = {}
    return result_group

def make_figure_contour(titles, result_matrices, fig_title, filename):
    x = readonly_fracs
    y = write_fracs
    X, Y = numpy.meshgrid(x,y)
    levels = numpy.linspace(-60,30,46)

    fig, axs = plt.subplots(1,len(result_matrices),figsize=((len(result_matrices))*5,5))

    for idx, m in enumerate(result_matrices):
        cs = axs[idx].contour(X, Y, m, levels=levels)
        cbar = fig.colorbar(cs, ax=axs[idx], format='%.0f%%', fraction=0.046, pad=0.04)
        plt.clabel(cs, inline=True, fmt='%.0f%%')
        axs[idx].set_title(titles[idx])
        axs[idx].set_aspect('equal')
        if idx == 0:
            axs[idx].set_xlabel('fraction of read-only txns')
            axs[idx].set_ylabel('fraction of writes in non-read-only txns')
            cbar.ax.set_ylabel('speed up')

    fig.subplots_adjust(wspace=0.5,
                        hspace=0.3,
                        left=0.05,
                        right=0.95,
                        top=0.9,
                        bottom=0.1)
    fig.suptitle(fig_title, fontsize=16)
    plt.savefig(filename)
    plt.show()

def get_comparisons(overall_results, sot_name, base_name):
    low_zmat = print_results_contour(overall_results, 'low', sot_name, base_name)
    med_zmat = print_results_contour(overall_results, 'med', sot_name, base_name)
    high_zmat = print_results_contour(overall_results, 'high', sot_name, base_name)
    return (('low contention', 'med contention', 'high contention'), (low_zmat, med_zmat, high_zmat))

def main():
    parser = optparse.OptionParser()
    parser.add_option('-l', action="store", dest="l", default='')
    parser.add_option('-f', action="store_true", dest="f", default=False)
    options, args = parser.parse_args()

    if options.l != '':
        with open(options.l, 'r') as input_file:
            overall_results = json.load(input_file)
    else:
        overall_results = [[new_result_group() for y in range(len(write_fracs))] for x in range(len(readonly_fracs))]

        print 'swicth to tictoc branch'
        os.system('git checkout tictoc')
        for x in range(len(readonly_fracs)):
            for y in range(len(write_fracs)):
                run_tictoc(overall_results[x][y], write_fracs[y], readonly_fracs[x])
        print 'switch to master branch'
        os.system('git checkout master')
        for x in range(len(readonly_fracs)):
            for y in range(len(write_fracs)):
                run_sto(overall_results[x][y], write_fracs[y], readonly_fracs[x])
        print 'ALL DONE'
        with open('tictoc_results.json', 'w') as outfile:
            json.dump(overall_results, outfile)

    r1 = get_comparisons(overall_results, 'tictoc', 'sto')
    r2 = get_comparisons(overall_results, 'tictoc opaque', 'sto opaque')

    if options.f == True:
        make_figure_contour(r1[0], r1[1], 'Speed up of TicToc over STO without opacity', 'nonopaque.pdf')
        make_figure_contour(r2[0], r2[1], 'Speed up of TicToc over STO with opacity', 'opaque.pdf')

if __name__ == '__main__':
    main()
