#!/usr/bin/env python
# Used to remove plStuff folder from live pl nodes
#e.g. python cleanPL.py -nodes nodes.txt

import sys
import argparse
import subprocess
import os

#read file 
parser = argparse.ArgumentParser()
parser.add_argument('-nodes')
args = parser.parse_args()
nodeF = args.nodes
f = open(nodeF, 'r')
nodes = []
for line in f:
    nodes.append(line.rstrip('\n'))
f.close()

for node in nodes:
    command = "ssh -o StrictHostKeyChecking=no yale_dissent@"+node+" \"rm -r plStuff;mkdir plStuff;\""
    p = subprocess.Popen([command], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.wait()
    print "cleaned "+node
