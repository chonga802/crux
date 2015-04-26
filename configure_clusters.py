#!/usr/bin/env python
# create clusters for each node
# python configure_clusters.py -nodes <node_file>

#requires that bunch files are sorted

import sys
import argparse
from decimal import Decimal
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('-nodes')
args = parser.parse_args()
nodes = args.nodes

#read in nodes
n = open(nodes,'r')
nodes=[]
for l in n:
    nodes.append(l.rstrip('\n'))
n.close()

subprocess.call(["rm", "-r", "clusters"])
subprocess.call(["mkdir", "clusters"])

# for each node
for node in nodes:
    print "configuring cluster for " + node
    ncluster = node + "_cluster.txt"
    cluster = []
    # for each bunchfile
    for target in nodes:
        if node != target:
            print " target is " + target
            bunchf = "bunches/" + target + "_bunch.txt"
            with open(bunchf, 'r') as f:
                for line in f:
            # if the file contains a line with our node,
            # copy it into our cluster list
                    if node in line:
                        words = line.split()
                        cluster.append((target,words[1]))
    # sort based on ping time
    print cluster
    cluster.sort(key=lambda data: Decimal(data[1]))
    with open("clusters/" + ncluster, 'w') as f:
    # save and close
        strout ='\n'.join('%s %s' % x for x in cluster)+'\n' 
        f.write(strout)
