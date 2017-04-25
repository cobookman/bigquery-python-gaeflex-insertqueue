#!/bin/bash
sudo apt-get install python3-pip
sudo pip3 install Flask --upgrade
sudo pip3 install google-cloud-bigquery --upgrade
gcloud auth application-default
