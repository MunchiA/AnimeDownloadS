# AnimeDownloadS

Interfaz Tkinter para descargar y lanzar scripts remotos de anime/donghua en un servidor Ubuntu.

> ⚠️ **Importante:** Este programa está creado para Windows.  
> Hace falta tener previamente los scripts creados en el servidor para que se ejecuten correctamente.

## Estructura del repositorio

```
AnimeDownloadS/              ← raíz del repo
│
├── .gitignore               ← archivos a ignorar
├── README.md                ← descripción e instrucciones
├── requirements.txt         ← dependencias
├── .env.example             ← plantilla de variables de entorno
├── mapeos.example.json      ← plantilla de rutas de mapeo
│
├── AnimeDownloadS.py        ← script principal con la GUI
├── mapeos.json              ← mapeo de rutas a nombres de scripts
│
└── build_exe.bat            ← script Windows para compilar el .exe
```

## Variables de entorno

Copia el archivo de ejemplo y configúralo con tus valores:

```bash
cp .env.example .env
# Edita .env con tus datos reales
```

El archivo `.env` debe incluir:

```dotenv
HOST=DIRECCION_IP
PORT=PUERTO
USER=USUARIO
KEY_PATH=RUTA DE LA CLAVE
REMOTE_TXT_PATH=RUTA DEL ARCHIVO EN EL SERVIDOR
LOCAL_TXT_PATH=ARCHIVO LOCAL
```

## Instalación

1. Clona el repositorio:

```bash
git clone <repo-url>
cd AnimeDownloadS
````

2. Crea y activa el entorno virtual:

```bash
python -m venv venv
venv\Scripts\activate
````

3. Instala dependencias:

```bash
pip install -r requirements.txt
````

4. Revisión de archivos:

> [!IMPORTANT]
> Hay que asegurarse de que mapeos.json y .env estén en el directorio raíz del proyecto.

## Compilación del ejecutable

Para generar un ejecutable autónomo (`AnimeDownloadS.exe`) que incluya `mapeos.json` y `.env`:

```powershell
.\build_exe.bat
```

El script `build_exe.bat` usa PyInstaller para compilar `AnimeDownloadS.py` en `dist\AnimeDownloadS.exe`, incluyendo `mapeos.json` y `.env`. El ejecutable verifica automáticamente si necesita recompilarse si `AnimeDownloadS.py` es más reciente.

### Notas
- Asegúrate de que `mapeos.json` y `.env` existan en el directorio del proyecto antes de compilar.
- El ejecutable no incluye la clave privada SSH especificada en `KEY_PATH`. Los usuarios deben proporcionar su propia clave y configurar `KEY_PATH` en `.env`.

## Uso

### En desarrollo (requiere Python)
Ejecuta el script directamente:

```bash
python AnimeDownloadS.py
```