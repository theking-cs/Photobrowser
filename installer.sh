#!/bin/sh

echo "************************************"
echo "* Installing Photobrowser v1.0     *"
echo "************************************"

PLUGIN="Photobrowser"
PLUGIN_PATH="/usr/lib/enigma2/python/Plugins/Extensions/$PLUGIN"

rm -rf $PLUGIN_PATH
rm -rf /tmp/Photobrowser.zip
rm -rf /tmp/Photobrowser-main

cd /tmp || exit 1

echo "> Downloading..."
wget --no-check-certificate https://github.com/theking-cs/PhotoBrowser/archive/refs/heads/main.zip -O Photobrowser.zip

echo "> Extracting..."
unzip -q Photobrowser.zip

EXTRACTED=$(ls /tmp | grep -i photobrowser-main)

echo "> Installing $EXTRACTED"
mv /tmp/$EXTRACTED $PLUGIN_PATH

chmod -R 755 $PLUGIN_PATH

rm -rf Photobrowser.zip

echo "************************************"
echo "* INSTALL DONE - RESTARTING ENIGMA2*"
echo "************************************"

killall -9 enigma2

exit 0
