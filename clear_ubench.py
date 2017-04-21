#!/usr/bin/env python

import json

sys_affected = ['tictoc', 'tictoc-o']
wl_affected = ['high-small']
thr_affected = ['24']

with open('./results/json/ubench_results.json', 'r') as rf:
    results = json.load(rf)

delkeys = []
for k in results:
    kl = k.split('/')
    if (kl[0] in sys_affected) and (kl[1] in wl_affected) and (kl[2] in thr_affected):
        print 'delete key: {}'.format(k)
        delkeys.append(k)

for k in delkeys:
    del results[k]

print '{} keys deleted'.format(len(delkeys))

with open('./results/json/ubench_results.del.json', 'w') as of:
    json.dump(results, of, indent=4, sort_keys=True)
