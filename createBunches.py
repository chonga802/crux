#!/usr/bin/env python
# given a node list, ping and rank information,
# constructs bunches for each node given ping and rank info
# usage: python createBunches.py -nodes <nodes> -ping <pings> -rank <ranks>

import sys
import argparse
import subprocess
import os
from decimal import Decimal

#read file 
parser = argparse.ArgumentParser()
parser.add_argument('-nodes')
parser.add_argument('-ping')
parser.add_argument('-rank')
args = parser.parse_args()
nodeFile = args.nodes
pingFile = args.ping
rankFile = args.rank


# make list of nodes
nodes = []
f = open(nodeFile, 'r')
for line in f:
    nodes.append(line.rstrip('\n'))
f.close()

# make dictionary of ranks (<node,rank>)
rank = dict()
r = open(rankFile, 'r')
for line in r:
    line = line.rstrip('\n')
    words = line.split('=')
    rank[words[0]] = words[1]
r.close()

# construct bunches from ping file
for node in nodes:
    npings = []
    # read in pings associated with node
    p = open(pingFile,'r')
    for line in p:
        line = line.rstrip('\n')
        x = line.split(' ')
        if len(x)==3 and x[0]==node:
            npings.append(x[1]+' '+x[2])
    p.close()
    # sort the pings
    npings.sort(key=lambda x: Decimal(x.split(' ')[1]))
    print npings
    # create bunch
    bunch = []
    myRank = rank[node]
    maxRank = myRank
    for hostping in npings:
        host = hostping.split(' ')[0]
        ping = hostping.split(' ')[1]
        r = rank[host]
        if r > maxRank:
            bunch.append((host,ping))
            maxRank = r
    with open('bunches/'+node+'_bunch.txt','w') as fout:
        for (x,y) in bunch:
            fout.write(x+' '+y+'\n')
        fout.close()
