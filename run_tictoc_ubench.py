#!/usr/bin/env python

import os,re,subprocess,numpy

capture_time = 'real time: ([0-9\.]*)'
capture_abort = '[0-9]* \(([0-9\.]*)%\) aborts'

ntrails = 3

skewness = [0.4, 0.8, 1.2]
contention = ['low', 'med', 'high']
data_structures = ['array-nonopaque', 'array']

def run_tictoc(overall_results):
    # make sure we are on the tictoc branch
    if not os.path.exists('./TicTocVersions.hh'):
        print "No can do tictoc branch please"
        exit()

    # build tictoc uncompressed
    print 'building tictoc'
    subprocess.check_output(['make', 'PROFILE_COUNTERS=1', 'concurrent'], stderr=subprocess.STDOUT)
    results = benchmark_zipf('concurrent', 'tictoc', ntrails)
    insert_results(overall_results, results)

    subprocess.check_output(['make', 'clean'], stderr=subprocess.STDOUT)

    #build tictoc compressed
    print 'building tictoc compressed'
    subprocess.check_output(['make', 'PROFILE_COUNTERS=1', 'TICTOC_COMPOUND=1', 'concurrent'], stderr=subprocess.STDOUT)
    results = benchmark_zipf('concurrent', 'tictoc compressed', ntrails)
    insert_results(overall_results, results)

    subprocess.check_output(['make', 'clean'], stderr=subprocess.STDOUT)

def run_sto(overall_results):
    # make sure we are on master branch
    if os.path.exists('./TicTocVersions.hh'):
        print "No can do master branch please"
        exit()

    # build
    print 'building sto'
    subprocess.check_output(['make', 'PROFILE_COUNTERS=1', 'concurrent'], stderr=subprocess.STDOUT)
    results = benchmark_zipf('concurrent', 'sto', ntrails)
    insert_results(overall_results, results)

    subprocess.check_output(['make', 'clean'], stderr=subprocess.STDOUT)

def benchmark_zipf(program, series_name, ntrails):
    results = {}
    default_record = {'time':0.0, 'abort':0.0, 'time_min':0.0, 'time_max':0.0}

    for c in contention:
        r = {}
        r[series_name] = default_record.copy()
        r[series_name+' opaque'] = default_record.copy()
        results[c] = r

    for ds in data_structures:
        for s in skewness:
            subcmd = './{0} 8 {1} --skew={2} --ntrans=10000000 --nthreads=16'.format(program, ds, s)
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

    record['time']     = med_time
    record['abort']    = config_results['aborts'][config_results['times'].index(med_time)]
    record['time_min'] = numpy.amin(config_results['times'])
    record['time_max'] = numpy.amax(config_results['times'])

def insert_results(overall_results, results):
    for c in results.keys():
        for s in results[c].keys():
            if not s in overall_results[c]:
                overall_results[c][s] = {}
            overall_results[c][s]['time']  = results[c][s]['time']
            overall_results[c][s]['abort'] = results[c][s]['abort']

def print_results(overall_results):
    print '### Overall Results ###'
    print 'Throughput (x1000 txns/sec/thread):'
    print ',low,med,high,'

    for s in overall_results['low']:
        ln = s + ','
        ln += '{:.2f},'.format(10000.0 / 16.0 / overall_results['low'][s]['time'])
        ln += '{:.2f},'.format(10000.0 / 16.0 / overall_results['med'][s]['time'])
        ln += '{:.2f},'.format(10000.0 / 16.0 / overall_results['high'][s]['time'])
        print ln

    print 'Abort rates:'
    print ',low,med,high,'

    for s in overall_results['low']:
        ln = s + ','
        ln += '{}%,'.format(overall_results['low'][s]['abort'])
        ln += '{}%,'.format(overall_results['med'][s]['abort'])
        ln += '{}%,'.format(overall_results['high'][s]['abort'])
        print ln

def main():
    overall_results = {}
    for c in contention:
        overall_results[c] = {}

    print 'swicth to tictoc branch'
    os.system('git checkout tictoc')
    run_tictoc(overall_results)
    print 'switch to master branch'
    os.system('git checkout master')
    run_sto(overall_results)
    print 'ALL DONE'

    print_results(overall_results)

if __name__ == '__main__':
    main()
