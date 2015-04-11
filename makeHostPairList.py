#! /usr/bin/env python

# This program reads a file of tokens, one per line, and outputs
# all unique pairs (i.e., ordering does not matter).

#python makeHostPairList.py nodes.txt

import random
import sys

DBG = False
RAND = False

if __name__ == "__main__":

    # Flags and arguments.
    argv = []
    for a in sys.argv:
        if a.startswith('--'):
            DBG = DBG or a == '--debug'
            RAND = RAND or a == '--rand'
        else:
            argv.append(a)
    if len(argv) < 2:
        sys.exit('usage: ' + argv[0] + ' [--debug] [--rand] <tokens file>')

    # Read the tokens.
    tokens = [token.strip() for token in open(argv[1])]

    # Enumerate the unique pairs.
    pairs = []
    for i, first in enumerate(tokens):
        for x in range(i + 1, len(tokens)):
            second = tokens[x]
            if RAND and random.randint(0, 1) == 1:
                pairs.append(second + " " + first)
            else:
                pairs.append(first + " " + second)

    # Sort and output the pairs.
    pairs.sort()
    fname = 'pairs.txt'
    fout = open(fname,'w')
    for p in pairs:
        fout.write(p + "\n")
    fout.close()


    
