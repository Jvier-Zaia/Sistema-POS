@echo off
echo Compilando ejecutable con PyInstaller...
pyinstaller --noconfirm --onefile --windowed --icon=caja.ico main.py

echo Firmando aplicacion...
powershell -ExecutionPolicy Bypass -File sign_app.ps1

echo Empaquetando ZIP Final...
python empaquetar.py

echo TODO COMPLETADO!
