import os
import subprocess

def run_fdroid(config_file):
    if not os.path.exists(config_file):
        print(f"--- Saltando {config_file}: No existe el archivo ---")
        return

    print(f"--- Procesando con: {config_file} ---")
    
    # Limpieza previa por si acaso
    if os.path.exists("config.yml"):
        os.remove("config.yml")
        
    # Renombrar para que fdroid lo reconozca
    os.rename(config_file, "config.yml")
    
    try:
        # Ejecutamos el update (añadimos shell=True para Windows)
        subprocess.run("fdroid update -c --clean", shell=True, check=True)
    except Exception as e:
        print(f"Error en fdroid update: {e}")
    finally:
        # ESTO ES LO IMPORTANTE: Siempre regresa el nombre original
        if os.path.exists("config.yml"):
            os.rename("config.yml", config_file)
            print(f"--- {config_file} restaurado correctamente ---")

# 1. Ejecutar procesos
run_fdroid("config_oficial.yml")
run_fdroid("config_pruebas.yml")

# 2. Subir a GitHub (Solo si quieres que el script lo haga)
print("--- Intentando subir a GitHub ---")
try:
    subprocess.run("git add .", shell=True, check=True)
    subprocess.run('git commit -m "Update automatico"', shell=True, check=True)
    subprocess.run("git push origin main", shell=True, check=True)
    print("¡Todo en internet!")
except Exception as e:
    print