#!/bin/bash

Count=3     # How many ping packets?
Interval=3  # How many seconds between pings?
Column=1    # Get the minimum or the averag? Min is 1, Avg is 2

TempFile=temp.txt
PingFile=pings.txt

if [ $# -ne 1 ]; then
  echo "usage: $0 <all-host-pairs file>"
  exit 1
fi

# Get the pings that I'm responsible for.
Me=$(hostname)
grep "^${Me}" $1 | cut -d ' ' -f 2 > $TempFile

# Do the pings and output the results.
while read dest; do

  PingResult=$(ping -q -c $Count -i $Interval $dest | tail -n 1)
  Vals=$(echo $PingResult | cut -d ' ' -f 4 | cut -d '/' -f 1-2 | tr '/' ' ')
  echo  "$Me $dest $Vals" >> $PingFile

done < $TempFile

rm $TempFile




