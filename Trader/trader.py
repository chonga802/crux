## Python implementation of the Crux scheme for a transactional trading database
##

# We can run our basic Crux-ified MongoDB trading system by calling:

# python trader.py ports.txt rings.txt instructions.txt binpath

# on each participant node, where binpath is the bin directory of MongoDB. Note
# that all of the necessary config files must be formed for given node A: 

# 	ports.txt, containing a line for each ring centered on A, specifying
# 	the port which the instance of MongoDB for that ring should use;

# 	rings.txt, containing a line for each ring that A is involved in, consisting
# 	of the hostname and port (whitespace-delineated) on which that ring is
# 	running;

#	and instructions.txt, containing the actual transaction instructions for each
# 	node to carry out (more below).

# Given these specifications, the trading program will initialize N instances of
# MongoDB, where N is the number of lines/ports in ports.txt, and it will
# also create N data folders. It will then wait for input before running
# the commands in instructions.txt (to ensure synchronicity).


# INSTRUCTIONS:
# We interact with our trading algorithm through a simple API, using commands
# specified in instructions.txt.  This is obviously best suited for a test
# environment; in practical deployments it would be a simple measure to
# use real-time input instead of a set of instructions.

# The API is specified here:

 	# post [BUY/SELL] [ITEM]

# 	Posts a BUY or SELL request for item ITEM to all rings in rings.txt, using
# 	the Crux algorithm (starting with the smallest rings and expanding outward
# 	to preserve locality).

 	# find [ITEM]

# 	Searches for a request containing item ITEM using the Crux algorithm on
# 	rings in rings.txt.  To preserve locality, when the item is found in a 
# 	given ring, it is immediately returned and the search is halted.

import subprocess
import time
import os
import socket
import sys

# Given file listing local ports on which to build rings, returns in tuple list form
# Takes input describing a single ring per line, with each line holding two port numbers:
# the mongos (publically used) port number and the config server port number
# 	e.g. 27019 27020
def parse_ring_ports(fn):

	b = []
	f = open(fn)
	l = f.read().strip().splitlines()

	for elt in l:
		s = elt.split()
		b.append((s[0], s[1]))

	return b

# Given file listing bunches to search returns as list of tuples
def parse_bunch(fn):

	b = []

	f = open(fn)
	l = f.read().strip().splitlines()

	for elt in l:
		s = elt.split()
		b.append((s[0],s[1],s[2]))

	return b

# One half of the process of construction of rings A around this node
# see build_mongos for other half
# Given ring ports, makes cfg servers for Mongo databases on those ports centered on local host
def build_cfg (mpath, host, ring_ports):

	print "-"*40
	print "Building cfg on ports", ring_ports

	host_short = host.split(".")[0]

	for ports in ring_ports:

		cfgpath = mpath+'/cfg_data_at_'+host_short+"_"+ports[1]

		if not os.path.exists(cfgpath):
			os.makedirs(cfgpath)

		subprocess.Popen([mpath + '/mongod', '--configsvr', '--dbpath', cfgpath, '--port', ports[1]])#, stdout=subprocess.PIPE)
		# result = p.communicate()[0]
		# print "STARTED:" + result

	return 

# One half of the process of construction of rings A around this node
# see build_cfg for other half
# Given ring ports, makes mongos servers for Mongo databases on those ports centered on local host
# returns processes for later shutdown
def build_mongos (mpath, host, ring_ports):

	print "-"*40
	print "Building mongos on ports", ring_ports
	# processes = []

	for ports in ring_ports:

		p = subprocess.Popen([mpath + '/mongos', '--port', ports[0], '--configdb', host+":"+ports[1]])
		# processes.append(p)

	return

# Building shards of rings
# Given bunch, builds necessary shards
def build_shards (mpath, host, bunch):

	print "-"*40
	print "Building shards on ports", bunch

	host_short = host.split(".")[0]

	for ports in bunch:

		cfgpath = mpath+'/shard_data_at_'+host_short+"_"+ports[2]

		if not os.path.exists(cfgpath):
			os.makedirs(cfgpath)

		p = subprocess.Popen([mpath + '/mongod', '--dbpath', cfgpath, '--port', ports[2]])

	return

def connect_shards (mpath, host, bunch):

	print "-"*40
	print "Connecting shards on ports", bunch

	for ports in bunch:

		command = 'sh.addShard("'+host+':'+ports[2]+'")'
		p = subprocess.Popen([mpath + "/mongo", "--port", ports[1], "--host", ports[0], "--eval", command], stdout=subprocess.PIPE)

	return

def shard_collections (mpath, host, ring_ports):

	print "-"*40
	print "Sharding collections on ports", ring_ports

	for ports in ring_ports:

		command = 'sh.enableSharding("test"); sh.shardCollection("test.trades", {_id:"hashed"});'
		p = subprocess.Popen([mpath + "/mongo", "--port", ports[0], "--eval", command])

	return

