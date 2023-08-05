# -*- coding: utf-8 -*-

from platform import system as os
import locale
import ctypes


# -------------------------------------------
def get_errors():
    """Returns the help_msg and chrome_error based on language"""
    if("es" in get_OS().get('lang')):
        help_msg = """
                        __  __                           ______ __     ____
                       / / / /____   _____ ____ _ _____ / ____// /    /  _/
                      / /_/ // __ \ / ___// __ `// ___// /    / /     / /
                     / __  // /_/ // /   / /_/ /(__  )/ /___ / /___ _/ /
                    /_/ /_/ \____//_/    \__,_//____/ \____//_____//___/

                    Uso:
                    horasCLI -h | --help
                        'Muestra esta ayuda'
                    horasCLI -s | --show
                        'Abre el registro en Chrome si esta instalado o en la linea de comandos'
                    horasCLI -r | --reset
                        'Resetea el registro'
                    horasCLI -n | --new <nombre del proyecto> <horas>
                        'Crea una fila en el registro con el dia de hoy'
                    horasCLI -n | --new <nombre del proyecto> <horas> <fecha (dd-mm)>
                        'Crea una fila en el registro con el dia que le pasemos'
                    horasCLI -d | --delete
                        'Elimina la ultima fila del registro'
                    horasCLI -f | --file
                        '*SOLO EN WINDOWS* Abre el directorio del archivo en el explorador'
                    horasCLI -c | --code
                        '*SOLO EN WINDOWS* Abre el archivo en VSCode (Necesitas tenerlo instalado)'
                    """
        chrome_error = """
                            __  __                           ______ __     ____
                           / / / /____   _____ ____ _ _____ / ____// /    /  _/
                          / /_/ // __ \ / ___// __ `// ___// /    / /     / /
                         / __  // /_/ // /   / /_/ /(__  )/ /___ / /___ _/ /
                        /_/ /_/ \____//_/    \__,_//____/ \____//_____//___/

                        Instala Google Chrome y la extension Markdown Reader para la mejor visualizacion.
                        """
    else:
        help_msg = """
                        __  __                           ______ __     ____
                       / / / /____   _____ ____ _ _____ / ____// /    /  _/
                      / /_/ // __ \ / ___// __ `// ___// /    / /     / /
                     / __  // /_/ // /   / /_/ /(__  )/ /___ / /___ _/ /
                    /_/ /_/ \____//_/    \__,_//____/ \____//_____//___/

                    Usage:
                    horasCLI -h | --help
                        'Shows this help'
                    horasCLI -s | --show
                        'Opens the schedule in Chrome if exists or as command line'
                    horasCLI -r | --reset
                        'Resets the schedule'
                    horasCLI -n | --new <project name> <hours>
                        'Adds row to the schedule with today date'
                    horasCLI -n | --new <project name> <hours> <date (dd-mm)>
                        'Adds row to the schedule with the given date'
                    horasCLI -d | --delete
                        'Deletes the last row added'
                    horasCLI -m | --manual
                        '*ONLY IN WINDOWS* Opens the folder where the file'
                    horasCLI -c | --code
                        '*ONLY IN WINDOWS* Opens the file in VSCode (You need to have it installed)'
                    """
        chrome_error = """
                            __  __                           ______ __     ____
                           / / / /____   _____ ____ _ _____ / ____// /    /  _/
                          / /_/ // __ \ / ___// __ `// ___// /    / /     / /
                         / __  // /_/ // /   / /_/ /(__  )/ /___ / /___ _/ /
                        /_/ /_/ \____//_/    \__,_//____/ \____//_____//___/

                        Install Chrome and Markdown Reader extension to get the best visualization.
                        """
    return {'help_msg': help_msg, 'chrome_error': chrome_error}


# -------------------------------------------
def get_OS():
    """Get the OS and returns the path to chrome in that OS and the language"""
    if os() == 'Linux':
        # Linux
        chrome_path = '/usr/bin/google-chrome %s'
        lang = locale.getlocale(locale.LC_MESSAGES)[0]
        explorer = False
    elif os() == "Darwin":
        # MacOs
        chrome_path = 'open -a /Applications/Google\ Chrome.app %s'
        lang = locale.getlocale(locale.LC_MESSAGES)[0]
        explorer = False
    elif os() == 'Windows':
        # Windows
        chrome_path = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s"
        lang = locale.windows_locale[ctypes.windll.kernel32.GetUserDefaultUILanguage(
        )]
        explorer = True
    return {'chrome': chrome_path, 'lang': lang, 'explorer': explorer}
