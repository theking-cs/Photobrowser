#!/bin/sh

# --- CONFIGURACIÓN ---
URL_BASE="https://raw.githubusercontent.com/theking-cs/Photobrowser/main"
PLUGIN_PATH="/usr/lib/enigma2/python/Plugins/Extensions/Photobrowser"

echo "================================================="
echo "   INSTALADOR DE PHOTOBROWSER v1.0"
echo "================================================="

# 1. CREAR CARPETAS
echo "> Creando directorios..."
mkdir -p $PLUGIN_PATH

# 2. DESCARGAR ARCHIVOS
# Nota: Asegúrate de que los nombres coincidan exactamente con tu GitHub
echo "> Descargando archivos del plugin..."

files="plugin.py __init__.py"

for file in $files; do
    echo "  Descargando $file..."
    wget -q --no-check-certificate "$URL_BASE/$file" -O "$PLUGIN_PATH/$file"
done

# 3. PERMISOS
chmod -R 755 $PLUGIN_PATH

echo "================================================="
echo "      INSTALACIÓN FINALIZADA"
echo "================================================="

# 4. REINICIO DEL GUI
echo ""
read -p "¿Deseas reiniciar Enigma2 para activar Photobrowser? (s/n): " confirm

if [ "$confirm" = "s" ] || [ "$confirm" = "S" ]; then
    echo "> Reiniciando..."
    killall -9 enigma2
else
    echo "> Instalación terminada. Reinicia manualmente cuando desees."
fi
