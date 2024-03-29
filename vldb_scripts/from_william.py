#!/usr/bin/env python3

import config
import json
import csv

from runner import BenchRunner as br

WILLIAM_TRIALS = 5

tpcc_occ_sys_name_map = {
    'name': 'tpcc',
    'OCC (W0)': 'o/0',
    'OCC + CU (W0)': 'o.c/0',
    'OCC (W0) + SV': 'o.s/0',
    'OCC + CU (W0) + SV': 'o.c.s/0',
    'OCC (W1)': 'o/1',
    'OCC + CU (W1)': 'o.c/1',
    'OCC (W1) + SV': 'o.s/1',
    'OCC + CU (W1) + SV': 'o.c.s/1',
    'OCC (W4)': 'o/4',
    'OCC + CU (W4)': 'o.c/4',
    'OCC (W4) + SV': 'o.s/4',
    'OCC + CU (W4) + SV': 'o.c.s/4'
}

tpcc_mvcc_sys_name_map = {
    'name': 'tpcc',
    'MVCC (W0)': 'm/0',
    'MVCC (W0) + SV': 'm.s/0',
    'MVCC + CU (W0)': 'm.c/0',
    'MVCC + CU (W0) + SV': 'm.c.s/0',
    'MVCC (W1)': 'm/1',
    'MVCC (W1) + SV': 'm.s/1',
    'MVCC + CU (W1)': 'm.c/1',
    'MVCC + CU (W1) + SV': 'm.c.s/1',
    'MVCC (W4)': 'm/4',
    'MVCC (W4) + SV': 'm.s/4',
    'MVCC + CU (W4)': 'm.c/4',
    'MVCC + CU (W4) + SV': 'm.c.s/4'
}

# MVCC TS implemented as vertical partitioning
tpcc_mvcc_slow_sys_name_map = {
    'name': 'tpcc',
    'MVCC (W0)': 'mvp/0',
    'MVCC (W0) + SV': 'mvp.s/0',
    'MVCC + CU (W0)': 'mvp.c/0',
    'MVCC + CU (W0) + SV': 'mvp.c.s/0',
    'MVCC (W1)': 'mvp/1',
    'MVCC (W1) + SV': 'mvp.s/1',
    'MVCC + CU (W1)': 'mvp.c/1',
    'MVCC + CU (W1) + SV': 'mvp.c.s/1',
    'MVCC (W4)': 'mvp/4',
    'MVCC (W4) + SV': 'mvp.s/4',
    'MVCC + CU (W4)': 'mvp.c/4',
    'MVCC + CU (W4) + SV': 'mvp.c.s/4'
}

tpcc_mvcc_cupast_sys_name_map = {
    'name': 'tpcc',
    'MVCC (W1) + SV + PAST': 'm.cp.s/1',
    'MVCC (W4) + SV + PAST': 'm.cp.s/4',
    'MVCC (W0) + SV + PAST': 'm.cp.s/0',
    'MVCC (W1) + PAST': 'm.cp/1',
    'MVCC (W4) + PAST': 'm.cp/4',
    'MVCC (W0) + PAST': 'm.cp/0'
}

tpcc_opacity_sys_name_map = {
    'name': 'tpcc',
    'OPQ (W0)': 'op/0',
    'OPQ + CU (W0)': 'op.c/0',
    'OPQ (W0) + SV': 'op.s/0',
    'OPQ + CU (W0) + SV': 'op.c.s/0',
    'OPQ (W1)': 'op/1',
    'OPQ + CU (W1)': 'op.c/1',
    'OPQ (W1) + SV': 'op.s/1',
    'OPQ + CU (W1) + SV': 'op.c.s/1',
    'OPQ (W4)': 'op/4',
    'OPQ + CU (W4)': 'op.c/4',
    'OPQ (W4) + SV': 'op.s/4',
    'OPQ + CU (W4) + SV': 'op.c.s/4'
}

