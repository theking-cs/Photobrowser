#!/bin/sh

# --- CONFIGURACIÓN ---
URL_BASE="https://raw.githubusercontent.com/theking-cs/Photobrowser/main"
PLUGIN_PATH="/usr/lib/enigma2/python/Plugins/Extensions/Photobrowser"

echo "================================================="
echo "   INSTALADOR DE PHOTOBROWSER v1.1"
echo "================================================="

# 1. CREAR CARPETA
echo "> Preparando directorio en $PLUGIN_PATH..."
mkdir -p $PLUGIN_PATH

# 2. LISTA DE ARCHIVOS A DESCARGAR
# Añadimos plugin.png a la lista
archivos="plugin.py __init__.py plugin.png"

for file in $archivos; do
    echo "> Descargando $file..."
    wget -q --no-check-certificate "$URL_BASE/$file" -O "$PLUGIN_PATH/$file"
done

# 3. VERIFICACIÓN Y PERMISOS
chmod -R 755 $PLUGIN_PATH

if [ -f "$PLUGIN_PATH/plugin.png" ]; then
    echo "> Icono plugin.png instalado correctamente."
else
    echo "> ADVERTENCIA: No se pudo descargar plugin.png (revisa si el nombre en GitHub es igual)."
fi

echo "================================================="
echo "      INSTALACIÓN FINALIZADA"
echo "================================================="

# 4. REINICIO
echo ""
read -p "¿Reiniciar Enigma2 ahora? (s/n): " confirm
if [ "$confirm" = "s" ] || [ "$confirm" = "S" ]; then
    killall -9 enigma2
fi
