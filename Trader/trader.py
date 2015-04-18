## Python implementation of the Crux scheme for a transactional trading database
##
## 
##
## 
## 
## 
## 

import subprocess
import time
import os


def build_rings (mpath, portlist):

	for port in portlist:

		if not os.path.exists(mpath+'/data'+port):
			os.makedirs(mpath+'/data'+port)

		p = subprocess.Popen([mpath + '/mongod', '--dbpath', mpath+'/data'+port, '--port', port], stdout=subprocess.PIPE)	
		out = p.communicate()[0]
		print out

	return

def post_trade ():



	return

def kill_rings (mpath, portlist):

	for port in portlist:

		subprocess.Popen([mpath + '/mongod', '--dbpath', mpath+'/data'+port, '--shutdown'])

	return

# Location of mongod program
mpath = "/home/accts/km637/mongodb-linux-i686-3.0.1/bin"

portlist = ["27017","27018"]

bunchfile = [("turtle", "27017")]

build_rings (mpath, portlist)

time.sleep(1)

# out = subprocess.check_output([mpath + "/mongo", "--eval", "db.adminCommand('listDatabases')"])

# print out*10

# out = subprocess.check_output([mpath + "/mongo", "--eval", "db.trades.insert({item:'card', qty: 15})"])

# print out*10

# out = subprocess.check_output([mpath + "/mongo", "--eval", "db.getCollectionNames()"])

# print out*10



time.sleep(1)

kill_rings (mpath, portlist)

# subprocess.Popen([mongodpath + '/mongod', '--dbpath', mongodpath+'/data', '--port', '27017'])

# # out = subprocess.Popen([mongodpath + '/mongod', '--dbpath', mongodpath+'/data2', '--port', '27018'])

# time.sleep(1)

# print "\n"*10

# out = subprocess.check_output([mongodpath + '/mongo', '--eval', 'printjson(db.getCollectionNames())'])

# print out*10

# print "\n"*10

# time.sleep(1)


# client = MongoClient('localhost', 27017)

# db = client.test_database

# post = {"author": "Mike"}

# posts = db.posts
# post_id = posts.insert_one(post).inserted_id
# print post_id

# print db.collection_names(include_system_collections=False)

# client2 = MongoClient('localhost', 27018)

# db = client2.test_database

# post = {"author": "Mike"}

# posts = db.posts
# post_id = posts.insert_one(post).inserted_id
# print post_id

# print db.collection_names(include_system_collections=False)


# subprocess.Popen([mongodpath + '/mongod', '--dbpath', mongodpath+'/data', '--shutdown'])
# subprocess.Popen([mongodpath + '/mongod', '--dbpath', mongodpath+'/data2', '--shutdown'])


def ask (trade):


	return


def bid (trade):


	return


def check_sales ():


	return

