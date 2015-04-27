#!/usr/bin/env python
#download files onto planetlab node using scp
#e.g. python recoverPings.py -nodes nodes.txt

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

# dictionary with ping times for all pairs of nodes,
# structured as dictionary of dictionaries where value
# is dictionary of pingtimes for that node
pingdict = dict()

# populate dictionary
for node in nodes:
    ndict = dict()
    pingdict[node] = ndict

# collect ping data
for node in nodes:
    print "gathering pings for: " + node
    # copy pings to local
    p = subprocess.Popen(["scp", "yale_dissent@" + node + ":/home/yale_dissent/plStuff/pings.txt", "."])
    # kill process if we freeze
    p.wait()
    #time.sleep(3.0)
    #p.kill()
    # move files and rename
    fname = "pl_pings/" + node + "_pings.txt"
    subprocess.call(["touch", fname])
    f = open(fname, "w")
    # remove first and last column of pings, which are hostname and avg ping time
    subprocess.call(["cut", "-d", ' ', "-f", "2-3", "pings.txt"], stdout=f)
    f.close()

# all pings will be moved into this new file of all ping pairs
pingfile = open('pl_pings/pings.txt','w')

# fill out new master ping file
for node in nodes:
    nping = 'pl_pings/'+node+ '_pings.txt'
    print 'moving pings over from '+nping
    subprocess.call(['cat', nping])
    r = open(nping, 'r')
    # read in pings and add them to ping file
    for line in r:
        line = line.rstrip('\n')
        words = line.split(' ')
        # add both [a,b,ping] and [b,a,ping] for ease of use
        ab = node + ' ' + words[0] + ' ' + words[1] + '\n'
        ba = words[0] + ' ' + node + ' ' + words[1] +'\n'
        print '  adding ' + ab
        print '  adding ' + ba
        if node != words[0] and not(str.isspace(words[1])) and words[1] != '':
            pingfile.write(ab)
            pingfile.write(ba)
    r.close()
    # remove old ping files
    subprocess.call(['rm', nping])

pingfile.close()
