#!/bin/sh
echo -e "\n--- Installing wkhtmltopdf --"
sudo apt-get install gdebi
wget -O wkhtmltox.deb "https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.1/wkhtmltox-0.12.1_linux-trusty-amd64.deb"
sudo gdebi wkhtmltox.deb
sudo rm wkhtmltox.deb
sudo ln -s /usr/local/bin/wkhtmltopdf /usr/bin/Wkhtmltopdf

echo -e "\n--- Installing PostgreSQL --"
sudo apt-get install postgresql -y

echo -e "\n--- Installing Python 3 + pip3 --"
sudo apt-get install python3 python3-pip -y

echo -e "\n---- Install tool packages ----"
sudo apt-get install wget git bzr python-pip gdebi-core -y

echo -e "\n---- Install python packages ----"
sudo apt-get install libxml2-dev libxslt1-dev zlib1g-dev -y
sudo apt-get install libsasl2-dev libldap2-dev libssl-dev -y
sudo apt-get install python-pypdf2 python-dateutil python-feedparser python-ldap python-libxslt1 python-lxml python-mako python-openid python-psycopg2 python-pybabel python-pychart python-pydot python-pyparsing python-reportlab python-simplejson python-tz python-vatnumber python-vobject python-webdav python-werkzeug python-xlwt python-yaml python-zsi python-docutils python-psutil python-mock python-unittest2 python-jinja2 python-pypdf python-decorator python-requests python-passlib python-pil -y
sudo pip3 install pypdf2 Babel passlib Werkzeug decorator python-dateutil pyyaml psycopg2 psutil html2text docutils lxml pillow reportlab ninja2 requests gdata XlsxWriter vobject python-openid pyparsing pydot mock mako Jinja2 ebaysdk feedparser xlwt psycogreen suds-jurko pytz pyusb greenlet xlrd chardet libsass

echo -e "\n---- Install python libraries ----"
# This is for compatibility with Ubuntu 16.04. Will work on 14.04, 15.04 and 16.04
sudo apt-get install python3-suds

echo -e "\n--- Install other required packages ----"
sudo apt-get install node-clean-css -y
sudo apt-get install node-less -y
sudo apt-get install python-gevent -y

echo -e "\n--- Upgrade pip ----"
sudo pip3 install --upgrade pip

echo -e "\n--- Install more python packages ----"
sudo pip3 install ofxparse pysftp num2words xlwt phonenumbers vobject qrcode pyldap

echo -e "\n---- Installing Odoo - Community ----"
sudo wget -O - https://nightly.odoo.com/odoo.key | apt-key add -
sudo echo "deb http://nightly.odoo.com/12.0/nightly/deb/ ./" >> /etc/apt/sources.list.d/odoo.list
sudo apt-get update && apt-get install odoo

echo "Installing Odoo - Enterprise : MDP : 34yRnE@@"
#git clone -b 12.0 https://fenuasoftware@github.com/odoo/enterprise.git

echo "Installing fenuasoftware"
#it clone -b 12.0 https://heifara@bitbucket.org/fenuasoftware/fenuasoftware.git

echo "Installing fenuasoftware_ee"
#git clone -b 12.0 git clone https://heifara@bitbucket.org/fenuasoftware/fenuasoftware_ee.git

echo "Installing notfenuasoftware"
#git clone -b 12.0 https://heifara@bitbucket.org/fenuasoftware/notfenuasoftware.git

echo "Installing Acespritech"
#git clone -b 12.0 https://heifara@bitbucket.org/fenuasoftware/acespritech.git

echo "Installing 73lines"
#git clone -b 12.0 https://heifara@bitbucket.org/fenuasoftware/73lines.git

echo "Installing odoolog"
#sudo ln -s /opt/odoo/addons/fenuasoftware/odoolog.sh /usr/local/bin/odoolog

echo "Installing odooalldb"
#sudo ln -s /opt/odoo/addons/fenuasoftware/odooall.sh /usr/local/bin/odooall
