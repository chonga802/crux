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

#parallely ssh into all nodes and run two commands
for node in nodes:
    print "testing " + node + "\n"
    #ssh into node
    ssh = subprocess.Popen(["ssh", "yale_dissent@" + node, "uname -a"], 
    	shell=False, 
    	stdout=subprocess.PIPE, 
    	stderr=subprocess.PIPE)
    result = ssh.stdout.readlines()
    if result == []:
    	error = ssh.stderr.readlines()
    	print >>sys.stderr, "ERROR: %s" % error
    else: 
    	print result
    #create list of ping times of all pairs and save in pings.txt
    subprocess.call(["./pingNodePairs.sh", "pairs.txt"])
	#takes landmark (rank) data and ping data and constructs a bunch file for current node
	subprocess.call(["python", "bunch.py", "--ping",  "pings.txt",  "--rank", "rank.txt"]