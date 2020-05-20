# MongoDB Cloud Project

This project consisted of configuring a MongoDB database manually in the cloud and using this database to handle and query millions of records pertaining to freeway data collected through the Oregon Department of Transportation (ODOT). The cloud provider used in this project is Google Cloud and the resources that are used within this platform are ten identical VM instances each created through a custom template that consists of n1-standard-2 (2vCPUs, 7.5 GB memory). All of the VM instances are contained in the same Virtual Private Cloud so that they can communicate with one another through their internal IP addresses. Each of the instances are configured such that they fall into one of three categories – a router to communicate with the application, a config server to store metadata of the shards, and shards to shard the data throughout the cluster. The additional VMs are part of a replica set of each of those categories with the exception of the router. The design for the entire system can be seen below.

<p align="center">
  <img src="https://github.com/dmesa2/MongoDB-Cloud-Project/blob/master/Images/System%20Design.png?raw=true" alt="SYSTEM DESIGN"/>
</p>

The above diagram maps to each of the instances below that are running in the Google Cloud Platform:

<p align="center">
  <img src="https://github.com/dmesa2/MongoDB-Cloud-Project/blob/master/Images/VM%20Instances.png?raw=true" alt="VM_INSTANCES"/>
</p>

After getting ten instances running, I proceeded to ssh into each one and update the system as well as install the latest version of MongoDB. After the initial setup, I then created a configuration file in each MongoDB instance to assign it a role in the cluster. Each of those configuration files look similar to this:

<p align="center">
  <img src="https://github.com/dmesa2/MongoDB-Cloud-Project/blob/master/Images/Config%20File.png?raw=true" alt="CONFIG FILE"/>
</p>

Depending on the specific instance being configured, the port address would need to be changed to the respective port as well as the IP address. Sharding and replication would also need to be changed to the respective roles. For the above image, I am configuring that instance to port 27019 which is the port for config servers, I’m inserting the internal IP address that belongs to that instance to the bindIP, I’m letting the system know that the cluster role for this instance is a configsvr, and that it belongs to the ConfigReplSet replication set. 

After configuring each config file in each of the ten VM instances, I then proceeded to connect the systems such that it matches the above database system. I began this procedure by first creating the replica sets for the configuration servers, and for both shard clusters. This was done through ssh’ing into one of the VM instances, logging into the mongo router, and running the MongoDB replication command and providing the respective arguments. 

At this stage, it was time to import the Freeway data which consists of over 17 million records into the database system. I used the MongoDB Compass application to connect to my database system and upload the data. Afterwards, the database look like this:

<p align="center">
  <img src="https://github.com/dmesa2/MongoDB-Cloud-Project/blob/master/Images/MongoDB%20Compass%20Data.png?raw=true" alt="COMPASS"/>
</p>

Once the data was imported, I cleaned the data by removing irrelevant information such as keys with empty values and speeds that consisted of ‘zero’ values. I then sharded the FreewayLoop collection that contains over 17 million records using a hash function with the shard key being the detectorid key:

<p align="center">
  <img src="https://github.com/dmesa2/MongoDB-Cloud-Project/blob/master/Images/Shard%20Diagram.png?raw=true" alt="SHARD DIAGRAM"/>
</p>

The database contains five collections total (four are relevant but the additional one was used as a subset to the larger collection for the initial queries). 

For the queries on the dataset, I used PyMongo which is a Python framework that connects to the MongoDB router. PyMongo is a great framework as it allows the user to query the database and then use the results from that query to perform more complex analysis with Python code. The following results are from three queries (The code to the queries can be seen in the QueryScript.py in the Code folder.

<p align="center">
  <img src="https://github.com/dmesa2/MongoDB-Cloud-Project/blob/master/Images/Query%20Results.png?raw=true" alt="QUERY RESULTS"/>
</p>
