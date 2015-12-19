Download and Install Redis:
$ wget http://download.redis.io/releases/redis-3.0.5.tar.gz
$ tar xzf redis-3.0.5.tar.gz
$ cd redis-3.0.5
$ make

Test Installation:
$ make test

Start Redis Server:
$ src/redis-server

Stop Redis Server:
control + c

Python Client:
$ sudo pip install redis

Note:
	* Redis Default port: 6379
	* pre req: 
		* sudo apt-get install gcc
		* sudo apt-get install g++
		* sudo apt-get install tcl8.6

Start Client:
1) cd to Redis/client folder.
2) config.json: Verify and modify the IP and port as per the server connections.
3) run : $python PeerBenchmark.py -c config.json -i 100000 -e 200000

	$ python PeerBenchmark.py [-h] -c CONFIG -i INDEX -e END

		Standard Arguments for talking to Distributed Index Server

		optional arguments:
			  -h, --help            show this help message and exit
			  -c CONFIG, --config CONFIG
			                        Config file of the network
			  -i INDEX, --index INDEX
			                        key range start index
			  -e END, --end END     
						key range end index
		Note:	* All arugment is mandatory.
or
4) chmod +x startbenchmarkclient.sh
5) run : $./startbechmarkclients.sh