tpcc_tictoc_sys_name_map = {
    'name': 'tpcc',
    'TicToc (W0)': 'tictoc/0',
    'TicToc (W1)': 'tictoc/1',
    'TicToc (W4)': 'tictoc/4',
    'TicToc + CU (W0)': 'tictoc.c/0',
    'TicToc + CU (W1)': 'tictoc.c/1',
    'TicToc + CU (W4)': 'tictoc.c/4',
    'TicToc (W0) + SV': 'tictoc.s/0',
    'TicToc (W1) + SV': 'tictoc.s/1',
    'TicToc (W4) + SV': 'tictoc.s/4',
    'TicToc + CU (W0) + SV': 'tictoc.c.s/0',
    'TicToc + CU (W1) + SV': 'tictoc.c.s/1',
    'TicToc + CU (W4) + SV': 'tictoc.c.s/4',
}

tpcc_tictoc_wrong_sys_name_map = {
    'name': 'tpcc',
    'TicToc (W0)': 'ttcc-wrong/0',
    'TicToc (W1)': 'ttcc-wrong/1',
    'TicToc (W4)': 'ttcc-wrong/4',
    'TicToc + CU (W0)': 'ttcc-wrong.c/0',
    'TicToc + CU (W1)': 'ttcc-wrong.c/1',
    'TicToc + CU (W4)': 'ttcc-wrong.c/4',
    'TicToc (W0) + SV': 'ttcc-wrong.s/0',
    'TicToc (W1) + SV': 'ttcc-wrong.s/1',
    'TicToc (W4) + SV': 'ttcc-wrong.s/4',
    'TicToc + CU (W0) + SV': 'ttcc-wrong.c.s/0',
    'TicToc + CU (W1) + SV': 'ttcc-wrong.c.s/1',
    'TicToc + CU (W4) + SV': 'ttcc-wrong.c.s/4',
}

tpcc_gc_sys_name_map = {
    'name': 'tpcc',
    'MVCC (W{} R0)': 'm.r0',
    'MVCC (W{} R1000)': 'm.r1k',
    'MVCC (W{} R100000)': 'm.r100k',
}

tpcc_safe_flatten_sys_name_map = {
    'name': 'tpcc',
    'MVCC (W0)': 'mf/0',
    'MVCC (W0) + SV': 'mf.s/0',
    'MVCC + CU (W0)': 'mf.c/0',
    'MVCC + CU (W0) + SV': 'mf.c.s/0',
    'MVCC (W1)': 'mf/1',
    'MVCC (W1) + SV': 'mf.s/1',
    'MVCC + CU (W1)': 'mf.c/1',
    'MVCC + CU (W1) + SV': 'mf.c.s/1',
    'MVCC (W4)': 'mf/4',
    'MVCC (W4) + SV': 'mf.s/4',
    'MVCC + CU (W4)': 'mf.c/4',
    'MVCC + CU (W4) + SV': 'mf.c.s/4'
}

tpcc_factors_sys_name_map = {
    'name': 'tpcc_factors',
    'MVCC (W1)-HT': 'm.h/1',
    'MVCC (W1)-AL': 'm.a/1',
    'MVCC (W1)-NOEXP': 'm.e/1',
    'MVCC (W1)-BACKOFF': 'm.r/1',
    'MVCC (W1)-AL-BACKOFF-HT': 'm.a.r.h/1'
}

