#!/usr/bin/env python
#create list of items within rings
#e.g. python rings.py --c cluster.txt --min 2 --max 20

import sys
from optparse import OptionParser
from decimal import Decimal
import os

#read flags
parser = OptionParser()
parser.add_option('--min')
parser.add_option('--max')
(options, args) = parser.parse_args()


minRing = options.min
maxRing = options.max
#go through every cluster list
path = 'clusters/' 
dirs = os.listdir(path)
for cluster in dirs:
    clusterList = open(cluster, 'r')
    ringList = open('rings_' + cluster +'.txt','w')
    lines = ringList.readlines()
    cRing = minRing
    cCluster = 0
    line = lines[cCluster]
    cluster = line.split(' ')[0]
    ping = line.split(' ')[1]
    while True:
        if ping < cRing:
            #print ring number
            ringList.write(cRing + '\n')
            #find max cCluster that fits within ring
            while ping < cRing:
                cCluster += 1
                line = lines[cCluster]
                cluster = line.split(' ')[0]
                ping = line.split(' ')[1]
            #print all clusters within ring
            x = 1
            while x < cCluster:
                ringList.write(lines[x].split(' ')[0] + '\n')
                x += 1
        if cRing > maxRing:
            break
        cRing = cRing * 2
    ringList.close()
