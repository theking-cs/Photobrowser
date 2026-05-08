#!/bin/sh

# --- CONFIGURACIÓN ---
URL_BASE="https://raw.githubusercontent.com/theking-cs/Photobrowser/main"
PLUGIN_PATH="/usr/lib/enigma2/python/Plugins/Extensions/Photobrowser"

echo "================================================="
echo "   INSTALADOR DE PHOTOBROWSER v1.1"
echo "================================================="

# 1. CREAR CARPETA
echo "> Preparando carpeta del plugin..."
mkdir -p $PLUGIN_PATH

# 2. DESCARGAR ARCHIVOS UNO A UNO
# Añadimos plugin.png a la lista
echo "> Descargando componentes..."

files="plugin.py __init__.py plugin.png"

for file in $files; do
    echo "  Descargando $file..."
    wget -q --no-check-certificate "$URL_BASE/$file" -O "$PLUGIN_PATH/$file"
done

# 3. PERMISOS
chmod -R 755 $PLUGIN_PATH

echo "================================================="
echo "      INSTALACIÓN FINALIZADA CON ÉXITO"
echo "================================================="

# 4. REINICIO DEL GUI
echo ""
read -p "¿Deseas reiniciar Enigma2 para ver el icono? (s/n): " confirm

if [ "$confirm" = "s" ] || [ "$confirm" = "S" ]; then
    echo "> Reiniciando interfaz..."
    killall -9 enigma2
else
    echo "> Instalación terminada. Recuerda reiniciar más tarde."
fi
