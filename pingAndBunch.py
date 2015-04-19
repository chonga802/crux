#!/usr/bin/env python
#download files onto planetlab node using scp
#e.g. python pingAndBunch.py -nodes nodes.txt

import sys
import argparse
import subprocess
import os
import shutil
import time

#read file 
parser = argparse.ArgumentParser()
parser.add_argument('-nodes')
args = parser.parse_args()
nodeFile = args.nodes
nodes = []
f = open(nodeFile, 'r')
for line in f:
    nodes.append(line.rstrip('\n'))
f.close()

#parallel ssh into all nodes and run two commands
for node in nodes:
    command = "ssh -o StrictHostKeyChecking=no yale_dissent@" + node + " \"cd plStuff; rm pings.txt;sh pingNodePairs.sh pairs.txt; rm bunch.txt; python bunch.py --ping pings.txt --rank rank.txt\";"
    p = subprocess.Popen([command], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print "added " + node
p.wait(900)
