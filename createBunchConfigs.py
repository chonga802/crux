#!/usr/bin/env python
# given a node list, ping and rank information,
# constructs bunches for each node given ping and rank info
# usage: python createBunchConfigs.py -nodes <nodes>

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

# clean old files
subprocess.call(['rm', '-r', 'bunch_cfgs'])
subprocess.call(['mkdir', 'bunch_cfgs'])

# create bunch config for each node
for node in nodes:
    rings = os.listdir('ring_cfgs')
    rings2join = []
    nodecfg = 'bunch_cfgs/'+node+'_bunch_cfg.txt'
    for center in nodes:
        for ring in rings:
            if center in ring:
                with open('rings/'+center+'_ring.txt') as ringf:
                    for line in ringf.readlines():
                        if node in line:
                            with open(nodecfg,'a') as nodeConfig:
                                p = line.split()[0]
                                q = int(p)+1
                                nodeConfig.write(center+' '+p+' '+str(q)+'\n')
