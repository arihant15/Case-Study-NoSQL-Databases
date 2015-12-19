#!/usr/bin/python

import time
import json
import random
import argparse
import sys
from httplib2 import Http

def get_args():
    """
    Get command line args from the user.
    """
    parser = argparse.ArgumentParser(
        description='Standard Arguments for talking to MongoDB Server')
    parser.add_argument('-c', '--config',
                        required=True,
                        action='store',
                        help='Config file of the network')
    parser.add_argument('-i', '--index',
                        type=int,
                        required=True,
                        action='store',
                        help='key range start index')
    parser.add_argument('-e', '--end',
                        type=int,
                        required=True,
                        action='store',
                        help='key range end index')
    args = parser.parse_args()
    return args

class Service():
    def __init__(self, config, index=1, end=1):
        """
        Constructor used to initialize class object.
        """
        self.config = config
        self.mod_function = len(config['servers'])
        self.key_start = index
        self.key_end = end
        self.workload = []
		self.revision_key = []
        self.h = Http()
		self.db = "benchmark"

    def _hash_function(self, key):
        """
        hash_function method is used to return the server location for
        storage/retrieval of key,value based on the hash function calculation.

        @param key:    The value stored as key in MongoDB server.
        """
        try:
            h = hash(key)
            index = h % self.mod_function
            return index
        except Exception as e:
            print "hash function error: %s" % e

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
        CouchDB server.

        @param key:     Key to be stored in the Server.
        @param value:   Value to be stored in the Server.
        """
        try:
            print "Starting CouchDB Insert Operation Benchmark..."
            t1 = time.time()
            for key,value,index in self.workload:
                data = {
				    "value" : value
                    }
				rp,content=self.h.request("http://"+self.config['servers'][index]['ip']+":5984/"+self.db+"/"+key,  "PUT",headers={"Content-type":"application/json"} ,body=data)
				self.revision_key[key]=json.loads(content)["rev"]
            t2 = time.time()
            total_ops = len(self.workload)
            print "Successfully completed: %s operations" % total_ops
            print "%s Insert operations = %s sec" % (total_ops,t2-t1)
            print "per Insert operation = %s msec" % (((t2-t1)/total_ops)*1000)
            print "Throughput of Insert operation = %s Kilo Ops/sec" % ((total_ops/(t2-t1))/1000)
        except Exception as e:
            print "Insert function error: %s" % e

    def get(self, key):
        """
        Get method is used to retrieve the value from the
        CouchDB server.

        @param key:    the key whose value needs to be retrieved.
        """
        try:
            print "Starting CouchDB Lookup Operation Benchmark..."
            t1 = time.time()
            for key,value,index in self.workload:
				rp=self.h.request("http://"+self.config['servers'][index]['ip']+":5984/"+self.db+"/"+key,  "GET",headers={"Content-type":"application/json"} )
            t2 = time.time()
            total_ops = len(self.workload)
            print "Successfully completed: %s operations" % total_ops
            print "%s Lookup operations = %s sec" % (total_ops,t2-t1)
            print "per Lookup operation = %s msec" % (((t2-t1)/total_ops)*1000)
            print "Throughput of Lookup operation = %s Kilo Ops/sec" % ((total_ops/(t2-t1))/1000)
        except Exception as e:
            print "Lookup function error: %s" % e

    def delete(self, key):
        """
        delete method is used to delete the key and value from the
        CouchDB server.

        @param key:    the key whose entree needs to be deleted.
        """
        try:
            print "Starting CouchDB Delete Operation Benchmark..."
            t1 = time.time()
            for key,value,index in self.workload:
				rp=self.h.request("http://"+self.config['servers'][index]['ip']+":5984/"+self.db+"/"+key+"?rev="+self.revision_key[key],  "DELETE",headers={"Content-type":"application/json"} )
            t2 = time.time()
            total_ops = len(self.workload)
            print "Successfully completed: %s operations" % total_ops
            print "%s Delete operations = %s sec" % (total_ops,t2-t1)
            print "per Delete operation = %s msec" % (((t2-t1)/total_ops)*1000)
            print "Throughput of Delete operation = %s Kilo Ops/sec" % ((total_ops/(t2-t1))/1000)
        except Exception as e:
            print "Delete function error: %s" % e

if __name__ == '__main__':
    """
    Main method starting deamon threads and peer operations.
    """
    try:
        print "Starting CouchDB Client..."
        args = get_args()
        with open(args.config) as f:
            config = json.loads(f.read())
        service = Service(config, args.index, args.end)
        service.establish_connection()
        service.generate_workload()
        time.sleep(1)
        service.put(1,1)
        time.sleep(5)
        service.get(1)
        time.sleep(5)
        service.delete(1)
    except Exception as e:
        print "main function error: %s" % e
        sys.exit(1)
    except (KeyboardInterrupt, SystemExit):
        print "Peer Shutting down..."
        time.sleep(1)
        sys.exit(1)

__author__ = 'arihant'