tpcc_noncumu_factors_sys_name_map = {
    'name': 'tpcc_noncumu_factors',
    'MVCC (W1)-AL': 'm-a/1',
    'MVCC (W1)-NOEXC': 'm-e/1',
    'MVCC (W1)-BACKOFF': 'm-r/1',
    'MVCC (W1)-HASH': 'm-h/1',
    'MVCC (W1)BASE': 'm-base/1',
    'MVCC (W4)-AL': 'm-a/4',
    'MVCC (W4)-NOEXC': 'm-e/4',
    'MVCC (W4)-BACKOFF': 'm-r/4',
    'MVCC (W4)-HASH': 'm-h/4',
    'MVCC (W4)BASE': 'm-base/4',
    'MVCC (W0)-AL': 'm-a/0',
    'MVCC (W0)-NOEXC': 'm-e/0',
    'MVCC (W0)-BACKOFF': 'm-r/0',
    'MVCC (W0)-HASH': 'm-h/0',
    'MVCC (W0)BASE': 'm-base/0',

    'OCC (W1)-AL': 'o-a/1',
    'OCC (W1)-NOEXC': 'o-e/1',
    'OCC (W1)-BACKOFF': 'o-r/1',
    'OCC (W1)-HASH': 'o-h/1',
    'OCC (W1)BASE': 'o-base/1',
    'OCC (W4)-AL': 'o-a/4',
    'OCC (W4)-NOEXC': 'o-e/4',
    'OCC (W4)-BACKOFF': 'o-r/4',
    'OCC (W4)-HASH': 'o-h/4',
    'OCC (W4)BASE': 'o-base/4',
    'OCC (W0)-AL': 'o-a/0',
    'OCC (W0)-NOEXC': 'o-e/0',
    'OCC (W0)-BACKOFF': 'o-r/0',
    'OCC (W0)-HASH': 'o-h/0',
    'OCC (W0)BASE': 'o-base/0',

    'TicToc (W1)-AL': 't-a/1',
    'TicToc (W1)-NOEXC': 't-e/1',
    'TicToc (W1)-BACKOFF': 't-r/1',
    'TicToc (W1)-HASH': 't-h/1',
    'TicToc (W1)BASE': 't-base/1',
    'TicToc (W4)-AL': 't-a/4',
    'TicToc (W4)-NOEXC': 't-e/4',
    'TicToc (W4)-BACKOFF': 't-r/4',
    'TicToc (W4)-HASH': 't-h/4',
    'TicToc (W4)BASE': 't-base/4',
    'TicToc (W0)-AL': 't-a/0',
    'TicToc (W0)-NOEXC': 't-e/0',
    'TicToc (W0)-BACKOFF': 't-r/0',
    'TicToc (W0)-HASH': 't-h/0',
    'TicToc (W0)BASE': 't-base/0',
}

tpcc_stacked_factors_sys_name_map = {
    'name': 'tpcc_stacked_factors',
    'MVCC (W1)NAIVE': 'mn/1',
    'MVCC (W1)+AL': 'mn.a/1',
    'MVCC (W1)+AL+NOEXC': 'mn.a.e/1',
    'MVCC (W1)+AL+NOEXC+BACKOFF': 'mn.a.r.e/1',
    'MVCC (W1)BASE': 'mn.a.r.e.h/1',
    'MVCC (W4)NAIVE': 'mn/4',
    'MVCC (W4)+AL': 'mn.a/4',
    'MVCC (W4)+AL+NOEXC': 'mn.a.e/4',
    'MVCC (W4)+AL+NOEXC+BACKOFF': 'mn.a.r.e/4',
    'MVCC (W4)BASE': 'mn.a.r.e.h/4',
    'MVCC (W0)NAIVE': 'mn/0',
    'MVCC (W0)+AL': 'mn.a/0',
    'MVCC (W0)+AL+NOEXC': 'mn.a.e/0',
    'MVCC (W0)+AL+NOEXC+BACKOFF': 'mn.a.r.e/0',
    'MVCC (W0)BASE': 'mn.a.r.e.h/0',
    'OCC (W1)NAIVE': 'on/1',
    'OCC (W1)+AL': 'on.a/1',
    'OCC (W1)+AL+NOEXC': 'on.a.e/1',
    'OCC (W1)+AL+NOEXC+BACKOFF': 'on.a.r.e/1',
    'OCC (W1)BASE': 'on.a.r.e.h/1',
    'OCC (W4)NAIVE': 'on/4',
    'OCC (W4)+AL': 'on.a/4',
    'OCC (W4)+AL+NOEXC': 'on.a.e/4',
    'OCC (W4)+AL+NOEXC+BACKOFF': 'on.a.r.e/4',
    'OCC (W4)BASE': 'on.a.r.e.h/4',
    'OCC (W0)NAIVE': 'on/0',
    'OCC (W0)+AL': 'on.a/0',
    'OCC (W0)+AL+NOEXC': 'on.a.e/0',
    'OCC (W0)+AL+NOEXC+BACKOFF': 'on.a.r.e/0',
    'OCC (W0)BASE': 'on.a.r.e.h/0'
}

