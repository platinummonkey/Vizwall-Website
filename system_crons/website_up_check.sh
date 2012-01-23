#!/bin/bash

WC="`wget -q -O - http://vizlab.utsa.edu/ | grep -c -i visualization`"

if [ WC == 0 ]
then
  /etc/init.d/apache2 restart &> /dev/null
  echo -e "restarting webserver at `date`\n" >> /root/webserver_restarts.log
fi
