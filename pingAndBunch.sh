#!/bin/bash
filename="$1"
while read -r line
do
    name=$line
    echo name
    ssh -o StrictHostKeyChecking=no "yale_dissent@${name}"
    cd plStuff
    #create list of ping times of all pairs and save in pings.txt
    sh pingNodePairs.sh pairs.txt
	#takes landmark (rank) data and ping data and constructs a bunch file for current node
	python bunch.py --ping pings.txt --rank rank.txt
done < "$filename"

