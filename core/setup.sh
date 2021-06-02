#!/bin/bash


## Install packages:
echo "Installing packages ..."
apt-get update
apt-get install python-pip
sudo apt-get install sqlite3
pip install python-swiftclient
pip install python-keystoneclient
sudo apt-get install s3cmd
sudo curl https://rclone.org/install.sh | bash


## Load environment variables:
if [ ! -f .env ]
then
  export $(cat .env | xargs)
fi
