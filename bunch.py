#!/usr/bin/env python
#create bunch list
#e.g. python bunch.py -ping ping.txt -rank rank.txt

import sys
import argparse

#read flags
parser = argparse.ArgumentParser()
parser.add_argument('-ping')
parser.add_argument('-rank')
args = parser.parse_args()
pingList = args.ping
rankList = args.rank
#sort ping list
sortedPings = []
with open(pingList, 'r') as p:
    for line in p:
        sortedPings.append(line.rstrip('\n'))
sortedPings.sort(key=lambda x: x.split('=')[1])
print "sortedPings = "
print sortedPings
#make dictionary of ranks (<node,rank>)
rank = dict()
with open(rankList, 'r') as r:
    for line in r:
        line = line.rstrip('\n')
        words = line.split('=')
        rank[words[0]] = words[1]
print "rank="
print rank

bunch = []
maxLandmark = 0
for line in sortedPings:
    node = line.split('=')[0]
    r = rank[node]
    if r >= maxLandmark:
        bunch.append(node)
        maxLandmark = r
print "bunch="
print bunch
#save bunch in bunch.txt 
with open("bunch.txt", 'w') as fout:
    for b in bunch:
        fout.write(b + "\n")