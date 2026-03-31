import os
import subprocess
import time

def run_fdroid(config_file):
    if not os.path.exists(config_file):
        print(f"Saltando {config_file}: No existe el archivo.")
        return

    print(f"--- Procesando con: {config_file} ---")
    
    # Si ya existe un config.yml, lo borramos para que no choque
    if os.path.exists("config.yml"):
        os.remove("config.yml")
        
    # Renombramos el archivo al nombre que fdroid espera
    os.rename(config_file, "config.yml")
    
    try:
        # Ejecutamos el update
        subprocess.run(["fdroid", "update", "-c", "--clean"], check=True)
    finally:
        # Siempre regresamos el archivo a su nombre original
        if os.path.exists("config.yml"):
            os.rename("config.yml", config_file)

# 1. Procesar Oficial (Asegúrate que el archivo se llame así)
run_fdroid("config_oficial.yml")

# 2. Procesar Pruebas
run_fdroid("config_pruebas.yml")

# 3. Subir a GitHub
print("--- Subiendo a GitHub ---")
try:
    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", "Update automatico Oficial y Pruebas"], check=True)
    subprocess.run(["git", "push", "origin", "main"], check=True)
    print("¡Todo listo y en internet!")
except Exception as e:
    print(f"Error al subir a Git: {e}")