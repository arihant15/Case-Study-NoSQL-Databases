Steps to Setup MongoDB:

1) sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10
2) echo 'deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen' | sudo tee /etc/apt/sources.list.d/mongodb.list
3) sudo apt-get update
4) sudo apt-get install -y mongodb-org

Start-Up MongoDB:
1) sudo service mongod start

Check MongoDB Service Status
1) sudo service mongod status

Shutdown MongoDB:
1) sudo service mongod stop

Restart MongoDB:
1) sudo service mongod restart

Remove any MongoDB packages that you had previously installed:
1) sudo apt-get purge mongodb-org*

Remove MongoDB databases and log files:
1) sudo rm -r /var/log/mongodb
1) sudo rm -r /var/lib/mongodb

Note:
	* Mongo DB default port: 27017
	* MongoDB starts automatically after install
	* Stop MongoDB to modify the conf file to allow mongo db to listen to all ports.
	* sudo vi /etc/mongod.conf
	* # Listen to local interface only. Comment out to listen on all interfaces. 
	  # bind_ip = 127.0.0.1


Py Mongo:
1) sudo pip install pymongo

Start Client:
1) cd to MongoDB/client folder.
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
4) chmod +x startbenchmark.sh
5) run : $./startbechmarkclients.sh