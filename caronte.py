import subprocess
import re
import os
import sys
import logging
from colorama import init, Fore, Style
from datetime import datetime
import urllib.request
import json as jsonlib
import getpass
try:
    import pyperclip
    _pyperclip_ok = True
except ImportError:
    _pyperclip_ok = False

init(autoreset=True)

# Configuración de logging
logging.basicConfig(
    filename="caronte.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Contraseña maestra (puedes cambiarla o mejorar el método de almacenamiento)
MASTER_PASSWORD = "caronte2026"

def mostrar_banner():
    ancho = 70
    print(Fore.CYAN + Style.BRIGHT + """
 ▄████▄   ▄▄▄       ██▀███   ▒█████   ███▄    █ ▄▄▄█████▓▓█████ 
▒██▀ ▀█  ▒████▄    ▓██ ▒ ██▒▒██▒  ██▒ ██ ▀█   █ ▓  ██▒ ▓▒▓█   ▀ 
▒▓█    ▄ ▒██  ▀█▄  ▓██ ░▄█ ▒▒██░  ██▒▓██  ▀█ ██▒▒ ▓██░ ▒░▒███   
▒▓▓▄ ▄██▒░██▄▄▄▄██ ▒██▀▀█▄  ▒██   ██░▓██▒  ▐▌██▒░ ▓██▓ ░ ▒▓█  ▄ 
▒ ▓███▀ ░ ▓█   ▓██▒░██▓ ▒██▒░ ████▓▒░▒██░   ▓██░  ▒██▒ ░ ░▒████▒
░ ░▒ ▒  ░ ▒▒   ▓▒█░░ ▒▓ ░▒▓░░ ▒░▒░▒░ ░ ▒░   ▒ ▒   ▒ ░░   ░░ ▒░ ░
  ░  ▒     ▒   ▒▒ ░  ░▒ ░ ▒░  ░ ▒ ▒░ ░ ░░   ░ ▒░    ░     ░ ░  ░
░          ░   ▒     ░░   ░ ░ ░ ░ ▒     ░   ░ ░   ░         ░   
░ ░            ░  ░   ░         ░ ░           ░             ░  ░
░                                                               
""")
    print(Fore.CYAN + Style.BRIGHT + "Caronte - Recuperador de credenciales WiFi".center(ancho))
    print(Fore.CYAN + "https://github.com/MixDark".center(ancho))
    print(Fore.CYAN + "Creado por Mix Dark".center(ancho))
    print(Fore.CYAN + f"Fecha: {datetime.now().strftime('%d/%m/%Y')}".center(ancho))
    print(Fore.CYAN + "Version: 2.0".center(ancho))
    print()


def solicitar_contraseña_maestra():
    for _ in range(3):
        pwd = getpass.getpass("Introduce la contraseña maestra para continuar: ")
        if pwd == MASTER_PASSWORD:
            return True
        print(Fore.RED + "Contraseña incorrecta.")
    print(Fore.RED + "Demasiados intentos fallidos. Saliendo...")
    sys.exit(1)

def mostrar_credenciales_wifi(ocultar_passwords=False, filtro_nombre=None, solo_contraseña=None):
    perfiles, data = obtener_perfiles_wifi()
    if not perfiles:
        print(Fore.RED + "No se encontraron perfiles WiFi guardados.")
        print("Salida de netsh para depuración:")
        print(data)
        return []
    resultados = []
    for perfil in perfiles:
        if filtro_nombre and filtro_nombre.lower() not in perfil.lower():
            continue
        password = obtener_contraseña_wifi(perfil)
        if solo_contraseña is True and (not password or password in ["(Sin contraseña o no disponible)", "ERROR al obtener la contraseña", "ERROR inesperado"]):
            continue
        if solo_contraseña is False and password not in ["(Sin contraseña o no disponible)", "ERROR al obtener la contraseña", "ERROR inesperado"]:
            continue
        resultados.append({"wifi": perfil, "password": password})
    if not resultados:
        print(Fore.RED + "No se encontraron redes WiFi con ese filtro.")
        return []
    ancho_nombre = 24
    ancho_pass = 38
    borde_color = Fore.GREEN + Style.BRIGHT
    print(borde_color + "╔" + "═"*ancho_nombre + "╦" + "═"*ancho_pass + "╗")
    print(borde_color + "║" + Fore.YELLOW + Style.BRIGHT + "{:^{ancho_nombre}}".format("Nombre de la red WiFi", ancho_nombre=ancho_nombre) + borde_color + "║" + Fore.YELLOW + Style.BRIGHT + "{:^{ancho_pass}}".format("Contraseña", ancho_pass=ancho_pass) + borde_color + "║")
    print(borde_color + "╠" + "═"*ancho_nombre + "╬" + "═"*ancho_pass + "╣")
    for r in resultados:
        mostrar_pass = "******" if ocultar_passwords and r["password"] not in ["ERROR al obtener la contraseña", "ERROR inesperado", "(Sin contraseña o no disponible)"] else r["password"]
        print(borde_color + "║" + Fore.CYAN + "{:<{ancho_nombre}}".format(r["wifi"][:ancho_nombre], ancho_nombre=ancho_nombre) + borde_color + "║" + Fore.WHITE + "{:<{ancho_pass}}".format(mostrar_pass[:ancho_pass], ancho_pass=ancho_pass) + borde_color + "║")
    print(borde_color + "╚" + "═"*ancho_nombre + "╩" + "═"*ancho_pass + "╝")
    return resultados

def exportar_credenciales(resultados, formato="txt"):
    fecha = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_base = f"wifi_credentials_{fecha}"
    try:
        if formato == "txt":
            nombre_archivo = nombre_base + ".txt"
            with open(nombre_archivo, "w", encoding="utf-8") as f:
                for r in resultados:
                    f.write(f"WiFi: {r['wifi']}\nPassword: {r['password']}\n{'-'*40}\n")
        elif formato == "csv":
            import csv
            nombre_archivo = nombre_base + ".csv"
            with open(nombre_archivo, "w", newline='', encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["WiFi", "Password"])
                for r in resultados:
                    writer.writerow([r['wifi'], r['password']])
        elif formato == "json":
            import json
            nombre_archivo = nombre_base + ".json"
            with open(nombre_archivo, "w", encoding="utf-8") as f:
                json.dump(resultados, f, ensure_ascii=False, indent=2)
        else:
            print(Fore.RED + "Formato no soportado.")
            return
        print(Fore.GREEN + f"Credenciales exportadas a {nombre_archivo}")
        logging.info(f"Credenciales exportadas a {nombre_archivo}")
    except Exception as e:
        print(Fore.RED + f"Error al exportar: {e}")
        logging.error(f"Error al exportar: {e}")

def mostrar_ayuda():
    print(Fore.YELLOW + """
Opciones del menú:
  1. Mostrar credenciales WiFi guardadas
  2. Exportar credenciales a archivo (txt/csv/json)
  3. Ver logs
  4. Ayuda
  5. Salir
  (Y todas las opciones avanzadas del menú principal)
""")

def obtener_perfiles_wifi():
    try:
        data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles'], encoding='utf-8', errors='ignore')
        patrones = [
            r"All User Profile\s*:\s*(.*)",
            r"Perfil de todos los usuarios\s*:\s*(.*)"
        ]
        perfiles = []
        for patron in patrones:
            perfiles += re.findall(patron, data)
        perfiles = [p.strip() for p in perfiles if p.strip()]
        return perfiles, data
    except Exception as e:
        logging.error(f"Error al obtener perfiles WiFi: {e}")
        return [], ""

def obtener_contraseña_wifi(perfil):
    try:
        perfil = perfil.replace('"', '').replace("'", "")
        result = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', perfil, 'key=clear'], encoding='utf-8', errors='ignore')
        patrones = [
            r"Key Content\s*:\s*(.*)",
            r"Contenido de la clave\s*:\s*(.*)"
        ]
        for patron in patrones:
            match = re.search(patron, result)
            if match:
                return match.group(1)
        return "(Sin contraseña o no disponible)"
    except subprocess.CalledProcessError:
        logging.warning(f"No se pudo obtener la contraseña para el perfil: {perfil}")
        return "ERROR al obtener la contraseña"
    except Exception as e:
        logging.error(f"Error inesperado con el perfil {perfil}: {e}")
        return "ERROR inesperado"

def main():
    mostrar_banner()
    while True:
        print(Fore.YELLOW + """
Menú principal:
  1. Mostrar credenciales WiFi guardadas
  2. Exportar credenciales a archivo (txt/csv/json)
  3. Copiar contraseña de una red al portapapeles
  4. Eliminar perfil WiFi
  5. Ver detalles avanzados de un perfil
  6. Filtrar redes WiFi por nombre
  7. Mostrar solo redes con/sin contraseña
  8. Ver logs
  9. Ayuda
  0. Salir
""")
        opcion = input(Fore.CYAN + "Selecciona una opción: ").strip()
        if opcion == "1":
            mostrar_credenciales_wifi()
        elif opcion == "2":
            resultados = mostrar_credenciales_wifi()
            if resultados:
                print(Fore.YELLOW + "\nMenú de exportación:")
                print("  1. txt")
                print("  2. csv")
                formato_opcion = input(Fore.CYAN + "Selecciona el formato (1/2): ").strip()
                if formato_opcion == "1":
                    exportar_credenciales(resultados, "txt")
                elif formato_opcion == "2":
                    exportar_credenciales(resultados, "csv")
                else:
                    print(Fore.RED + "Opción inválida.")
        elif opcion == "3":
            resultados = mostrar_credenciales_wifi()
            if resultados and _pyperclip_ok:
                nombre = input("Nombre exacto de la red WiFi a copiar: ").strip()
                for r in resultados:
                    if r["wifi"] == nombre:
                        pyperclip.copy(r["password"])
                        print(Fore.GREEN + "Contraseña copiada al portapapeles.")
                        break
                else:
                    print(Fore.RED + "Red no encontrada.")
            elif not _pyperclip_ok:
                print(Fore.RED + "pyperclip no está instalado.")
        elif opcion == "4":
            nombre = input("Nombre exacto del perfil WiFi a eliminar: ").strip()
            try:
                subprocess.check_call(["netsh", "wlan", "delete", "profile", f"name={nombre}"])
                print(Fore.GREEN + f"Perfil '{nombre}' eliminado.")
            except Exception as e:
                print(Fore.RED + f"Error al eliminar: {e}")
        elif opcion == "5":
            nombre = input("Nombre exacto del perfil WiFi: ").strip()
            try:
                result = subprocess.check_output(["netsh", "wlan", "show", "profile", nombre, "key=clear"], encoding="utf-8", errors="ignore")
                print(Fore.WHITE + result)
            except Exception as e:
                print(Fore.RED + f"Error al mostrar detalles: {e}")
        elif opcion == "6":
            filtro = input("Parte del nombre de la red WiFi a filtrar: ").strip()
            mostrar_credenciales_wifi(filtro_nombre=filtro)
        elif opcion == "7":
            tipo = input("Mostrar (1) solo redes CON contraseña o (2) solo SIN contraseña: ").strip()
            if tipo == "1":
                mostrar_credenciales_wifi(solo_contraseña=True)
            elif tipo == "2":
                mostrar_credenciales_wifi(solo_contraseña=False)
            else:
                print(Fore.RED + "Opción inválida.")
        elif opcion == "8":
            try:
                with open("caronte.log", "r", encoding="utf-8", errors="replace") as f:
                    print(Fore.WHITE + f.read())
            except Exception as e:
                print(Fore.RED + f"No se pudo leer el log: {e}")
        elif opcion == "9":
            mostrar_ayuda()
        elif opcion == "0":
            print(Fore.YELLOW + "Saliendo...")
            break
        else:
            print(Fore.RED + "Opción inválida.")

if __name__ == "__main__":
    main()