## Python implementation of the Crux scheme for a transactional trading database
##
## Christine Hong; Kojiro Murase; Sage Price
##
## 
## 
## 
## 

import subprocess
import time
import os
import socket
import sys

# Given file listing local ports on which to build rings, returns in list form
def parse_ports(fn):

	f = open(fn)
	l = f.read().splitlines()

	return l

# Given file listing bunches to search returns as list of tuples
def parse_bunch(fn):

	b = []

	f = open(fn)
	l = f.read().splitlines()

	for elt in l:
		s = elt.split()
		b.append((s[0],s[1]))

	return b

# Construction of rings A
# Given list of ports, makes Mongo databases on those ports centered on local host
def build_rings (mpath, host, portlist):

	print "-"*40
	print "Building on ports", portlist

	host = host.split(".")[0]

	for port in portlist:

		mypath = mpath+'/data_at_'+host+"_"+port

		if not os.path.exists(mypath):
			os.makedirs(mypath)

		# out = subprocess.check_output(["echo", "Hello World!"])

		subprocess.Popen([mpath + '/mongod', '--dbpath', mypath, '--port', port])#, stdout=subprocess.PIPE)
		# result = p.communicate()[0]
		# print "STARTED:" + result

	return

# Destruction of rings A
# Given list of ports, shuts down Mongo databases on those ports centered on local host
def kill_rings (mpath, host, portlist):

	host = host.split(".")[0]

	for port in portlist:

		mypath = mpath+'/data_at_'+host+"_"+port
		subprocess.Popen([mpath + '/mongod', '--dbpath', mypath, '--shutdown'])

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

	for b in bunch:
		post_instance(mpath, b[0], b[1], t_type, t_id, localhost)

	return

# Search all rings until given trade found
def find_all (mpath, bunch, t_id):

	result = "NO MATCH"
	start_t = time.time()

	print "============================================="
	print "SEARCHING FOR" + t_id

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

	print "DONE SEARCHING FOR" + t_id
	print "============================================="


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
def run_instructions (fn, mpath, localhost, portlist, bunch):

	f = open(fn)

	for instr in f:
		i = instr.split()

		if i[0] == "post":

			post_all(mpath, bunch, i[1], i[2], localhost)

		elif i[0] == "find":

			find_all(mpath, bunch, i[1])


	return

####################################################

def main(argv):

	if len(argv) < 4:
		print "Call as trader.py [port file] [bunch file] [instructions file] [mongo loc (def for default)] "
		return

	portlist = parse_ports(argv[0])
	bunch = parse_bunch(argv[1])

	# Location of mongod program
	if argv[3] == "def" or argv[3] == "d":
		mpath = "/home/accts/km637/mongodb-linux-i686-3.0.1/bin"
	else:
		mpath = argv[3]

	# Local host name
	localhost = socket.gethostname()


	build_rings (mpath, localhost, portlist)

	# maybe later fix so that read pipe, resume when rings are set up
	inp = raw_input("Any key to continue: ")

	if inp != "n":

		# post_trade (mpath, "", portlist, "HAVE", "123", "Koji")
		run_instructions(argv[2], mpath, localhost, portlist, bunch)

		# for i in range(10):
		# 	find_trade(mpath, localhost, "27017", "123")

		# 	show_collections(mpath, "", "27017")

	inp = raw_input("Any key to quit: ")

	if inp != "n":

		# clear out stuff from earlier tests
		for p in portlist:
			clear_collection (mpath, localhost, p, "trades")

		kill_rings (mpath, localhost, portlist)


	# out = subprocess.check_output([mpath + "/mongo", "--eval", "db.adminCommand('listDatabases')"])
	# print out*10

	# out = subprocess.check_output([mongodpath + '/mongo', '--eval', 'printjson(db.getCollectionNames())'])
	# print out*10
	# print "\n"*10

	# time.sleep(1)

if __name__ == "__main__":
    main(sys.argv[1:])