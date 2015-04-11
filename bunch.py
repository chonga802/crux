#!/usr/bin/env python
#create bunch list
#e.g. python bunch.py -ping pings.txt -rank rank.txt

import sys
# import argparse
from optparse import OptionParser
from decimal import Decimal

#read flags
# parser = argparse.ArgumentParser()
# parser.add_argument('-ping')
# parser.add_argument('-rank')
# args = parser.parse_args()
# pingList = args.ping
# rankList = args.rank
parser = OptionParser()
parser.add_option('--ping')
parser.add_option('--rank')
(option, args) = parser.parse_args()
pingList = option.ping
rankList = option.rank
#sort ping list
sortedPings = []
p = open(pingList, 'r')
for line in p:
    x = line.split(' ')
    #skip dead nodes
    if len(x)==4:
	sortedPings.append(x[1] + "=" + x[2])
p.close()
sortedPings.sort(key=lambda x: Decimal(x.split('=')[1]))
#make dictionary of ranks (<node,rank>)
rank = dict()
r = open(rankList, 'r')
for line in r:
    line = line.rstrip('\n')
    words = line.split('=')
    rank[words[0]] = words[1]
r.close()

bunch = []
maxLandmark = 0
for item in sortedPings:
    node = item.split('=')[0]
    pingTime = item.split('=')[1]
    r = rank[node]
    if r >= maxLandmark:
        bunch.append((node, pingTime))
        maxLandmark = r
#save bunch in bunch.txt 
fout = open("bunch.txt", 'w')
for b in bunch:
    fout.write(b[0] + " " + b[1] +  "\n")
fout.close()