tpcc_index_contention_sys_name_map = {
    'name': 'tpcc_index_contention',
    'OCC (W1)-CONT-AWARE-IDX': 'on/1',
    'OCC (W4)-CONT-AWARE-IDX': 'on/4',
    'OCC (W0)-CONT-AWARE-IDX': 'on/0',
    'OCC (W1)BASE': 'o/1',
    'OCC (W4)BASE': 'o/4',
    'OCC (W0)BASE': 'o/0'
}

tpcc_history_key_sys_name_map = {
    'name': 'tpcc',
    'OCC (W1) + SEQ': 'o-s/1',
    'OCC (W1) + TS + SEQ': 'o-s.s/1',
    'OCC + CU (W1) + SEQ': 'o-s.c/1',
    'OCC + CU (W1) + TS + SEQ': 'o-s.c.s/1',
    'TicToc (W1) + SEQ': 'tictoc-s/1',
    'TicToc (W1) + TS + SEQ': 'tictoc-s.s/1',
    'TicToc + CU (W1) + SEQ': 'tictoc-s.c/1',
    'TicToc + CU (W1) + TS + SEQ': 'tictoc-s.c.s/1'
}

ycsb_all_map = {
    'name': 'ycsb',
    'OCC ({})': 'o',
    'MVCC ({})': 'm',
    'TicToc ({})': 'tictoc',

    'OCC + CU ({})': 'o.c',
    'MVCC + CU ({})': 'm.c',
    'TicToc + CU ({})': 'tictoc.c',

    'OCC ({}) + SV': 'o.s',
    'MVCC ({}) + SV': 'm.s',
    'TicToc ({}) + SV': 'tictoc.s',

    'OCC + CU ({}) + SV': 'o.c.s',
    'MVCC + CU ({}) + SV': 'm.c.s',
    'TicToc + CU ({}) + SV': 'tictoc.c.s',
}

ycsb_tictoc_comp_sys_name_map = {
    'name': 'ycsb_tictoc_comp',
    'OCC (A)': 'o/a',
    'OCC (B)': 'o/b',
    'OCC (C)': 'o/c',
    'MVCC (A)': 'm/a',
    'MVCC (B)': 'm/b',
    'MVCC (C)': 'm/c',
    'TicToc (A)': 'tictoc/a',
    'TicToc (B)': 'tictoc/b',
    'TicToc (C)': 'tictoc/c',

    'OCC + CU (A)': 'o.c/a',
    'OCC + CU (B)': 'o.c/b',
    'OCC + CU (C)': 'o.c/c',
    'MVCC + CU (A)': 'm.c/a',
    'MVCC + CU (B)': 'm.c/b',
    'MVCC + CU (C)': 'm.c/c',
    'TicToc + CU (A)': 'tictoc.c/a',
    'TicToc + CU (B)': 'tictoc.c/b',
    'TicToc + CU (C)': 'tictoc.c/c',

    'OCC (A) + SV': 'o.s/a',
    'OCC (B) + SV': 'o.s/b',
    'OCC (C) + SV': 'o.s/c',
    'MVCC (A) + SV': 'm.s/a',
    'MVCC (B) + SV': 'm.s/b',
    'MVCC (C) + SV': 'm.s/c',
    'TicToc (A) + SV': 'tictoc.s/a',
    'TicToc (B) + SV': 'tictoc.s/b',
    'TicToc (C) + SV': 'tictoc.s/c',

    'OCC + CU (A) + SV': 'o.c.s/a',
    'OCC + CU (B) + SV': 'o.c.s/b',
    'OCC + CU (C) + SV': 'o.c.s/c',
    'MVCC + CU (A) + SV': 'm.c.s/a',
    'MVCC + CU (B) + SV': 'm.c.s/b',
    'MVCC + CU (C) + SV': 'm.c.s/c',
    'TicToc + CU (A) + SV': 'tictoc.c.s/a',
    'TicToc + CU (B) + SV': 'tictoc.c.s/b',
    'TicToc + CU (C) + SV': 'tictoc.c.s/c',
}

