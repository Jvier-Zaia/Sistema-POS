@echo off
color 0b
title Instalador - Sistema de Registro de Ventas

echo ========================================================
echo   Instalando Sistema de Registro de Ventas...
echo ========================================================
echo.

set "INSTALL_DIR=%LOCALAPPDATA%\SistemaVentas"

echo [1/3] Creando directorio de instalacion en %INSTALL_DIR%...
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"
if not exist "%INSTALL_DIR%\tickets" mkdir "%INSTALL_DIR%\tickets"

echo [2/3] Copiando archivos del sistema...
copy /Y "main.exe" "%INSTALL_DIR%\SistemaVentas.exe" >nul
copy /Y "caja.ico" "%INSTALL_DIR%\caja.ico" >nul

echo [3/3] Creando acceso directo en el Escritorio...
set "VBS_SCRIPT=%TEMP%\CreateShortcut.vbs"
echo Set oWS = WScript.CreateObject("WScript.Shell") > "%VBS_SCRIPT%"
echo sLinkFile = "%USERPROFILE%\Desktop\Sistema Ventas.lnk" >> "%VBS_SCRIPT%"
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> "%VBS_SCRIPT%"
echo oLink.TargetPath = "%INSTALL_DIR%\SistemaVentas.exe" >> "%VBS_SCRIPT%"
echo oLink.IconLocation = "%INSTALL_DIR%\caja.ico" >> "%VBS_SCRIPT%"
echo oLink.WorkingDirectory = "%INSTALL_DIR%" >> "%VBS_SCRIPT%"
echo oLink.Save >> "%VBS_SCRIPT%"

cscript /nologo "%VBS_SCRIPT%"
del "%VBS_SCRIPT%"

echo.
echo ========================================================
echo   Instalacion Completada con Exito!
echo   Ya puedes abrir "Sistema Ventas" desde tu Escritorio.
echo ========================================================
timeout /t 5 >nul
