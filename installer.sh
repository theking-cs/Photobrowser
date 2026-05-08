#!/bin/sh

echo ""
echo "==========================================="
echo "   PhotoBrowser Installer v1.0"
echo "   Author: theking-cs"
echo "==========================================="
echo ""

PLUGIN="PhotoBrowser"
VERSION="1.0"
REPO="theking-cs/PhotoBrowser"
BRANCH="main"

TMP="/tmp/$PLUGIN"

# Clean temp
rm -rf $TMP
mkdir -p $TMP

cd /tmp || exit 1

echo "[1/5] Downloading PhotoBrowser v$VERSION ..."

wget --no-check-certificate -O photobrowser.zip https://github.com/$REPO/archive/refs/heads/$BRANCH.zip

if [ $? -ne 0 ]; then
    echo ""
    echo "ERROR: Download failed!"
    exit 1
fi

echo "[2/5] Extracting package..."

unzip -o photobrowser.zip > /dev/null

if [ $? -ne 0 ]; then
    echo ""
    echo "ERROR: Extraction failed!"
    exit 1
fi

echo "[3/5] Installing dependencies..."

opkg update > /dev/null 2>&1

# Python3 Pillow
opkg install python3-pillow > /dev/null 2>&1

# Python2 fallback
opkg install python-pillow > /dev/null 2>&1

echo "[4/5] Installing plugin files..."

cp -r PhotoBrowser-main/usr/* /usr/

chmod -R 755 /usr/lib/enigma2/python/Plugins/Extensions/PhotoBrowser

sync

echo "[5/5] Restarting Enigma2..."

sleep 2

killall -9 enigma2

exit 0
