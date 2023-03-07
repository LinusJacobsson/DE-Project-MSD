#!/bin/bash

# Configuration of Spark master node

# Written by Linus Jacobsson
# March 7 2023


#Check for argument
if [ $# == 0 ]; then
    echo "Usage: $0 <public ip of master node>"
    exit 1
fi

# Update the package list
sudo apt update

# Check if Java is installed
if ! command -v java &> /dev/null
then
    echo "Java is not installed. Installing Java..."
    sudo apt install openjdk-8-jdk
else
    echo "Java is already installed."
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "Python is not installed. Installing Python..."
    sudo apt install python3
else
    echo "Python is already installed."
fi

# Download and install Spark
wget 
https://dlcdn.apache.org/spark/spark-3.3.2/spark-3.3.2-bin-hadoop3.tgz
tar -xvf spark-3.3.2-bin-hadoop3.tgz
sudo mv spark-3.3.2-bin-hadoop3/ /opt/spark

# Set environment variables
echo 'export SPARK_HOME=/opt/spark' >> ~/.bashrc
echo 'export PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin' >> ~/.bashrc
echo "export SPARK_MASTER_HOST=$1" >> /opt/spark/conf/spark-env.sh
source ~/.bashrc

