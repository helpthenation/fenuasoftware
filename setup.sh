#!/bin/sh
# Initialise l'environnement de production pour Odoo

echo "Installing Gdebi"
sudo apt-get install gdebi

echo "Installing wkhtmltopdf"
wget -O wkhtmltox.deb "https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.1/wkhtmltox-0.12.1_linux-trusty-amd64.deb"
sudo gdebi wkhtmltox.deb
sudo rm wkhtmltox.deb
sudo ln -s /usr/local/bin/wkhtmltopdf /usr/bin/Wkhtmltopdf

echo "Installing PostgreSQL"
sudo apt-get install postgresql -y

echo "Installing Odoo - Community"
sudo wget -O - https://nightly.odoo.com/odoo.key | apt-key add -
sudo echo "deb http://nightly.odoo.com/10.0/nightly/deb/ ./" >> /etc/apt/sources.list.d/odoo.list
sudo apt-get update && apt-get install odoo

echo "Installing pip"
sudo apt-get install python-pip python-dev build-essential
sudo pip install --upgrade pip

echo "Installing pysftp"
sudo pip install pysftp==0.2.8

echo "Installing pysftp"
sudo pip install ofxparse==0.14

echo "Installing Odoo - Enterprise"
git clone -b 10.0 https://Heifara@github.com/odoo/enterprise.git

echo "Installing fenuasoftware"
git clone -b 10.0 https://heifara@bitbucket.org/fenuasoftware/fenuasoftware.git

echo "Installing notfenuasoftware"
git clone -b 10.0 https://heifara@bitbucket.org/fenuasoftware/notfenuasoftware.git

echo "Installing odoolog"
chmod 777 ./fenuasoftware/odoolog.sh
sudo ln -s /opt/odoo/fenuasoftware/odoolog.sh /usr/local/bin/odoolog

echo "Installing odooalldb"
chmod 777 ./fenuasoftware/odooalldb.sh
sudo ln -s /opt/odoo/fenuasoftware/odooall.sh /usr/local/bin/odooall

echo "Installing odooupgrade"
chmod 777 ./fenuasoftware/odooupgrade.sh
sudo ln -s /opt/odoo/fenuasoftware/odooupgrade.sh /usr/local/bin/odooupgrade