# One half of the process of destruction of rings A around this node
# see kill_mongos for other half
# Given ring ports, destroys cfg servers using mongod commands
def kill_cfg (mpath, host, ring_ports):

	print "-"*40
	print "Killing cfg on ports", ring_ports

	host = host.split(".")[0]

	for ports in ring_ports:

		cfgpath = mpath+'/cfg_data_at_'+host+"_"+ports[1]
		subprocess.Popen([mpath + '/mongod', '--dbpath', cfgpath, '--shutdown'])

	return

# One half of the process of destruction of rings A around this node
# see kill_mongos for other half
# Given bunch, destroys cfg servers using mongod commands
def kill_shards (mpath, host, bunch):

	print "-"*40
	print "Killing shards on ports", bunch

	host = host.split(".")[0]

	for ports in bunch:

		cfgpath = mpath+'/shard_data_at_'+host+"_"+ports[2]
		subprocess.Popen([mpath + '/mongod', '--dbpath', cfgpath, '--shutdown'])

	return

# One half of the process of construction of rings A around this node
# see build_cfg for other half
# Given ring ports, destroys mongos servers using mongod commands
def kill_mongos (mpath, host, ring_ports):

	print "-"*40
	print "Killing mongos on ports", ring_ports

	command = "db = db.getSiblingDB('admin'); db.shutdownServer()"

	for ports in ring_ports:

		subprocess.Popen([mpath + '/mongo', '--port', ports[0], '--eval', command])
		
	return

# One half of the process of construction of rings A around this node
# see build_cfg for other half
# Given processes, destroys mongos servers using -kill
def kill_mongos2 (mpath, host, processes):

	print "-"*40
	print "Killing mongos"

	# command = "use admin; db.shutdownServer()"

	for p in processes:

		# subprocess.Popen([mpath + '/mongo', '--port', ports[0], '--eval', command])
		p.kill()

	return

# Posts a single trade entry into database specified
# t_type is "WANT"/"SELL"
# t_id is object ID
# username contains information for direct connection to poster of trade
def post_instance (mpath, host, port, t_type, t_id, username):

	command = "db.trades.insert({type:'"+t_type+"', object: '"+t_id+"', user: '"+username+"'})"

	p = subprocess.Popen([mpath + "/mongo", "--port", port, "--host", host, "--eval", command], stdout=subprocess.PIPE)
	result = p.communicate()[0]
	print "TRADE OUT:" + result

	return

# Finds trade entry based on given object id t_id
def find_instance (mpath, host, port, t_id):

	command = "var myCursor = db.trades.find({object: '"+t_id+"'}); \
myCursor.forEach(printjson);"

	start_t = time.time()

	p = subprocess.Popen([mpath + "/mongo", "--port", port, "--host", host, "--eval", command], stdout=subprocess.PIPE)
	result = p.communicate()[0]
	print "SEARCHING FOR " + t_id + ":" + result

	end_t = time.time()
	print "LOCAL TIMING OF " + host + port
	print end_t-start_t

	if "object" in result:
		return result
	else:
		return "NO MATCH"

	return

# Post given trade in all rings of bunch
def post_all (mpath, bunch, t_type, t_id, localhost) :

	print "============================================="
	print "POSTING " + t_id

	start_t = time.time()

	for b in bunch:
		post_instance(mpath, b[0], b[1], t_type, t_id, localhost)

		end_t = time.time()
		print "\n TIMING UP TO: "+b[0]+b[1]
		print end_t-start_t
		print "-------------------------------------------"

	print "DONE POSTING " + t_id
	print "============================================="

	return


# Search all rings until given trade found
def find_all (mpath, bunch, t_id):

	result = "NO MATCH"
	start_t = time.time()

	print "============================================="
	print "SEARCHING FOR " + t_id

	for b in bunch:
		result = find_instance(mpath, b[0], b[1], t_id)
		end_t = time.time()

		print "\n TIMING UP TO: "+b[0]+b[1]
		print end_t-start_t
		print "-------------------------------------------"

		# As soon as item found, stop searching rings
		if result != "NO MATCH":
			break

	if result == "NO MATCH":

		print "Could not find any matches for " + t_id

	else:

		print "FOUND MATCH! " + t_id

		for line in result.split("\n"):
			line = line.strip().split()

			if line and line[0] == '"user"':
				print "DIRECTLY CONTACTING " + line[2] + " TO ARRANGE TRANSACTION"

	print "DONE SEARCHING FOR " + t_id
	print "============================================="


	return

# Drops current databases
def drop_dbs (mpath, host, ring_ports):

	print "-"*40
	print "Dropping db"

	for ports in ring_ports:

		p = subprocess.Popen([mpath + "/mongo", "--port", ports[0], "--host", host, "--eval", "db.dropDatabase()"])

	return

