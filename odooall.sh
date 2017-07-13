#!/bin/sh
USER=odoo
DAEMON=/usr/bin/odoo
CONFIG=/etc/odoo/odoo.conf
sudo start-stop-daemon --start --chuid $USER:$USER --exec $DAEMON -- --config $CONFIG $@
