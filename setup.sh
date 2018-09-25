#!/bin/sh
# Initialise l'environnement de production pour Odoo

echo "Installing Odoo - Enterprise : MDP : 34yRnE@@"
git clone -b 11.0 https://fenuasoftware@github.com/odoo/enterprise.git

echo "Installing fenuasoftware"
git clone -b 11.0 https://heifara@bitbucket.org/fenuasoftware/fenuasoftware.git

echo "Installing fenuasoftware_ee"
git clone -b 11.0 git clone https://heifara@bitbucket.org/fenuasoftware/fenuasoftware_ee.git

echo "Installing notfenuasoftware"
git clone -b 11.0 https://heifara@bitbucket.org/fenuasoftware/notfenuasoftware.git

echo "Installing Acespritech"
git clone -b 11.0 https://heifara@bitbucket.org/fenuasoftware/acespritech.git

echo "Installing 73lines"
git clone -b 11.0 https://heifara@bitbucket.org/fenuasoftware/73lines.git

echo "Installing odoolog"
sudo ln -s /opt/odoo/fenuasoftware/odoolog.sh /usr/local/bin/odoolog

echo "Installing odooalldb"
sudo ln -s /opt/odoo/fenuasoftware/odooall.sh /usr/local/bin/odooall

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
sudo echo "deb http://nightly.odoo.com/11.0/nightly/deb/ ./" >> /etc/apt/sources.list.d/odoo.list
sudo apt-get update && apt-get install odoo

echo "Installing pip"
sudo apt-get install python3-pip python3.5-dev build-essential
sudo pip3 install --upgrade pip

echo "Installing pysftp"
sudo pip3 install pysftp==0.2.8

echo "Installing pysftp"
sudo pip3 install ofxparse==0.14

echo "Installing pyOpenSSL"
sudo pip3 install pyOpenSSL==16.2.0

sudo pip3 install num2words xlwt
sudo pip3 install phonenumbers
sudo pip3 install vobject qrcode
sudo apt install libldap2-dev libsasl2-dev
sudo pip3 install pyldap


