#! /bin/bash

######################CHECK FOR ROOT########################
if [ "$(id -u)" != "0" ]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

INSTALL_DIR=$(readlink /usr/bin/gbsgrid)
INSTALL_DIR=${INSTALL_DIR%/gbsgrid/gbsgrid.sh}
rm /usr/bin/gbsgrid
rm /usr/share/applications/gbsgrid.desktop
rm -rf $INSTALL_DIR/gbsgrid
./INSTALL.sh $INSTALL_DIR

