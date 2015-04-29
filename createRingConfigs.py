#!/usr/bin/env python
# given a node list, ping and rank information,
# constructs bunches for each node given ping and rank info
# usage: python createRingConfigs.py -nodes <nodes>

import sys
import argparse
import subprocess
import os

#read file 
parser = argparse.ArgumentParser()
parser.add_argument('-nodes')
args = parser.parse_args()
nodeFile = args.nodes

# make list of nodes
nodes = []
f = open(nodeFile, 'r')
for line in f:
    nodes.append(line.rstrip('\n'))
f.close()

# clean local directory
subprocess.call(['rm', '-r', 'ring_cfgs'])
subprocess.call(['mkdir', 'ring_cfgs'])

# Create config for each node
for node in nodes:
    # Read in ring data
    ringList = []
    with open('rings/'+node+'_ring.txt', 'r') as ringf:
        rings = ringf.readlines()
        for ring in rings:
            data = ring.split()
            ringList.append(data)
    for ring in ringList:
        p = ring[0]
        with open('ring_cfgs/'+node+'_ring_ports.txt','a') as portf:
            q = int(p)+1
            portf.write(p+' '+str(q)+'\n')




# port format:
# <cfg port 1> <mongos port 1>
# <cfg port 2> <mongos port 2>
# ...
# ...
#
#
# bunch format:
# <hostname1> <mongos port1> <local mongod port1>
# <hostname2> <mongos port2> <local mongod port2>
# ...
# ...
#
#
#
