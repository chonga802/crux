#!/usr/bin/env python
# given a node list, ping and rank information,
# constructs bunches for each node given ping and rank info
# usage: python createBunches.py -nodes <nodes> -dest <dest path>

import sys
import argparse
import subprocess
import os
from decimal import Decimal

#read file 
parser = argparse.ArgumentParser()
parser.add_argument('-nodes')
parser.add_argument('-dest')
args = parser.parse_args()
nodeFile = args.nodes
dest = args.dest

# make list of nodes
nodes = []
f = open(nodeFile, 'r')
for line in f:
    nodes.append(line.rstrip('\n'))
f.close()

uname = 'yale_dissent'
for node in nodes:
    bcfg = 'bunch_cfgs/'+node+'_bunch_cfg.txt'
    rcfg = 'ring_cfgs/'+node+'_ring_ports.txt'
    target = uname+'@'+node+':'+dest
    subprocess.call(['scp','-r', bcfg, target])
    subprocess.call(['scp','-r', rcfg, target])
