#!/usr/bin/env python
#download files onto planetlab node using scp
#e.g. python filesToPlanetLab.py -item <path-name> -nodes nodes.txt

import sys
import argparse
import subprocess
import os

#read file 
parser = argparse.ArgumentParser()
parser.add_argument('-nodes')
parser.add_argument('-item')
args = parser.parse_args()
nodeFile = args.nodes
item = args.item
nodes = []
f = open(nodeFile, 'r')
for line in f:
    nodes.append(line.rstrip('\n'))
f.close()

#call ssh
for node in nodes:
    p = subprocess.Popen(["scp","-r", item, "yale_dissent@" + node + ":/home/yale_dissent"])
    sts = os.waitpid(p.pid, 0)
