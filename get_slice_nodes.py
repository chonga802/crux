#!/usr/bin/python

import sys
import xmlrpclib
import sets
import getpass

def get_nodes(login_name):
    api_server = xmlrpclib.Server('https://www.planet-lab.org/PLCAPI/')
    auth= {}
    auth['Username']= login_name
    # always 'password', for password based authentication
    auth['AuthMethod']= "password"
    auth['AuthString']= getpass.getpass()
    # valid roles include, 'user', 'tech', 'pi', 'admin'
    auth['Role']= "user"
    slice_name = 'yale_dissent'
    have_node_ids = api_server.GetSlices(auth, [ slice_name ], \
                                         ['node_ids'])[0]['node_ids']
    return [node['hostname'] for node in api_server.GetNodes(auth, \
                                                             have_node_ids, \
                                                             ['hostname'])]    

def main():
    output_file_name = sys.argv[1]
    login_name = sys.argv[2]
    node_list = get_nodes(login_name)
    output_file = open(output_file_name, 'w')
    for node in node_list:
        output_file.write(node + '\n')
    output_file.close()

if __name__ == '__main__':
    main()


