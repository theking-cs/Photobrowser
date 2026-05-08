#!/bin/sh

# --- CONFIGURACIÓN ---
URL_BASE="https://raw.githubusercontent.com/theking-cs/Photobrowser/main"
PLUGIN_PATH="/usr/lib/enigma2/python/Plugins/Extensions/Photobrowser"

echo "================================================="
echo "   INSTALADOR COMPLETO PHOTOBROWSER v1.1"
echo "================================================="

# 1. CREAR ESTRUCTURA
echo "> Creando carpetas..."
mkdir -p $PLUGIN_PATH/img

# 2. DESCARGAR ARCHIVOS PRINCIPALES
echo "> Descargando archivos base..."
wget -q --no-check-certificate "$URL_BASE/plugin.py" -O "$PLUGIN_PATH/plugin.py"
wget -q --no-check-certificate "$URL_BASE/__init__.py" -O "$PLUGIN_PATH/__init__.py"

# 3. DESCARGAR IMÁGENES
echo "> Descargando recursos visuales..."
wget -q --no-check-certificate "$URL_BASE/img/icono.png" -O "$PLUGIN_PATH/img/icono.png"
wget -q --no-check-certificate "$URL_BASE/img/background.jpg" -O "$PLUGIN_PATH/img/background.jpg"

echo "================================================="
echo "      INSTALACIÓN FINALIZADA"
echo "================================================="

# 4. PREGUNTA DE REINICIO CORREGIDA
echo -e "\n¿Deseas reiniciar Enigma2 ahora? (s/n)"
read confirm

if [ "$confirm" = "s" ] || [ "$confirm" = "S" ]; then
    echo "> Reiniciando interfaz..."
    killall -9 enigma2
else
    echo "> Instalación terminada. Reinicia manualmente para ver el plugin."
fi
