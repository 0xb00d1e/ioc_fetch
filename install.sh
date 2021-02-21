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

adduser --quiet --disabled-password --shell /bin/bash --home /home/ioc_fetch --gecos "User" ioc_fetch

sudo -i -u postgres psql -c "create database ioc_fetch;"
sudo -i -u postgres psql -c "create database ioc_fetch_test;"
sudo -i -u postgres psql -c "create database ioc_fetch_dev;"
sudo -i -u postgres psql -c "create user ioc_fetch with encrypted password '12345';"
sudo -i -u postgres psql -c "create user ioc_fetch_test with encrypted password '12345';"
sudo -i -u postgres psql -c "create user ioc_fetch_dev with encrypted password '12345';"
sudo -i -u postgres psql -c "grant all privileges on database ioc_fetch to ioc_fetch;"
sudo -i -u postgres psql -c "grant all privileges on database ioc_fetch_test to ioc_fetch_test;"
sudo -i -u postgres psql -c "grant all privileges on database ioc_fetch_dev to ioc_fetch_dev;"

cp -r ../ioc_fetch/ /home/ioc_fetch/ioc_fetch/
chown -R ioc_fetch:ioc_fetch /home/ioc_fetch/ioc_fetch/
cp site_conf/ioc_fetch.conf /etc/apache2/sites-available/ioc_fetch.conf
a2ensite ioc_fetch.conf
a2dissite 000-default.conf

echo '<Directory /home/ioc_fetch/ioc_fetch/>' >> /etc/apache2/apache2.conf
echo '    Options Indexes FollowSymLinks' >> /etc/apache2/apache2.conf
echo '    AllowOverride None' >> /etc/apache2/apache2.conf
echo '    Require all granted' >> /etc/apache2/apache2.conf
echo '</Directory>' >> /etc/apache2/apache2.conf

service apache2 restart
sudo -i -u ioc_fetch virtualenv -p python3 /home/ioc_fetch/ioc_fetch/venv/

usermod -aG www-data ioc_fetch
cd /home/ioc_fetch/ioc_fetch/
chmod g+s logs/
setfacl -d -m o::rw logs/
chmod 777 logs/
