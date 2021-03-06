#!/usr/bin/env python
#complete setup
#python setup.py

import sys
import subprocess

#gets list of planet lab nodes -> creates nodes.txt
subprocess.call(["python", "get_slice_nodes.py", "nodes.txt", "christine.hong@yale.edu"])

#remove dead nodes -> creates aliveNodes.txt
subprocess.call(["python", "removeDeadNodes.py",  "-nodes", "nodes.txt"])

#assigns landmark value to each node in nodes.txt -> creates rank.txt
subprocess.call(["python", "landmark.py", "-file", "nodes.txt", "-b", "3"]) 

#constructs all pairs of nodes -> creates pairs.txt
subprocess.call(["python", "makeHostPairList.py", "nodes.txt"])

#puts all the files onto the planet lab nodes (or just do it from folder)
subprocess.call(["python", "filesToPlanetLab.py", "-item", "plStuff", "-nodes", "nodes.txt"])

#sshes into all nodes and runs command to create pings.txt and create bunch.txt
subprocess.call(["sh", "pingAndBunch.sh", "nodes.txt"])

#return to local computer and recover bunches -> all bunches saved locally to pl_pings folder
subprocess.call(["python", "recover_bunches.py", "-nodes", "nodes.txt"])

#looks at bunches in pl_pings to create clusters-> all clusters saved locally to clusters folder
subprocess.call(["python", "configure_clusters.py", "-nodes", "nodes.txt"])

#create ring list for every cluster -> all rings saved locally into a ring folder
subprocess.call(["python", "rings.py", "--min", "2", "--max", "20"])