wiki_sys_name_map = {
    'name': 'wiki',
    'OCC': 'o/1',
    'OCC + CU': 'o.c/1',
    'OCC + SV': 'o.s/1',
    'OCC + CU + SV': 'o.c.s/1',
    'TicToc': 'tictoc/1',
    'TicToc + CU': 'tictoc.c/1',
    'TicToc + SV': 'tictoc.s/1',
    'TicToc + CU + SV': 'tictoc.c.s/1',
    'MVCC': 'm/1',
    'MVCC + SV': 'm.s/1',
    'MVCC + CU': 'm.c/1',
    'MVCC + CU + SV': 'm.c.s/1',
}

rubis_sys_name_map = {
    'name': 'rubis',
    'OCC': 'o/1',
    'OCC + CU': 'o.c/1',
    'OCC + SV': 'o.s/1',
    'OCC + CU + SV': 'o.c.s/1',
    'TicToc': 'tictoc/1',
    'TicToc + CU': 'tictoc.c/1',
    'TicToc + SV': 'tictoc.s/1',
    'TicToc + CU + SV': 'tictoc.c.s/1',
    'MVCC': 'm/1',
    'MVCC + SV': 'm.s/1',
    'MVCC + CU': 'm.c/1',
    'MVCC + CU + SV': 'm.c.s/1',
}

tpcc_out_file = config.get_result_file(config.MVSTOConfig.NAME)
tpcc_occ_result_file = 'tpcc_occ_results.txt'
tpcc_mvcc_file = 'tpcc_mvcc_results.txt'
tpcc_mvcc_slow_file = 'tpcc_mvcc_slow_results.txt'
tpcc_opacity_file = 'tpcc_opacity_results.txt'
tpcc_tictoc_file = 'tpcc_tictoc_results.txt'
# "Wrong" means incomplete phantom protection :)
tpcc_tictoc_wrong_file = 'tpcc_tictoc_wrong_results.txt'
tpcc_mvcc_cupast_file = 'tpcc_mvcc_cu_past_results.txt'
tpcc_history_key_file = 'tpcc_history_key_results.txt'
tpcc_safe_flatten_file = 'tpcc_safe_flatten_results.txt'
ycsb_out_file = config.get_result_file(config.YCSBSemanticOptGraphConfig.NAME)
ycsb_result_file = 'ycsb_results.txt'

# YCSB baseline CC comparisons (convert using the generic convert() function)
ycsb_tictoc_comp_out_file = config.get_result_file(config.YCSBTicTocCompConfig.NAME)
ycsb_tictoc_comp_result_file = 'ycsb_tictoc_results.txt'

wiki_out_file = config.get_result_file(config.WikiSemanticOptGraphConfig.NAME)
wiki_result_file = 'wiki_results.txt'
rubis_out_file = config.get_result_file(config.RubisSemanticOptGraphConfig.NAME)
rubis_result_file = 'rubis_results.txt'
tpcc_stacked_factors_out_file = config.get_result_file(config.MVSTOTPCCStackedFactorsConfig.NAME)
tpcc_stacked_factors_result_file = 'tpcc_stacked_factors_results.txt'
tpcc_noncumu_factors_out_file = config.get_result_file(config.MVSTOTPCCNonCumuFactorsConfig.NAME)
tpcc_noncumu_factors_result_file = 'tpcc_noncumu_factors_results.txt'
old_tpcc_noncumu_factors_out_file = config.get_result_file(config.OldMVSTOTPCCNonCumuFactorsConfig.NAME)
old_tpcc_noncumu_factors_result_file = 'old_tpcc_noncumu_factors_results.txt'
tpcc_index_contention_out_file = config.get_result_file(config.MVSTOTPCCIndexContentionConfig.NAME)
tpcc_index_contention_result_file = 'tpcc_index_contention_results.txt'
tpcc_factors_out_file = config.get_result_file(config.MVSTOTPCCFactorsConfig.NAME)
tpcc_factors_result_file = 'tpcc_factors_results.txt'


