#!/usr/bin/python

import socket
import time
import json
import random

class DIndexService():
    def __init__(self, config, index=1, end=1):
        """
        Constructor used to initialize class object.
        """
        self.config = config
        self.mod_function = len(config['servers'])
        self.key_start = index
        self.key_end = end
        self.workload = []
        self.server_sockets = []

    def _hash_function(self, key):
        """
        hash_function method is used to return the server location for
        storage/retrieval of key,value based on the hash function calculation.

        @param key:    The value stored as key in distributed index server.
        """
        try:
            h = hash(key)
            index = h % self.mod_function
            return index
        except Exception as e:
            print "hash function error: %s" % e

    def establish_connection(self):
        """
        Establish socket connection with DHT servers.
        """
        try:
            for i in range(0,len(self.config['servers'])):
                timeout = 0
                while timeout < 60:
                    try:
                        s = \
                            socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        s.setsockopt(
                            socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                        s.setsockopt(
                            socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                        s.connect(
                                (self.config['servers'][i]['ip'],
                                 self.config['servers'][i]['port']))
                        self.server_sockets.append(s)
                        break
                    except Exception as e:
                        time.sleep(10)
                        timeout = timeout + 10
        except Exception as e:
            print "Establish Connection Error: %s" % e

    def disable_connection(self):
        """
        Disable socket connection with DHT servers.
        """
        try:
            for s in self.server_sockets:
                cmd_issue = {
                    'command' : 'close'
                }
                try:
                    s.sendall(json.dumps(cmd_issue))
                    s.close()
                except Exception as e:
                    pass
            del self.server_sockets[:]
        except Exception as e:
            print "Disable Connection Error: %s" % e

    def generate_workload(self):
        """
        This method is used to Generate Key Value work load.
        """
        try:
            print "Generating workload..."
            for i in range(self.key_start, self.key_end):
                key = str(random.randrange(10**9, 10**10))
                value = key + '*' * (90-len(key))
                index = self._hash_function(key)
                self.workload.append([key,value,index])
        except Exception as e:
            print "Generating Workload Error: %s" % e
    
    def put(self, key, value):
        """
        Put method is used to store the key and value in the
        distributed index server.

        @param key:     Key to be stored in the Index Server.
        @param value:   Value to be stored in the Index Server.
        """
        try:
            print "Starting Put Operation Benchmark..."
            t1 = time.time()
            for key,value,index in self.workload:
                cmd_issue = {
                    'command' : 'put',
                    'key' : key,
                    'value' : value
                }
                self.server_sockets[index].sendall(json.dumps(cmd_issue))
                rcv_data = json.loads(self.server_sockets[index].recv(1024))
            t2 = time.time()
            total_ops = len(self.workload)
            print "Successfully completed: %s operations" % total_ops
            print "%s Put operations = %s sec" % (total_ops,t2-t1)
            print "per Put operation = %s msec" % (((t2-t1)/total_ops)*1000)
            print "Throughput of Put operation = %s Kilo Ops/sec" % ((total_ops/(t2-t1))/1000)

        except Exception as e:
            print "Put function error: %s" % e

    def get(self, key):
        """
        Get method is used to retrieve the value from the
        distributed index server.

        @param key:    the key whose value needs to be retrieved.
        """
        try:
            print "Starting Get Operation Benchmark..."
            t1 = time.time()
            for key,value,index in self.workload:
                cmd_issue = {
                    'command' : 'get',
                    'key' : key
                }
                self.server_sockets[index].sendall(json.dumps(cmd_issue))
                rcv_data = json.loads(self.server_sockets[index].recv(1024))
            t2 = time.time()
            total_ops = len(self.workload)
            print "Successfully completed: %s operations" % total_ops
            print "%s Get operations = %s sec" % (total_ops,t2-t1)
            print "per Get operation = %s msec" % (((t2-t1)/total_ops)*1000)
            print "Throughput of Get operation = %s Kilo Ops/sec" % ((total_ops/(t2-t1))/1000)

        except Exception as e:
            print "Get function error: %s" % e

    def delete(self, key):
        """
        delete method is used to delete the key and value from the
        distributed index server.

        @param key:    the key whose entree needs to be deleted.
        """
        try:
            print "Starting Delete Operation Benchmark..."
            t1 = time.time()
            for key,value,index in self.workload:
                cmd_issue = {
                    'command' : 'delete',
                    'key' : key
                }
                self.server_sockets[index].sendall(json.dumps(cmd_issue))
                rcv_data = json.loads(self.server_sockets[index].recv(1024))
            t2 = time.time()
            total_ops = len(self.workload)
            print "Successfully completed: %s operations" % total_ops
            print "%s Delete operations = %s sec" % (total_ops,t2-t1)
            print "per Delete operation = %s msec" % (((t2-t1)/total_ops)*1000)
            print "Throughput of Delete operation = %s Kilo Ops/sec" % ((total_ops/(t2-t1))/1000)

        except Exception as e:
            print "Delete function error: %s" % e

__author__ = 'arihant'
