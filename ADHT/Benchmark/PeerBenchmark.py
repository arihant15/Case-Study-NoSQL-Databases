#!/usr/bin/python

import time
import json
import argparse
from DIndexServiceBenchmark import DIndexService
import sys

def get_args():
    """
    Get command line args from the user.
    """
    parser = argparse.ArgumentParser(
        description='Standard Arguments for talking to Distributed Index Server')
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

if __name__ == '__main__':
    """
    Main method starting deamon threads and peer operations.
    """
    try:
        print "Starting DHT Client..."
        args = get_args()
        with open(args.config) as f:
            config = json.loads(f.read())

        service = DIndexService(config, args.index, args.end)
        service.establish_connection()
        service.generate_workload()
        time.sleep(1)
        service.put(1,1)
        service.disable_connection()
        time.sleep(5)
        service.establish_connection()
        service.get(1)
        service.disable_connection()
        time.sleep(5)
        service.establish_connection()
        service.delete(1)
        service.disable_connection()

    except Exception as e:
        print "main function error: %s" % e
        sys.exit(1)
    except (KeyboardInterrupt, SystemExit):
        print "Peer Shutting down..."
        time.sleep(1)
        sys.exit(1)

__author__ = 'arihant'