def convert(infile, sys_name_map, compatible_results):
    sys_name_reverse_map = {}
    sys_short_names = []

    for k,v in sys_name_map.items():
        if k == 'name':
            continue
        sys_name_reverse_map[v] = k
        sys_short_names.append(v)

    num_trials = WILLIAM_TRIALS
    if sys_name_map['name'] == 'rubis':
        num_trials = 10

    try:
        with open(infile, 'r') as rf:
            reader = csv.DictReader(rf)
            scalabilities = {}
            for row in reader:
                d1 = row['# Threads']
                for v in sys_short_names:
                    long_name = sys_name_reverse_map[v]
                    for i in range(num_trials):
                        (d2, d3) = v.split('/')
                        runner_key = br.key(d1, d2, d3, i)
                        col_key = long_name
                        col_key += ' [T{}]'.format(i+1)
                        try:
                            if not row[col_key]:
                              continue
                            xput = float(row[col_key])
                        except KeyError:
                            #print('key {} not found.'.format(runner_key))
                            continue
                        if runner_key in compatible_results:
                            print('WARNING: Overriding result runner key {}'.format(runner_key))
                        compatible_results[runner_key] = (xput, 0.0, 0.0)
                        if d1 == '1':
                            scalabilities[(d2, d3)] = xput
            # Scalability lines
            for key, t1 in scalabilities.items():
                key64 = br.key(64, key[0] + '.scale', key[1], 0)
                for t in (0, 1, 24, 32, 64):
                    tkey = br.key(t, key[0] + '.scale', key[1], 0)
                    compatible_results[tkey] = (t1 * t, 0, 0)
    except (FileNotFoundError, IOError):
        print('Input file {} not found, not processed.'.format(infile))
        return {}
    return compatible_results


def convert_cicada(compatible_results):
    try:
        with open('c-1w-results.txt', 'r') as rf:
            reader = csv.DictReader(rf)
            for row in reader:
                d1 = row['# Threads']
                d2 = 'c'
                d3 = '1'
                for i in range(WILLIAM_TRIALS):
                    runner_key = br.key(d1,d2,d3,i)
                    xput = float(row['Cicada (W1)' + ' [T{}]'.format(i+1)]) * 1000000.0
                    compatible_results[runner_key] = (xput, 0.0, 0.0)

        with open('c-4w-results.txt', 'r') as rf:
            reader = csv.DictReader(rf)
            for row in reader:
                d1 = row['# Threads']
                d2 = 'c'
                d3 = '4'
                for i in range(WILLIAM_TRIALS):
                    runner_key = br.key(d1,d2,d3,i)
                    xput = float(row['Cicada (W4)' + ' [T{}]'.format(i+1)]) * 1000000.0
                    compatible_results[runner_key] = (xput, 0.0, 0.0)

        with open('c-0w-results.txt', 'r') as rf:
            reader = csv.DictReader(rf)
            for row in reader:
                d1 = row['# Threads']
                d2 = 'c'
                d3 = '0'
                for i in range(WILLIAM_TRIALS):
                    runner_key = br.key(d1,d2,d3,i)
                    cell_val = row['Cicada (W0)' + ' [T{}]'.format(i+1)]
                    if cell_val == "":
                        cell_val = '0.0'
                    xput = float(cell_val) * 1000000.0
                    compatible_results[runner_key] = (xput, 0.0, 0.0)
    except (FileNotFoundError, IOError):
        print('Cicada results files not found, not processed.')
        return {}
    return compatible_results

def convert_ermia(compatible_results):
    try:
        with open('e-1w-results.txt', 'r') as rf:
            reader = csv.DictReader(rf)
            for row in reader:
                d1 = row['# Threads']
                d2 = 'e'
                d3 = '1'
                for i in range(WILLIAM_TRIALS):
                    runner_key = br.key(d1,d2,d3,i)
                    cell_val = row['ERMIA (W1)' + ' [T{}]'.format(i+1)]
                    if cell_val == "":
                        cell_val = '0.0'
                    xput = float(cell_val)
                    compatible_results[runner_key] = (xput, 0.0, 0.0)

        with open('e-4w-results.txt', 'r') as rf:
            reader = csv.DictReader(rf)
            for row in reader:
                d1 = row['# Threads']
                d2 = 'e'
                d3 = '4'
                for i in range(WILLIAM_TRIALS):
                    runner_key = br.key(d1,d2,d3,i)
                    cell_val = row['ERMIA (W4)' + ' [T{}]'.format(i+1)]
                    if cell_val == "":
                        cell_val = '0.0'
                    xput = float(cell_val)
                    compatible_results[runner_key] = (xput, 0.0, 0.0)

        with open('e-0w-results.txt', 'r') as rf:
            reader = csv.DictReader(rf)
            for row in reader:
                d1 = row['# Threads']
                d2 = 'e'
                d3 = '0'
                for i in range(WILLIAM_TRIALS):
                    runner_key = br.key(d1,d2,d3,i)
                    cell_val = row['ERMIA (W0)' + ' [T{}]'.format(i+1)]
                    if cell_val == "":
                        cell_val = '0.0'
                    xput = float(cell_val)
                    compatible_results[runner_key] = (xput, 0.0, 0.0)
    except (FileNotFoundError, IOError):
        print('ERMIA results files not found, not processed.')
        return {}
    return compatible_results

