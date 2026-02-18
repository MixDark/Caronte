# Caronte

**Caronte** es una herramienta en Python para recuperar, gestionar y exportar credenciales WiFi guardadas en Windows. Pensada para usuarios que desean visualizar, exportar o administrar sus redes WiFi de forma sencilla y segura.

## Características principales

- **Visualización de redes WiFi**: Muestra todas las redes WiFi guardadas y sus contraseñas (cuando están disponibles).
- **Exportación de credenciales**: Permite exportar las credenciales a archivos TXT o CSV.
- **Copia al portapapeles**: Copia la contraseña de una red seleccionada directamente al portapapeles.
- **Eliminación de perfiles WiFi**: Elimina perfiles WiFi guardados desde el menú.
- **Filtrado avanzado**: Filtra redes por nombre o muestra solo redes con/sin contraseña.
- **Detalles avanzados**: Visualiza información técnica detallada de cada perfil WiFi.
- **Visualización de logs**: Accede al registro de acciones y errores desde el menú.
- **Interfaz de menú interactivo**: Navegación sencilla por todas las funcionalidades.

## Requisitos

- Python 3.x
- Sistema operativo Windows
- Paquetes: `colorama`, `pyperclip`

## Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/MixDark/Caronte.git
   ```
2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Uso

Ejecuta el script desde la terminal:
```bash
python caronte.py
```

### Menú principal

1. Mostrar credenciales WiFi guardadas
2. Exportar credenciales a archivo (txt/csv)
3. Copiar contraseña de una red al portapapeles
4. Eliminar perfil WiFi
5. Ver detalles avanzados de un perfil
6. Filtrar redes WiFi por nombre
7. Mostrar solo redes con/sin contraseña
8. Ver logs
9. Ayuda
0. Salir

### Ejemplo de exportación

Al elegir la opción de exportar, puedes seleccionar el formato:
- TXT: Archivo de texto plano con todas las credenciales.
- CSV: Archivo de hoja de cálculo compatible con Excel.

## Seguridad

- El script no requiere privilegios de administrador.
- No almacena ni transmite credenciales fuera del equipo.
- El log registra solo acciones locales.

## Contribución

¿Tienes ideas o mejoras? ¡Puedes contribuir! Haz un fork, crea una rama y envía tu pull request.

## Licencia

MIT. Puedes usar, modificar y distribuir libremente.

## Autor

Mix Dark
https://github.com/MixDark
