@echo off
REM ---- build_exe.bat ----
cd /d "%~dp0"

set PY=AnimeDownloadS.py
set EXE=dist\AnimeDownloadS.exe
set PYTHON=%~dp0venv\Scripts\python.exe
set ICON=%~dp0munchi.ico
set MAPEOS=%~dp0mapeos.json
set ENV=%~dp0.env

REM Si no existe el exe, reconstruir
if not exist "%EXE%" goto build

REM Obtener timestamps
for %%I in ("%PY%") do set PYTIME=%%~tI
for %%I in ("%MAPEOS%") do set MAPEOSTIME=%%~tI
for %%I in ("%ENV%") do set ENVTIME=%%~tI
for %%I in ("%ICON%") do set ICONTIME=%%~tI
for %%I in ("%EXE%") do set EXETIME=%%~tI

REM Comparar timestamps (recompilar si el .py, mapeos.json, .env o icono.ico es más reciente)
if "%PYTIME%" GTR "%EXETIME%" goto build
if "%MAPEOSTIME%" GTR "%EXETIME%" goto build
if "%ENVTIME%" GTR "%EXETIME%" goto build
if "%ICONTIME%" GTR "%EXETIME%" goto build
goto end

:build
echo [Build] Detectado cambio en %PY%, %MAPEOS%, %ENV%, o %ICON%, recompilando...
if not exist "%ICON%" (
    echo ERROR: No se encontró el archivo de ícono %ICON%
    pause
    exit /b 1
)
if not exist "%MAPEOS%" (
    echo ERROR: No se encontró el archivo mapeos.json
    pause
    exit /b 1
)
if not exist "%ENV%" (
    echo ERROR: No se encontró el archivo .env
    pause
    exit /b 1
)
echo [Debug] Usando icono: %ICON%
echo [Debug] Incluyendo archivos: %MAPEOS%, %ENV%, %ICON%
"%PYTHON%" -m PyInstaller ^
    --onefile ^
    --windowed ^
    --add-data "%~dp0mapeos.json;." ^
    --add-data "%~dp0.env;." ^
    --add-data "%~dp0munchi.ico;." ^
    --icon "%ICON%" ^
    --distpath "%~dp0dist" ^
    --workpath "%~dp0build" ^
    --name AnimeDownloadS ^
    "%~dp0%PY%"
if errorlevel 1 (
    echo ERROR en compilación. Revisa el archivo de ícono o los parámetros de PyInstaller.
    pause
    exit /b 1
)
echo [Build] Compilación completada.

:end