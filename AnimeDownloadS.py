import tkinter as tk
from tkinter import messagebox, ttk
import paramiko
import json
import os
import sys
from dotenv import load_dotenv

# Función para obtener la ruta correcta de archivos empaquetados
def resource_path(relative_path):
    """Obtiene la ruta absoluta del archivo, funciona para desarrollo y ejecutable."""
    try:
        # Si está empaquetado, usa el directorio temporal del .exe
        base_path = sys._MEIPASS if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base_path, relative_path)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo resolver la ruta de {relative_path}: {e}")
        raise

# Carga el .env que está en la misma carpeta
try:
    load_dotenv(resource_path(".env"))
except Exception as e:
    messagebox.showerror("Error", f"No se pudo cargar .env: {e}")
    raise

# --- CONFIGURACIÓN DEL SERVIDOR ---
HOST            = os.getenv("HOST")
PORT            = int(os.getenv("PORT", 22))
USER            = os.getenv("USER")
KEY_PATH        = os.getenv("KEY_PATH")
REMOTE_TXT_PATH = os.getenv("REMOTE_TXT_PATH")
LOCAL_TXT_PATH  = os.getenv("LOCAL_TXT_PATH", "scripts.txt")

# --- MAPEOS DE RUTAS A NOMBRES ---
mapeos_path = resource_path("mapeos.json")

try:
    with open(mapeos_path, "r", encoding="utf-8") as f:
        RUTAS_NOMBRES = json.load(f)
except FileNotFoundError as e:
    messagebox.showerror("Error", f"No se encontró mapeos.json: {e}")
    raise
except Exception as e:
    messagebox.showerror("Error", f"Error al leer mapeos.json: {e}")
    raise

# --- FUNCIONES ---
def descargar_scripts_txt():
    try:
        key = paramiko.RSAKey.from_private_key_file(KEY_PATH)

        transport = paramiko.Transport((HOST, PORT))
        transport.connect(username=USER, pkey=key)

        sftp = paramiko.SFTPClient.from_transport(transport)
        sftp.get(REMOTE_TXT_PATH, LOCAL_TXT_PATH)
        sftp.close()
        transport.close()

    except Exception as e:
        messagebox.showerror("Error al actualizar", f"No se pudo descargar scripts.txt\n\n{e}")
        return False
    return True

def leer_scripts_local():
    try:
        with open(LOCAL_TXT_PATH, "r") as archivo:
            rutas = [line.strip() for line in archivo if line.strip()]
        
        # Obtener los nombres desde el diccionario
        nombres_scripts = [
            RUTAS_NOMBRES.get(ruta, os.path.splitext(os.path.basename(ruta))[0].replace('_', ' ').replace('-', ' ').title()) 
            for ruta in rutas
        ]
        
        return rutas, nombres_scripts  # Devuelve tanto las rutas como los nombres
    except FileNotFoundError:
        messagebox.showerror("Error", f"No se encontró '{LOCAL_TXT_PATH}'")
        return [], []

def ejecutar_script(ruta_script):
    if not ruta_script:
        messagebox.showwarning("Selecciona un script", "Por favor, selecciona un script.")
        return

    carpeta = "/".join(ruta_script.split("/")[:-1])
    archivo = ruta_script.split("/")[-1]
    comando = f"cd {carpeta} && python3 {archivo}"

    try:
        key = paramiko.RSAKey.from_private_key_file(KEY_PATH)

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(HOST, port=PORT, username=USER, pkey=key)

        stdin, stdout, stderr = ssh.exec_command(comando)
        salida = stdout.read().decode()
        errores = stderr.read().decode()
        ssh.close()

        resultado = salida if salida else errores
        messagebox.showinfo("Resultado del script", resultado or "Script ejecutado sin salida.")

    except Exception as e:
        messagebox.showerror("Error al ejecutar", str(e))

def actualizar_y_recargar():
    if descargar_scripts_txt():
        cargar_scripts()
        messagebox.showinfo("Actualizado", "Lista de scripts actualizada desde el servidor.")

def cargar_scripts():
    rutas, nombres_scripts = leer_scripts_local()
    if nombres_scripts:
        # Limpiar los botones anteriores (si existían)
        for widget in boton_frame.winfo_children():
            widget.destroy()
        
        # Crear un botón por cada script en una grid de 2 columnas
        for i, (ruta, nombre) in enumerate(zip(rutas, nombres_scripts)):
            row = i // 2
            col = i % 2

            boton = tk.Button(
                boton_frame, text=nombre, width=30, height=2,
                font=('Helvetica', 12, 'bold'), bg="#4CAF50", fg="white",
                relief="raised", bd=2, command=lambda ruta=ruta: ejecutar_script(ruta)
            )

            # Si es el último botón y el número total es impar
            if i == len(nombres_scripts) - 1 and len(nombres_scripts) % 2 == 1:
                boton.grid(row=row, column=0, columnspan=2, padx=20, pady=10, sticky="n")
            else:
                boton.grid(row=row, column=col, padx=20, pady=10, sticky="nsew")

            boton_frame.grid_columnconfigure(0, weight=1)
            boton_frame.grid_columnconfigure(1, weight=1)

# --- INTERFAZ ---
ventana = tk.Tk()
ventana.title("AnimeDownloadS")

# Establecer el ícono de la ventana
icon_path = resource_path("munchi.ico")
if os.path.exists(icon_path):
    try:
        ventana.iconbitmap(icon_path)
    except Exception as e:
        messagebox.showwarning("Advertencia", f"No se pudo cargar el ícono de la ventana desde {icon_path}: {e}")
else:
    messagebox.showwarning("Advertencia", f"El archivo de ícono {icon_path} no se encontró en el entorno empaquetado.")

# --- CENTRAR VENTANA EN PANTALLA ---
ventana.update_idletasks()  # Asegura que winfo_* devuelvan los valores correctos

# Tamaño deseado de la ventana
ancho = 750
alto  = 400

# Resolución de la pantalla
pantalla_ancho  = ventana.winfo_screenwidth()
pantalla_alto   = ventana.winfo_screenheight()

# Coordenadas para que la ventana quede centrada
pos_x = (pantalla_ancho  // 2) - (ancho // 2)
pos_y = (pantalla_alto   // 2) - (alto  // 2)

# Configuramos la geometría con posición
ventana.geometry(f"{ancho}x{alto}+{pos_x}+{pos_y}")

# --- Modo oscuro ---
ventana.config(bg="#2e2e2e")

# Cambiar el color...
titulo = tk.Label(ventana, text="Selecciona un script remoto para ejecutar:", font=("Helvetica", 14, "bold"), bg="#2e2e2e", fg="white")
titulo.pack(pady=20)

# Frame para los botones
boton_frame = tk.Frame(ventana, bg="#2e2e2e")
boton_frame.pack(pady=10, padx=10, fill="both", expand=True)

# Agregar el botón de actualización
tk.Button(ventana, text="Actualizar lista", width=20, height=2, font=('Helvetica', 12), bg="#2196F3", fg="white", relief="raised", command=actualizar_y_recargar).pack(pady=10)

# Carga inicial silenciosa (sin mostrar mensaje de "Actualizado")
if descargar_scripts_txt():
    cargar_scripts()

ventana.mainloop()