# Drops given collection
def clear_collection (mpath, host, port, db_name):

	p = subprocess.Popen([mpath + "/mongo", "--port", port, "--host", host, "--eval", "db."+db_name+".drop()"], stdout=subprocess.PIPE)
	result = p.communicate()[0]
	print "CLEARED:" + result

	return

# Shows available collections
def show_collections (mpath, host, port):

	p = subprocess.Popen([mpath + "/mongo", "--port", port, "--host", host, "--eval", "db.getCollectionNames()"], stdout=subprocess.PIPE)
	result = p.communicate()[0]
	print "COLLECTIONS:" + result

	return

# Run commands from given instruction file
def run_instructions (fn, mpath, localhost, ring_ports, bunch):

	f = open(fn)

	for instr in f:
		i = instr.split()

		if i[0] == "post":

			post_all(mpath, bunch, i[1], i[2], localhost)

		elif i[0] == "find":

			find_all(mpath, bunch, i[1])


	return

####################################################

# Requires direct input to proceed through test phases.
def manual_test(argv):

	ring_ports = parse_ring_ports(argv[0])
	bunch = parse_bunch(argv[1])

	# Location of mongod program
	if argv[3] == "default" or argv[3] == "d":
		mpath = "/home/accts/km637/mongodb-linux-i686-3.0.1/bin"
	else:
		mpath = argv[3]

	# Local host name
	localhost = socket.gethostname()

	build_cfg (mpath, localhost, ring_ports)
	build_shards (mpath, localhost, bunch)

	inp = raw_input("Any key to continue: ")

	if inp != "n":
		build_mongos (mpath, localhost, ring_ports)

	
	inp = raw_input("Any key to continue: ")

	if inp != "n":
		connect_shards(mpath, localhost, bunch)


	inp = raw_input("Any key to continue: ")

	if inp != "n":

		shard_collections(mpath, localhost, ring_ports)

	inp = raw_input("Any key to continue: ")

	if inp != "n":

		# post_trade (mpath, "", ring_ports, "HAVE", "123", "Koji")
		run_instructions(argv[2], mpath, localhost, ring_ports, bunch)

		# for i in range(10):
		# 	find_trade(mpath, localhost, "27017", "123")

		# 	show_collections(mpath, "", "27017")

	inp = raw_input("Any key to continue: ")

	if inp != "n":

		drop_dbs(mpath, localhost, ring_ports)
		# clear out stuff from earlier tests
		# for p in ring_ports:
		# 	clear_collection (mpath, localhost, p, "trades")

	inp = raw_input("Any key to continue: ")

	if inp != "n":

		kill_mongos (mpath, localhost, ring_ports)

		# for m in mongos:
		# 	m.kill()

	inp = raw_input("Any key to continue: ")

	if inp != "n":

		kill_cfg (mpath, localhost, ring_ports)
		kill_shards (mpath, localhost, bunch)


# Allows passing of flags to specify which phase of testing to execute.  Consider using when 
# deploying large network
def flag_test(argv):


	ring_ports = parse_ring_ports(argv[0])
	bunch = parse_bunch(argv[1])
	flag = argv[4]

	# Location of mongod program
	if argv[3] == "default" or argv[3] == "d":
		mpath = "/home/accts/km637/mongodb-linux-i686-3.0.1/bin"
	else:
		mpath = argv[3]

	# Local host name
	localhost = socket.gethostname()

	if flag == "1" or flag == "build_cfg":
		build_cfg (mpath, localhost, ring_ports)
		build_shards (mpath, localhost, bunch)

	elif flag == "2" or flag == "build_mongos":
		build_mongos (mpath, localhost, ring_ports)

	elif flag == "3" or flag == "connect_shards":
		connect_shards(mpath, localhost, bunch)

	elif flag == "4" or flag == "shard_collections":
		shard_collections(mpath, localhost, ring_ports)

	elif flag == "5" or flag == "instructions":
		run_instructions(argv[2], mpath, localhost, ring_ports, bunch)

	elif flag == "6" or flag == "drop":
		drop_dbs(mpath, localhost, ring_ports)

	elif flag == "7" or flag == "kill_mongos":
		kill_mongos (mpath, localhost, ring_ports)

	elif flag == "8" or flag == "kill_cfg":
		kill_cfg (mpath, localhost, ring_ports)
		kill_shards (mpath, localhost, bunch)


def main(argv):

	if len(argv) < 4:
		print "Call as trader.py [port file] [bunch file] [instructions file] [mongo bin path] [(stage flag)]"
		return
	
	if len(argv) == 5:
		flag_test(argv)

	else:
		manual_test(argv)


if __name__ == "__main__":
    main(sys.argv[1:])