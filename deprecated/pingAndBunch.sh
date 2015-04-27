#!/bin/bash
# deprecated, use python script instead
filename="$1"
while read -r line
do
    name="yale_dissent@${line}"
    echo $name
    ssh -o StrictHostKeyChecking=no $name "cd plStuff; sh pingNodePairs.sh pairs.txt; python bunch.py --ping pings.txt --rank rank.txt"
    #create list of ping times of all pairs and save in pings.txt
	#takes landmark (rank) data and ping data and constructs a bunch file for current node
done < "$filename"

