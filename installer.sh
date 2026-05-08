#!/bin/sh

echo ""
echo "==========================================="
echo "   PhotoBrowser Installer v1.0"
echo "   Author: theking-cs"
echo "==========================================="
echo ""

PLUGIN="PhotoBrowser"
REPO="theking-cs/PhotoBrowser"
BRANCH="main"

TMP="/tmp/$PLUGIN"

rm -rf $TMP
mkdir -p $TMP

cd /tmp || exit 1

echo "[1/6] Downloading package..."

wget --no-check-certificate -O photobrowser.zip https://github.com/$REPO/archive/refs/heads/$BRANCH.zip

if [ $? -ne 0 ]; then
    echo "ERROR: Download failed"
    exit 1
fi

echo "[2/6] Checking unzip..."

if ! command -v unzip >/dev/null 2>&1; then
    echo "Installing unzip..."
    opkg update
    opkg install unzip
fi

echo "[3/6] Extracting..."

unzip -o photobrowser.zip

if [ $? -ne 0 ]; then
    echo "ERROR: unzip failed"
    exit 1
fi

echo "[4/6] Installing dependencies..."

opkg update

opkg install python3-pillow
opkg install python-pillow

echo "[5/6] Installing plugin..."

if [ -d PhotoBrowser-main ]; then
    cp -r PhotoBrowser-main/usr/* /usr/
else
    echo "ERROR: Folder PhotoBrowser-main not found"
    ls -l
    exit 1
fi

chmod -R 755 /usr/lib/enigma2/python/Plugins/Extensions/PhotoBrowser

sync

echo "[6/6] Restart Enigma2..."

sleep 2
killall -9 enigma2

echo ""
echo "Installation completed!"
exit 0
