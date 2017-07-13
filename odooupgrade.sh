#!/bin/sh

echo "Updating repos ..."
sudo apt-get update

echo "Upgrading ..."
sudo apt-get upgrade

echo "Pulling odoo/enterprise ..."
cd /home/vittoria/enterprise
git pull

echo "Pulling vittoriaconseil/vittodoo"
cd /home/vittoria/vittodoo
git pull

echo "Restarting odoo server"
sudo service odoo restart