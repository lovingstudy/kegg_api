#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 20:25:04 2020

@author: jingxing
"""

import urllib3

ECNUM = '1.6.99.1'

http = urllib3.PoolManager()
r = http.request('GET', 'http://rest.kegg.jp/get/ec:%s/'%ECNUM)
lines_tmp = r.data.decode().split('\n')
lines = []
swc = False
for line in lines_tmp:
    if line.startswith('GENES'): swc = True
    if not swc: continue
    if swc and (not line.startswith(' ')) and (not line.startswith('GENES')): break
    lines.append(line[12:].strip())
    

org_ids = []
for line in lines:
    tmp = line.split(' ')
    org = tmp[0].replace(':', '').lower()
    ids = [i.split('(')[0] for i in tmp[1:]]
    org_ids += [(org, i) for i in ids]
print('%s gene AA seq to collect...'%len(org_ids))


fout = open('EC_%s.fastq'%ECNUM, 'w')
for num, (org, i) in enumerate(org_ids):
    if num % 500 == 0: print('{:.2%}'.format(num / len(org_ids)) + ' done.')
    try:
        r = http.request('GET', 'http://rest.kegg.jp/get/%s:%s/aaseq'%(org, i))
        seq = r.data.decode()
        fout.write(seq + '\n')
    except Exception as e:
        continue

fout.close()