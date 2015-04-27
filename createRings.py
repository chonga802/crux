#!/usr/bin/env python
#create list of items within rings
#e.g. python rings.py -nodes nodes.txt -min 2 -max 20

import sys
from optparse import OptionParser
from decimal import Decimal
import os
import subprocess

#read flags
parser = OptionParser()
parser.add_option('--min')
parser.add_option('--max')
parser.add_option('--nodes')
(options, args) = parser.parse_args()

minRing = int(options.min)
maxRing = int(options.max)
nodef = options.nodes

# collect node names
n = open(nodef,'r')
nodes=[]
for l in n:
    nodes.append(l.rstrip('\n'))
n.close()

# clean local directory
subprocess.call(['rm', '-r', 'rings'])
subprocess.call(['mkdir', 'rings'])

# iterate through nodes
for node in nodes:
    ringD = minRing
    clusterNum = 0
    # collect cluster data for node
    with open('clusters/'+node+'_cluster.txt','r') as clusterf:
        ringMembers = clusterf.readlines()
        node_ping_list = []
        for line in ringMembers:
            pair = line.split()
            node_ping_list.append(pair)

    # if there is any data
    if node_ping_list:
        i = 0
        rnum = 0

        # construct ring file
        with open('rings/'+node+'_ring.txt','w') as ringFile:
            while True:
                ringNodes=[]
                # break out if at end of list or no data
                if i == len(node_ping_list) or not(node_ping_list[i]):
                    break
                # when current node is inside ring, add nodes to current ring
                if float(node_ping_list[i][1]) < ringD:
                    # add all nodes in smaller rings
                    for x in range(0,i):
                        ringNodes.append(node_ping_list[x][0])
                    # add all nodes local to ring
                    while i<len(node_ping_list) and float(node_ping_list[i][1]) < ringD:
                        ringNodes.append(node_ping_list[i][0])
                        i = i + 1
                    # write members of ring to file and update local vars
                    ringInfo = str(rnum)+'\n'+'\n'.join(ringNodes)+'\n'
                    ringFile.write(ringInfo)
                    ringD = ringD * 2
                    rnum = rnum + 1
                # if ring is empty, move to next ring
                elif ringD < maxRing:
                    ringD = ringD * 2
                    rnum = rnum + 1
                # Error state, implies there are nodes outside largest ring
                else:
                    print 'Stuck: '+str(node_ping_list[i][1])+' '+str(ringD)

