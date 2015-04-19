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

# Construction of rings A
# Given list of ports, makes Mongo databases on those ports centered on local host
def build_rings (mpath, portlist):

	for port in portlist:

		if not os.path.exists(mpath+'/data'+port):
			os.makedirs(mpath+'/data'+port)

		# out = subprocess.check_output(["echo", "Hello World!"])

		p = subprocess.Popen([mpath + '/mongod', '--dbpath', mpath+'/data'+port, '--port', port], stdout=subprocess.PIPE)
		# result = p.communicate()[0]
		# print "STARTED:" + result

	return

# Destruction of rings A
# Given list of ports, shuts down Mongo databases on those ports centered on local host
def kill_rings (mpath, portlist):

	for port in portlist:

		subprocess.Popen([mpath + '/mongod', '--dbpath', mpath+'/data'+port, '--shutdown'])

	return

# t_type is "WANT"/"SELL"
# t_id is object ID
# username contains information for direct connection to poster of trade
def post_trade (mpath, host, port, t_type, t_id, username):

	command = "db.trades.insert({type:'"+t_type+"', object: '"+t_id+"', user: '"+username+"'})"

	p = subprocess.Popen([mpath + "/mongo", "--eval", command], stdout=subprocess.PIPE)
	result = p.communicate()[0]
	print "TRADE OUT:" + result

	return

def find_trade (mpath, host, port, t_id):

	command = "var myCursor = db.trades.find({object: '"+t_id+"'}); \
myCursor.forEach(printjson);"

	p = subprocess.Popen([mpath + "/mongo", "--port", port, "--host", host, "--eval", command], stdout=subprocess.PIPE)
	result = p.communicate()[0]
	print "TRADE FOUND:" + result

	return

# Drops given collection
def clear_collection (mpath, host, port, db_name):

	p = subprocess.Popen([mpath + "/mongo", "--eval", "db."+db_name+".drop()"], stdout=subprocess.PIPE)
	result = p.communicate()[0]
	print "CLEARED:" + result

	return

# Shows available collections
def show_collections (mpath, host, port):

	p = subprocess.Popen([mpath + "/mongo", "--port", port, "--eval", "db.getCollectionNames()"], stdout=subprocess.PIPE)
	result = p.communicate()[0]
	print "COLLECTIONS:" + result

	return


# Location of mongod program
mpath = "/home/accts/km637/mongodb-linux-i686-3.0.1/bin"
# Local host name
localhost = socket.gethostname()

build_rings (mpath, portlist)

# maybe later fix so that read pipe, resume when rings are set up
time.sleep(1)

####################################################
# Example instance

portlist = ["27017","27018"]

bunchfile = [("turtle", "27017")]

# post_trade (mpath, "", portlist, "HAVE", "123", "Koji")

for i in range(10):
	find_trade(mpath, localhost, "27017", "123")

# 	show_collections(mpath, "", "27017")

time.sleep(1)

kill_rings (mpath, portlist)

# out = subprocess.check_output([mpath + "/mongo", "--eval", "db.adminCommand('listDatabases')"])
# print out*10

# out = subprocess.check_output([mongodpath + '/mongo', '--eval', 'printjson(db.getCollectionNames())'])
# print out*10
# print "\n"*10

# time.sleep(1)


def ask (trade):


	return


def bid (trade):


	return


def check_sales ():


	return

