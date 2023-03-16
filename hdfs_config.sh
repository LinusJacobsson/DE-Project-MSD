
#!/bin/bash

# Config script for HDFS
# Written by Linus Jacobsson March 14 2023
# Note! Assumes ssh between nodes is configured 

# Update the package list
sudo apt-get update

# Download Hadoop
wget https://archive.apache.org/dist/hadoop/common/hadoop-2.7.3/hadoop-2.7.3.tar.gz

# Extract the downloaded file
tar -xzvf hadoop-2.7.3.tar.gz

# Move the extracted folder to /usr/local
sudo mv hadoop-2.7.3 /usr/local/hadoop

# Set environment variables
echo 'export HADOOP_HOME=/usr/local/hadoop' >> ~/.bashrc
echo 'export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin' >> ~/.bashrc
source ~/.bashrc

# Configure Hadoop
cd /usr/local/hadoop/etc/hadoop


# Set JAVA HOME in env files
echo 'export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64' >> hadoop-env.sh
echo 'export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64' >> yarn-env.sh
echo 'export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64' >> mapred-env.sh
# Edit the core-site.xml file
echo '<configuration>
	<property>
	<name>fs.default.name</name>
	<value>hdfs://192.168.2.139:50000</value>
	</property>
    </configuration>' > core-site.xml

# Edit the hdfs-site.xml file
echo '<configuration>
        <property>
            <name>dfs.replication</name>
            <value>5</value>
        </property>
	<property>
	<name>dfs.namenode.name.dir</name>
	<value>/home/ubuntu/hdfs_metadata-dir/namenode-dir</value>
	</property>
	<property>
	<name>dfs.datanode.data.dir</name>
	<value>/home/username/hdfs_metadata-dir/datanode-dir</value>
	</property>
    </configuration>' > hdfs-site.xml

# We must first create file from template
cp mapred-site.xml.template mapred-site.xml

# Edit the mapred-site.xml file
echo '<configuration>
        <property>
            <name>mapreduce.framework.name</name>
            <value>yarn</value>
        </property>
    </configuration>' > mapred-site.xml

# Edit the yarn-site.xml file
echo '<configuration>
	<property>
	<name>yarn.nodemanager.aux-services</name> <value>mapreduce_shuffle</value>
	</property>
	<property>
	<name>yarn.nodemanager.aux-services.mapreduce.shuffle.class</name> 
	<value>org.apache.hadoop.mapred.ShuffleHandler</value>
	</property>
	<property>
	<description>The hostname of the RM.</description>
	<name>yarn.resourcemanager.hostname</name>
	<value>192.168.2.139</value>
	</property>
	<property>
	<description>The address of the applications manager interface in the 
RM.</description>
	<name>yarn.resourcemanager.address</name>
	<value>192.168.2.139:8032</value>
	</property>
    </configuration>' > yarn-site.xml

# Enter IP's of slave nodes (including namenode if it is both)
echo '192.168.2.216
      192.168.2.203
      192.168.2.149
      192.168.2.139
      192.168.2.84' > slaves

# ------------------ Should only be done on namenod! -----------------------

# Format the namenode
cd ../../sbin
./hdfs namenode -format

# Start Hadoop
./start-all.sh

# Check Hadoop status
jps

