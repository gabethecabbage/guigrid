#! /bin/bash

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

echo Install finished to $INSTALL_DIR/gbsgrid
