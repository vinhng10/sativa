#!/bin/bash

## Install packages:
echo "Installing packages ..."
apt-get update
apt-get install python-pip
pip install python-swiftclient
apt-get install s3cmd
curl https://rclone.org/install.sh | bash


