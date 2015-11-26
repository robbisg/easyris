#!/bin/bash
sss=$(uname -m)
if [ "${sss}" = "armv7l" ] ;
  then
    echo "LC_ALL=\"en_GB.UTF-8\"" >> /etc/environment
    export LC_ALL="en_GB.UTF-8"
  else
    echo "LC_ALL=\"en_US.UTF-8\"" >> /etc/environment
    export LC_ALL="en_US.UTF-8"
fi

apt-get -y update
apt-get -y upgrade
apt-get -y dist-upgrade

echo "Insert today date: DD MMM YYYY HH:MM"
read today
if [ "${today}X" = "X" ] ;
  then
    echo No date. Quit.
    exit 1
  else
    date -s "${today}"
    date
  fi

apt-get -y install apache2 apache2-mpm-prefork apache2-prefork-dev python-dev

apt-get -y install python-pip
pip install flask

apt-get -y install p7zip-full
#wget http://facat.github.io/mongodb-2.6.4-arm.7z

mkdir -p /data
mkdir -p /data/db
mkdir -p /data/log
useradd mongo
usermod --password raspberry mongo
chown mongo:mongo /data/db
chown mongo:mongo /data/log

hm=$(pwd)
sss=$(uname -m)
if [ "${sss}" = "armv7l" ] ;
  then
    fin=mongodb-2.6.4-arm.7z
    wfin=https://www.dropbox.com/s/o6451xdrya4ntt4/$fin
  else
    fin=mongodb-linux-x86_64-2.6.4.7z
    wfin=https://www.dropbox.com/s/y6kxz9d698w9yyj/$fin
fi
wget $wfin
cd /usr/bin
7z e ${hm}/$fin
rm ${hm}/$fin
chmod 755 bson* mongo*
#chown mongo:mongo /usr/bin/mongo*
cd ${hm}

##########################################
# change bash.bashrc add "export LC_ALL=C"
##########################################

# Eventualmente aggiungiamo solo la riga che ci serve.
# cp bash.bashrc /etc/

cp ${hm}/mongod.conf /etc/
cp ${hm}/mongod /etc/init.d/
chmod 755 /etc/init.d/mongod

#if [ "${sss}" = "armv7l" ] ;
#  then
#    cp ${hm}/mongod /etc/init.d/
#    chmod 755 /etc/init.d/mongod
#  else
#    cp /usr/bin/mongod /etc/init.d/
#  fi

service mongod start

pip install mod_wsgi
pip install pymongo Flask-PyMongo
pip install MongoAlchemy Flask-MongoAlchemy
pip install codicefiscale

apt-get -y install libapache2-mod-wsgi

#################################
#Test check link Apache-Flask:
################################
sss=$(uname -m)
if [ "${sss}" = "armv7l" ] ;
  then
    uuu=pi
  else
    uuu=vagrant
  fi

cp ${hm}/project.py /home/${uuu}/

chown ${uuu}:${uuu} /home/${uuu}/project.py

mkdir -p /var/www/hellopy/

cat application.wsgi | sed "s/\/home\/pi\//\/home\/"${uuu}"\//g" > /var/www/hellopy/application.wsgi

chown -R www-data:www-data /var/www/hellopy/

##########################################

cd /etc/apache2/sites-available/
mv default default.orig
cat default.orig | sed 's/<\/VirtualHost>//g' > default
cat ${hm}/to_be_added_to_default | sed "s/=pi/="${uuu}"/g" >> default
echo "</VirtualHost>" >> default

service apache2 restart
