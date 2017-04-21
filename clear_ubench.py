#!/usr/bin/env python

import json

affected = ['low-small', 'low-large', 'high-small', 'high-large']

with open('./results/json/ubench_results.json', 'r') as rf:
    results = json.load(rf)

delkeys = []
for k in results:
    kl = k.split('/')
    if kl[2] == '12' and kl[1] in affected:
        delkeys.append(k)

for k in delkeys:
    del results[k]

print '{} keys deleted'.format(len(delkeys))

with open('./results/json/ubench_results.del.json', 'w') as of:
    json.dump(results, of, indent=4, sort_keys=True)
