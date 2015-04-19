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

subprocess.call(["rm", "-r", "clusters"])
subprocess.call(["mkdir", "clusters"])

# for each node
for node in nodes:
    ncluster = node + "_cluster.txt"
    cluster = []
    # for each bunchfile
    for target in nodes:
        nodef = "pl_pings/" + target + "_file.txt"
        f = open(nodef, 'r')
        for line in f.splitlines():
            # if the file contains a line with our node,
            # copy it into our cluster list
            if node in line:
                cluster.append(line)
    # sort based on ping time
    cluster.sort(key=lambda data: Decimal(data[1]))
    f = open("clusters/" + ncluster, 'w')
    # save and close
    f.write(cluster)
    f.close()
