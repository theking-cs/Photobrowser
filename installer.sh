#!/bin/sh

echo "********************************************************"
echo "* Installing PhotoBrowser v1.0 - theking-cs           *"
echo "********************************************************"

PLUGIN_NAME="PhotoBrowser"
PLUGIN_PATH="/usr/lib/enigma2/python/Plugins/Extensions/$PLUGIN_NAME"

rm -rf $PLUGIN_PATH
rm -rf /tmp/PhotoBrowser.zip
rm -rf /tmp/PhotoBrowser-main

echo "> Downloading from GitHub..."
wget --no-check-certificate https://github.com/theking-cs/PhotoBrowser/archive/refs/heads/main.zip -O /tmp/PhotoBrowser.zip

if [ $? -ne 0 ]; then
    echo "Download failed!"
    exit 1
fi

echo "> Extracting..."
unzip -q /tmp/PhotoBrowser.zip -d /tmp/

echo "> Installing plugin..."
mv /tmp/PhotoBrowser-main $PLUGIN_PATH

echo "> Setting permissions..."
chmod -R 755 $PLUGIN_PATH

rm -rf /tmp/PhotoBrowser.zip

echo "********************************************************"
echo "* INSTALLATION COMPLETE - RESTARTING ENIGMA2         *"
echo "********************************************************"

killall -9 enigma2

exit 0
