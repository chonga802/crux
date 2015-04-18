#!/usr/bin/python

# XXX: This file depends on the Fabric module! Calling raw ssh from within
# Python is *extremely* error-prone.

import subprocess
import os
import fabric
from fabric.api import *
from fabric.operations import put

def setup_env(node_file_name, username, key_file):
    node_file = open(node_file_name)
    node_list = []
    for node in node_file:
        node = node.split()[0]          # Deal with trailing whitespace
        node_list.append(node)
    node_file.close()
    env.hosts = node_list
    print env.hosts
    env.user = username
    env.key_filename = key_file
    env.disable_known_hosts = True
    env.warn_only = True

@parallel
def copy_single(username, key_file, file_name, destination_dir):
    print env.host_string
    subprocess.call(['scp', '-i', key_file, file_name, 
                     username+'@'+env.host_string+':~/'+destination_dir])

def pull_latencies(destination_dir, key_file):
    subprocess.call(['scp', '-i', key_file, \
                     'yale_locsys@'+env.host_string+':~/ping_times.txt', '.'])
    file_location = os.path.join(destination_dir, env.host_string + '.txt')
    subprocess.call(['mv', 'ping_times.txt', file_location])

@parallel
def pull_pubsub_results(destination_dir, key_file):
    subprocess.call(['mkdir', env.host_string])
    subprocess.call(['scp', '-i', key_file, \
                     'yale_locsys@'+env.host_string+':~/locsys/results/latency.txt',\
                     env.host_string])
    file_host = os.path.join(destination_dir, env.host_string+'.txt')
    downloaded_file = os.path.join(env.host_string, 'latency.txt')
    subprocess.call(['mv', downloaded_file, file_host])
    subprocess.call(['rm', '-rf', env.host_string])

    

@parallel
def pull_results(destination_dir, key_file):
    subprocess.call(['mkdir', env.host_string])
    subprocess.call(['scp', '-i', key_file, \
                     'yale_locsys@'+env.host_string+':~/locsys/results/latency.txt',\
                     env.host_string])
    subprocess.call(['scp', '-i', key_file, \
                     'yale_locsys@'+env.host_string+':~/locsys/results/get_bamboo_compact_latencies.txt',\
                     env.host_string])    
    put_file_host = os.path.join(destination_dir, 'put_'+env.host_string+'.txt')
    get_file_host = os.path.join(destination_dir, 'get_'+env.host_string+'.txt')
    downloaded_put_file = os.path.join(env.host_string, 'put_bamboo_compact_latencies.txt')
    downloaded_get_file = os.path.join(env.host_string, 'get_bamboo_compact_latencies.txt')
    subprocess.call(['mv', downloaded_put_file, put_file_host])
    subprocess.call(['mv', downloaded_get_file, get_file_host])
    subprocess.call(['rm', '-rf', env.host_string])


@parallel
def deploy_bamboo(username, key_file, bundle_file):
    bundle_archive = bundle_file+'.tar.gz'
    home_dir = os.path.join('/home', username)
    jdk_path = os.path.join(home_dir, bundle_file)
    
    cleanup_cmd = 'rm -rf ' + bundle_file + '*'
    unzip_cmd = 'tar xzf ' + bundle_archive

    run(cleanup_cmd)
    subprocess.call(['scp', '-i', key_file, bundle_archive, 
                     username+'@'+env.host_string+':~/'])
    run(unzip_cmd)

@parallel
def kill_bamboo():
    with fabric.context_managers.cd('/home/yale_locsys/locsys/'):
        run('./locsys_kill.py java')
        run('./locsys_kill.py locsys_daemon')
        

def kill_python():
    run('killall python')

@parallel
def kill_ping():
    with fabric.context_managers.cd('/home/yale_locsys/'):
        run('rm ping_times.txt')
    run('killall locsys_pin.py')


@parallel
def start_ping():
    with fabric.context_managers.cd('/home/yale_locsys/'):
        run('nohup ./locsys_ping.py all_nodes.txt ping_times.txt &')

@parallel
def put_memcached():
    with fabric.context_managers.cd('/home/yale_locsys/locsys/'):
        run('./locsys_daemon.py -f 5 -c plconfigs -o '
            'results/put_latencies.txt')

@parallel
def single_put_memcached():
    with fabric.context_managers.cd('/home/yale_locsys/locsys/'):
        run('./locsys_daemon.py -f 9 -c plconfigs -o '
            'results/single_put_latencies.txt')

