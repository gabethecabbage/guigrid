#! /bin/bash

######################CHECK FOR ROOT########################
if [ "$(id -u)" != "0" ]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

INSTALL_DIR=/opt
mkdir $INSTALL_DIR/gbsgrid
cp gbsgrid*	$INSTALL_DIR/gbsgrid/

mkdir $INSTALL_DIR/gbsgrid/icons
cp icons/*	$INSTALL_DIR/gbsgrid/icons/
echo Icon=$INSTALL_DIR/gbsgrid/icons/gbsgrid-icon.png >> $INSTALL_DIR/gbsgrid/gbsgrid.desktop
ln -s $INSTALL_DIR/gbsgrid/gbsgrid.desktop /usr/share/applications/gbsgrid.desktop

echo '#! /bin/bash' >> $INSTALL_DIR/gbsgrid/gbsgrid.sh
echo cd $INSTALL_DIR/gbsgrid >> $INSTALL_DIR/gbsgrid/gbsgrid.sh
echo python gbsgrid_front.py >> $INSTALL_DIR/gbsgrid/gbsgrid.sh
ln -s $INSTALL_DIR/gbsgrid/gbsgrid.sh /usr/bin/gbsgrid
chmod +x /usr/bin/gbsgrid

echo "Install finished to $INSTALL_DIR/gbsgrid"
echo "Ensure PyQt4 and sbgrid are installed."
echo "(e.g. RHEL:'yum install PyQt4' or DEB:'apt-get install python-qt4')"