def convert_mocc(compatible_results):
    try:
        with open('mocc_results.txt', 'r') as rf:
            reader = csv.DictReader(rf)
            for row in reader:
                d1 = row['# Threads']
                d2 = 'mocc'
                for d3 in ['1', '4', '0']:
                    for i in range(WILLIAM_TRIALS):
                        runner_key = br.key(d1,d2,d3,i)
                        cell_val = row['MOCC (W{}) [T{}]'.format(d3, i+1)]
                        if cell_val == "":
                            cell_val = '0.0'
                        xput = float(cell_val) * 1000000.0
                        compatible_results[runner_key] = (xput, 0.0, 0.0)
    except (FileNotFoundError, IOError):
        print('MOCC results files not found, not processed.')
        return {}
    return compatible_results

def convert_ycsb_all(sys_name_map, compatible_results):
    sys_name_reverse_map = {}
    sys_short_names = []

    for k,v in sys_name_map.items():
        if k == 'name':
            continue
        sys_name_reverse_map[v] = k
        sys_short_names.append(v)

    ycsb_types = ('a', 'b', 'c', 'x', 'y', 'z')
    for yt in ycsb_types:
        try:
            filename = 'ycsb_{}_results.txt'.format(yt)
            with open(filename, 'r') as rf:
                reader = csv.DictReader(rf)
                scalabilities = {}
                for row in reader:
                    d1 = row['# Threads']
                    # Skip 1-thread 
                    if yt in ('x', 'y', 'z') and d1 == '1':
                      continue
                    d3 = yt
                    for v in sys_short_names:
                        d2 = v
                        long_name = sys_name_reverse_map[v]
                        for i in range(WILLIAM_TRIALS):
                            runner_key = br.key(d1, d2, d3, i)
                            col_key = long_name
                            col_key = col_key.format(d3.upper(), d3)
                            col_key += ' [T{}]'.format(i+1)
                            if col_key in row:
                                xput = float(row[col_key])
                                compatible_results[runner_key] = (xput, 0.0, 0.0)
                            elif d3 == yt:
                                #print('Missing from {}: {}'.format(yt, col_key))
                                pass
                            if d1 == '1':
                                scalabilities[(d2, d3)] = xput
                # Scalability lines
                for key, t1 in scalabilities.items():
                    key64 = br.key(64, key[0] + '.scale', key[1], 0)
                    for t in (0, 1, 24, 32, 64):
                        tkey = br.key(t, key[0] + '.scale', key[1], 0)
                        compatible_results[tkey] = (t1 * t, 0, 0)
        except (FileNotFoundError, IOError):
            print('File {} not found, not processed.'.format(filename))
    return compatible_results


def convert_tpcc_gc_all(sys_name_map, compatible_results):
    sys_name_reverse_map = {}
    sys_short_names = []

    for k,v in sys_name_map.items():
        if k == 'name':
            continue
        sys_name_reverse_map[v] = k
        sys_short_names.append(v)

    num_whs = ('1', '0')
    for wh in num_whs:
        try:
            filename = 'tpcc_gc_results.txt'
            with open(filename, 'r') as rf:
                reader = csv.DictReader(rf)
                for row in reader:
                    d1 = row['# Threads']
                    d3 = wh
                    for v in sys_short_names:
                        d2 = v
                        long_name = sys_name_reverse_map[v]
                        for i in range(WILLIAM_TRIALS):
                            runner_key = br.key(d1, d2, d3, i)
                            col_key = long_name
                            col_key = col_key.format(d3)
                            col_key += ' [T{}]'.format(i+1)
                            xput = float(row[col_key])
                            compatible_results[runner_key] = (xput, 0.0, 0.0)
        except (FileNotFoundError, IOError):
            print('File {} not found, not processed.'.format(filename))
    return compatible_results

