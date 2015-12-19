Steps to Install Java 8:
1) sudo add-apt-repository ppa:webupd8team/java
2) sudo apt-get update
3) sudo apt-get install oracle-java8-installer

Switching between Oracle Java 8 and Java 7:
1) sudo update-java-alternatives -s java-7-oracle
2) sudo update-java-alternatives -s java-8-oracle

Setting Java environment variables:
1) sudo apt-get install oracle-java8-set-default

Steps to Setup Cassandra:

1) echo "deb http://debian.datastax.com/community stable main" | sudo tee -a /etc/apt/sources.list.d/cassandra.sources.list
2) curl -L http://debian.datastax.com/debian/repo_key | sudo apt-key add -
3) sudo apt-get update
4) sudo apt-get install cassandra

Start-Up Cassandra:
1) sudo cassandra -f
or
2) sudo /etc/init.d/cassandra start (dont use this -- this is only for cassandra as a service)

Check Cassandra Service status
1) ps -ef | grep cassandra

Shutdown Cassandra:
1) kill -9 <pid>
or
2) sudo /etc/init.d/cassandra stop (dont use this -- this is only for cassandra as a service)

Remove Cassandra databases and log files:
1) sudo rm -r /var/log/cassandra
1) sudo rm -r /var/lib/cassandra

Note:
	* Cassandra default port: native_transport_port: 9042
	* Stop cassandra to modify the conf file to allow cassandra db to listen to all ports.
	* vi /etc/cassandra/cassandra.yaml
	* # Listen to local interface only. Make the below change to listen on all interfaces. 
	  rpc_address: localhost --> comment out
	  rpc_address: 0.0.0.0 --> set this value
	  broadcast_rpc_address: 1.2.3.4 --> uncomment this line



Py Cassandra:
1) sudo apt-get install freetds-dev
2) sudo apt-get install python-dev
3) sudo pip install cassandra-driver

Cassandra cli:
1) cqlsh
2) CREATE KEYSPACE mykeyspace
WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 };
3) USE mykeyspace;
4) CREATE TABLE benchmark (
  key text PRIMARY KEY,
  value text
);
5) SELECT * FROM benchmark;

Start Client:
1) cd to Cassandra/client folder.
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
