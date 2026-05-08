#!/bin/sh

# --- CONFIGURACIÓN ---
URL_BASE="https://raw.githubusercontent.com/theking-cs/Photobrowser/main"
PLUGIN_PATH="/usr/lib/enigma2/python/Plugins/Extensions/Photobrowser"

echo "================================================="
echo "   INSTALADOR COMPLETO PHOTOBROWSER v1.0"
echo "================================================="

# 1. PREPARAR CARPETAS
echo "> Creando estructura de carpetas..."
mkdir -p $PLUGIN_PATH
mkdir -p $PLUGIN_PATH/img

# 2. LISTA DE ARCHIVOS A DESCARGAR
# Añade aquí todos los archivos que vayas creando en tu GitHub
FILES="plugin.py __init__.py"
IMAGES="img/icono.png img/background.jpg"

# 3. DESCARGA DE CÓDIGO
for file in $FILES; do
    echo "> Descargando $file..."
    wget -q --no-check-certificate "$URL_BASE/$file" -O "$PLUGIN_PATH/$file"
done

# 4. DESCARGA DE IMÁGENES (Si las tienes en carpeta img)
for img in $IMAGES; do
    echo "> Descargando imagen $img..."
    wget -q --no-check-certificate "$URL_BASE/$img" -O "$PLUGIN_PATH/$img"
done

# 5. PERMISOS
chmod -R 755 $PLUGIN_PATH

echo "================================================="
echo "      INSTALACIÓN FINALIZADA"
echo "================================================="

# 6. REINICIO
read -p "¿Deseas reiniciar Enigma2 ahora? (s/n): " confirm
if [ "$confirm" = "s" ] || [ "$confirm" = "S" ]; then
    killall -9 enigma2
fi
