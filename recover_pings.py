#!/usr/bin/env python
#download files onto planetlab node using scp
#e.g. python recover_pings.py -nodes nodes.txt

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

shutil.rmtree("pl_pings", ignore_errors=True)
subprocess.call(["mkdir", "pl_pings"])

#call ssh
for node in nodes:
    print "testing " + node + "\n"
    # copy pings to local
    p = subprocess.Popen(["scp", "yale_dissent@" + node + ":/home/yale_dissent/crux/pings.txt", "."])
    # kill process if we freeze
    time.sleep(3.0)
    p.kill()
    # move files and rename
    fname = "pl_pings/" + node + "_pings.txt"
    subprocess.call(["touch", fname])
    f = open(fname, "w")
    # remove first column of pings, which is just name of host
    subprocess.call(["cut", "-d", ' ', "-f", "2-", "pings.txt"], stdout=f)
    subprocess.call(["rm", "pings.txt"])

