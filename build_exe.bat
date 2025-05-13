@echo off
REM ---- build_exe.bat ----
cd /d "%~dp0"

set PY=AnimeDownloadS.py
set EXE=dist\AnimeDownloadS.exe
set PYTHON=%~dp0venv\Scripts\python.exe

REM Si no existe el exe, o el .py es más reciente, reconstruir
if not exist "%EXE%" goto build

for %%I in ("%PY%") do set PYTIME=%%~tI
for %%I in ("%EXE%") do set EXETIME=%%~tI

REM Comparar timestamps (string compare funciona bien para fechas)
if "%PYTIME%" GTR "%EXETIME%" goto build
goto end

:build
echo [Build] Detectado cambio en %PY%, recompilando...
"%PYTHON%" -m PyInstaller ^
    --onefile ^
    --windowed ^
    --add-data "%~dp0mapeos.json;." ^
    --add-data "%~dp0.env;." ^
    --distpath "%~dp0dist" ^
    --workpath "%~dp0build" ^
    --name AnimeDownloadS ^
    "%~dp0%PY%"
if errorlevel 1 (
    echo ERROR en compilación.
    pause
    exit /b 1
)
echo [Build] Compilación completada.

:end