if __name__ == '__main__':
    results = {}
    results = convert(tpcc_occ_result_file, tpcc_occ_sys_name_map, results)
    results = convert(tpcc_mvcc_file, tpcc_mvcc_sys_name_map, results)
    results = convert(tpcc_mvcc_slow_file, tpcc_mvcc_slow_sys_name_map, results)
    results = convert(tpcc_opacity_file, tpcc_opacity_sys_name_map, results)
    results = convert(tpcc_tictoc_file, tpcc_tictoc_sys_name_map, results)
    results = convert(tpcc_tictoc_wrong_file, tpcc_tictoc_wrong_sys_name_map, results)
    results = convert(tpcc_mvcc_cupast_file, tpcc_mvcc_cupast_sys_name_map, results)
    results = convert(tpcc_history_key_file, tpcc_history_key_sys_name_map, results)
    results = convert_tpcc_gc_all(tpcc_gc_sys_name_map, results)
    results = convert(tpcc_safe_flatten_file, tpcc_safe_flatten_sys_name_map, results)
    results = convert_cicada(results)
    results = convert_ermia(results)
    results = convert_mocc(results)
    if results:
        with open(tpcc_out_file, 'w') as wf:
            json.dump(results, wf, indent=4, sort_keys=True)
    results = {}
    results = convert(ycsb_tictoc_comp_result_file, ycsb_tictoc_comp_sys_name_map, results)
    if results:
        with open(ycsb_tictoc_comp_out_file, 'w') as wf:
            json.dump(results, wf, indent=4, sort_keys=True)
    results = {}
    results = convert_ycsb_all(ycsb_all_map, results)
    if results:
        with open(ycsb_out_file, 'w') as wf:
            json.dump(results, wf, indent=4, sort_keys=True)
    results = {}
    results = convert(wiki_result_file, wiki_sys_name_map, results)
    if results:
        with open(wiki_out_file, 'w') as wf:
            json.dump(results, wf, indent=4, sort_keys=True)
    results = {}
    results = convert(rubis_result_file, rubis_sys_name_map, results)
    if results:
        with open(rubis_out_file, 'w') as wf:
            json.dump(results, wf, indent=4, sort_keys=True)
    results = {}
    results = convert(tpcc_occ_result_file, tpcc_occ_sys_name_map, results)
    results = convert(tpcc_factors_result_file, tpcc_factors_sys_name_map, results)
    results = convert_cicada(results)
    if results:
        with open(tpcc_factors_out_file, 'w') as wf:
            json.dump(results, wf, indent=4, sort_keys=True)

    results = {}
    results = convert(tpcc_stacked_factors_result_file, tpcc_stacked_factors_sys_name_map, results)
    if results:
        with open(tpcc_stacked_factors_out_file, 'w') as wf:
            json.dump(results, wf, indent=4, sort_keys=True)
    results = {}
    results = convert(tpcc_noncumu_factors_result_file, tpcc_noncumu_factors_sys_name_map, results)
    if results:
        with open(tpcc_noncumu_factors_out_file, 'w') as wf:
            json.dump(results, wf, indent=4, sort_keys=True)
    results = {}
    results = convert(old_tpcc_noncumu_factors_result_file, tpcc_noncumu_factors_sys_name_map, results)
    if results:
        with open(old_tpcc_noncumu_factors_out_file, 'w') as wf:
            json.dump(results, wf, indent=4, sort_keys=True)
    results = {}
    results = convert(tpcc_index_contention_result_file, tpcc_index_contention_sys_name_map, results)
    if results:
        with open(tpcc_index_contention_out_file, 'w') as wf:
            json.dump(results, wf, indent=4, sort_keys=True)
