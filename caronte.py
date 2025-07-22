import subprocess
import re
from colorama import init, Fore, Style

init(autoreset=True)

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
    print(Fore.CYAN + Style.BRIGHT + "Caronte - Recuperador de contraseñas WiFi".center(ancho))
    print(Fore.CYAN + "https://github.com/MixDark".center(ancho))
    print(Fore.CYAN + "Creado por Mix Dark".center(ancho))
    print(Fore.CYAN + "Fecha: 22/07/2025".center(ancho))
    print(Fore.CYAN + "Version: 1.0".center(ancho))
    print()


def process_wifi():
    try:
        # Ejecuta el comando para obtener los perfiles WiFi
        data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles'], encoding='utf-8', errors='ignore')
        # Busca los nombres de los perfiles en inglés y español
        profiles_en = re.findall(r"All User Profile\s*:\s*(.*)", data)
        profiles_es = re.findall(r"Perfil de todos los usuarios\s*:\s*(.*)", data)
        profiles = profiles_en + profiles_es
        if not profiles:
            print(Fore.RED + "No se encontraron perfiles WiFi guardados.")
            print("Salida de netsh para depuración:")
            print(data)
            return
        # Encabezado de la tabla
        ancho_nombre = 24
        ancho_pass = 38
        borde_color = Fore.GREEN + Style.BRIGHT
        print(borde_color + "╔" + "═"*ancho_nombre + "╦" + "═"*ancho_pass + "╗")
        print(borde_color + "║" + Fore.YELLOW + Style.BRIGHT + "{:^{ancho_nombre}}".format("Nombre de la red WiFi", ancho_nombre=ancho_nombre) + borde_color + "║" + Fore.YELLOW + Style.BRIGHT + "{:^{ancho_pass}}".format("Contraseña", ancho_pass=ancho_pass) + borde_color + "║")
        print(borde_color + "╠" + "═"*ancho_nombre + "╬" + "═"*ancho_pass + "╣")
        for profile in profiles:
            try:
                # Ejecuta el comando para obtener la información del perfil, incluyendo la clave
                result = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', profile, 'key=clear'], encoding='utf-8', errors='ignore')
                # Busca la contraseña en inglés y español
                password_en = re.search(r"Key Content\s*:\s*(.*)", result)
                password_es = re.search(r"Contenido de la clave\s*:\s*(.*)", result)
                password = (password_en.group(1) if password_en else (password_es.group(1) if password_es else "(Sin contraseña o no disponible)"))
                print(borde_color + "║" + Fore.CYAN + "{:<{ancho_nombre}}".format(profile[:ancho_nombre], ancho_nombre=ancho_nombre) + borde_color + "║" + Fore.WHITE + "{:<{ancho_pass}}".format(password[:ancho_pass], ancho_pass=ancho_pass) + borde_color + "║")
            except subprocess.CalledProcessError:
                print(borde_color + "║" + Fore.CYAN + "{:<{ancho_nombre}}".format(profile[:ancho_nombre], ancho_nombre=ancho_nombre) + borde_color + "║" + Fore.RED + "{:<{ancho_pass}}".format("ERROR al obtener la contraseña", ancho_pass=ancho_pass) + borde_color + "║")
        print(borde_color + "╚" + "═"*ancho_nombre + "╩" + "═"*ancho_pass + "╝")
    except Exception as e:
        print(Fore.RED + f"Error al obtener los perfiles WiFi: {e}")

if __name__ == "__main__":
    mostrar_banner()
    process_wifi()