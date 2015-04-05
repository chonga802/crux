#!/usr/bin/env python
#assign landmark nodes
#e.g. python landmark.py -file nodes.txt -b 3 

import sys
import random
import argparse

#read flags
parser = argparse.ArgumentParser()
parser.add_argument('-b', type=int)
parser.add_argument('-file')
args = parser.parse_args()
b = args.b
if b==1:
    print "b must be greater than 1"
    sys.exit()
fileName = args.file
#read from file to make array of nodes
nodes = []
with open(fileName, 'r') as f:
    for line in f:
        nodes.append(line.rstrip('\n'))
#assign level 0 to all nodes initially in rank
rank = dict()
for node in nodes:
    rank[node] = 0
#assign levels by flipping weighted coin
high = 0
run = True
while run:
    #print "high =%d" % (high)
    run = False
    for node in nodes:
        #flip coin according so 1/b prob of true
        flip = random.randrange(1,b+1)
        val = rank.get(node)
        #print "val=%d,high=%d,flip=%d, b=%d" % (val,high,flip,b)
        if val==high and flip==b:
            #upgrade node
            rank[node] = val+1
            run = True
    high += 1

#save values in landmark.txt ("node=rank")
fname = 'rank.txt'
with open(fname, 'w') as fout:
    for node in nodes:
        level = rank[node]
        fout.write("%s=%d\n" % (node,level))