@parallel
def get_memcached():
    with fabric.context_managers.cd('/home/yale_locsys/locsys/'):
        run('./locsys_daemon.py -f 6 -c plconfigs -o '
            'results/get_latencies.txt')

@parallel
def single_get_memcached():
    with fabric.context_managers.cd('/home/yale_locsys/locsys/'):
        run('./locsys_daemon.py -f 10 -c plconfigs -o '
            'results/single_get_latencies.txt')

@parallel
def start_memcached():
    with fabric.context_managers.cd('/home/yale_locsys/locsys/'):
        run('./locsys_daemon.py -f 4 -c plconfigs -m ' 
            '/home/yale_locsys/memcached')

@parallel
def single_start_memcached():
    with fabric.context_managers.cd('/home/yale_locsys/locsys/'):
        run('./locsys_daemon.py -f 8 -c plconfigs -m ' 
            '/home/yale_locsys/memcached')

@parallel
def kill_redis():
    with fabric.context_managers.cd('/home/yale_locsys/locsys/'):
        run('./locsys_kill.py redis-server')
    
@parallel
def start_redis(compact):
    with fabric.context_managers.cd('/home/yale_locsys/locsys/'):
        if compact == 'compact':
            run('./locsys_daemon.py -f 11')
        else:
            run('./locsys_daemon.py -f 14')            
        
@parallel
def start_redis_subscribers(compact):    
    with fabric.context_managers.cd('/home/yale_locsys/locsys/'):
        if compact == 'compact':            
            run('nohup ./locsys_daemon.py -f 12 &')
        else:
            run('nohup ./locsys_daemon.py -f 15 &')

@parallel
def start_redis_publishers(compact):
    with fabric.context_managers.cd('/home/yale_locsys/locsys/'):
        if compact == 'compact':
            run('./locsys_daemon.py -f 13 ')
        else:
            run('./locsys_daemon.py -f 16 ')


@parallel
def kill_memcached():
    with fabric.context_managers.cd('/home/yale_locsys/locsys/'):
        run('./locsys_kill.py memcached')

def start_bamboo():
    with fabric.context_managers.cd('/home/yale_locsys/locsys/'):
        run('nohup ./locsys_daemon.py -f 0 &')

def start_plain_bamboo():
    with fabric.context_managers.cd('/home/yale_locsys/locsys/'):
        run('nohup ./locsys_daemon.py -f 3 &')

@parallel
def get_experiment():
    with fabric.context_managers.cd('/home/yale_locsys/locsys/'):
        run('./locsys_daemon.py -f 2 -o results/get_bamboo_compact_latencies.txt')

@parallel
def put_experiment():
    with fabric.context_managers.cd('/home/yale_locsys/locsys/'):
        run('./locsys_daemon.py -f 1 -o results/put_bamboo_compact_latencies.txt')


def set_jdk_path():
    jdk_path = '/home/yale_locsys/jdk/'
    unzip_cmd = 'tar xzf jdk.tar.gz'
    javapath_cmd = 'echo export JAVAHOME=' + jdk_path + ' >> ~/.bashrc'
    run('rm -rf /home/yale_locsys/jdk')
    run(unzip_cmd)
    run(javapath_cmd)

def deploy_jdk(username, key_file, bundle_file):
    bundle_archive = bundle_file+'.tar.gz'
    home_dir = os.path.join('/home', username)
    jdk_path = os.path.join(home_dir, bundle_file)
    
    cleanup_cmd = 'rm -rf ' + bundle_file + '*'
    unzip_cmd = 'tar xzf ' + bundle_archive
    javapath_cmd = 'echo export JAVAHOME=' + jdk_path + ' >> ~/.bashrc'


    run(cleanup_cmd)
    subprocess.call(['scp', '-i', key_file, bundle_archive, 
                     username+'@'+env.host_string+':~/'])
    run(unzip_cmd)
    run(javapath_cmd)
    
@parallel
def deploy_experiment(username, key_file, bundle_file):
    # Setup the environment and configuration needed to upload the bundle to the
    # remote node, extract it, and setup some env variables.
    bundle_archive = bundle_file+'.tar.gz'
    unzip_cmd = 'tar xzf ' + bundle_archive
    home_dir = os.path.join('/home', username)
    jdk_path = os.path.join(home_dir, bundle_file, 'jdk')

    cleanup_cmd = 'rm -rf ' + bundle_file + '*'
    

    run(cleanup_cmd)

    subprocess.call(['scp', '-i', key_file, bundle_archive, 
                     username+'@'+env.host_string+':~/'])
    run(unzip_cmd)
#    run(javapath_cmd)
