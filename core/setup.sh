#!/bin/bash


## Install packages:
echo "Installing packages ..."
apt-get update
apt-get install python-pip
sudo apt-get install sqlite3
pip install python-swiftclient
pip install python-keystoneclient
apt-get install s3cmd
curl https://rclone.org/install.sh | bash


## Load environment variables:
if [ ! -f .env ]
then
  export $(cat .env | xargs)
fi


## Declare target bucket name for tool experiments:
readonly SWIFT="vinh-swift-experiemnts"
#readonly S3CMD="vinh-s3cmd-experiments"
#readonly RCLONE="vinh-rclone-experiements"


