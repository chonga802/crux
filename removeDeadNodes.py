#!/usr/bin/env python
#remove dead nodes from nodes.txt, save them in aliveNodes.txt
#e.g. removeDeadNodes.py -nodes nodes.txt

import sys
import argparse
import subprocess
import socket

#read file 
parser = argparse.ArgumentParser()
parser.add_argument('-nodes')
args = parser.parse_args()
nodeFile = args.nodes
#put nodes into array
nodes = []
f = open(nodeFile, 'r')
for line in f:
    nodes.append(line.rstrip('\n'))
f.close()
#ping each node, if no response after 5 seconds, don't add node to aliveNodees
aliveNodes = []
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
for node in nodes:
    try:
        s.connect((node, 22))
        aliveNode.append(node)
    except socket.error:
    	continue

#save bunch in aliveNodes.txt
fout = open("aliveNodes.txt", 'w')
for node in aliveNodes:
    fout.write(node +  "\n")
fout.close()


