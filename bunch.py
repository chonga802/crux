#!/usr/bin/env python
#create bunch list
#e.g. python bunch.py -ping ping.txt -rank rank.txt

import sys
# import argparse
from optparse import OptionParser

#read flags
# parser = argparse.ArgumentParser()
# parser.add_argument('-ping')
# parser.add_argument('-rank')
# args = parser.parse_args()
# pingList = args.ping
# rankList = args.rank
parser = OptionParser()
parser.add_option('-ping')
parser.add_option('-rank')
(option, args) = parser.parse_args()
pingList = options.ping
rankList = options.rank
print "ping list"
print pingList
print "rank list"
print rankList
#sort ping list
sortedPings = []
p = open(pingList, 'r')
for line in p:
    sortedPings.append(line.rstrip('\n'))
p.close()
sortedPings.sort(key=lambda x: x.split('=')[1])
print "sortedPings = "
print sortedPings
#make dictionary of ranks (<node,rank>)
rank = dict()
r = open(rankList, 'r')
for line in r:
    line = line.rstrip('\n')
    words = line.split('=')
    rank[words[0]] = words[1]
r.close()
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
fout = open("bunch.txt", 'w')
for b in bunch:
    fout.write(b + "\n")
fout.close()
