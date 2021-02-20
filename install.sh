#!/bin/bash


if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

apt update
apt install -y virtualenv
apt install -y redis
apt install -y apache2
apt install -y libapache2-mod-wsgi-py3
apt install -y postgresql-10
apt install -y postgresql-server-dev-10
apt install -y python3-dev
apt install -y build-essential
apt install -y linux-headers-$(uname -r)

sudo -i -u postgres psql -c "create database ioc_fetch;"
sudo -i -u postgres psql -c "create database ioc_fetch_test;"
sudo -i -u postgres psql -c "create database ioc_fetch_dev;"
sudo -i -u postgres psql -c "create user ioc_fetch with encrypted password '12345';"
sudo -i -u postgres psql -c "create user ioc_fetch_test with encrypted password '12345';"
sudo -i -u postgres psql -c "create user ioc_fetch_dev with encrypted password '12345';"
sudo -i -u postgres psql -c "grant all privileges on database ioc_fetch to ioc_fetch;"
sudo -i -u postgres psql -c "grant all privileges on database ioc_fetch_test to ioc_fetch_test;"
sudo -i -u postgres psql -c "grant all privileges on database ioc_fetch_dev to ioc_fetch_dev;"