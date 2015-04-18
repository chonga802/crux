#!/usr/bin/python

import sys
import fabdeploy
import fabric

def test(argv):

    username = "yale_dissent"
    pw = "/home/accts/km637/.ssh/id_rsa.pub"

    fabdeploy.setup_env("slice_nodes.txt",username, pw)
    fab fabdeploy.copy_single(username, pw, "test.txt", "/home/yale_dissent")

    return

if __name__ == "__main__":
    test(sys.argv[1:])
