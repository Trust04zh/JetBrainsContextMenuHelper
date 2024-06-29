"""
This is a helper script to add options like "使用 Idea 打开 (Open with Idea)" into right-click context menu on Windows by adding Windows registry entries.
If you install JetBrains' applications via JetBrains Toolbox, there would be no option for you to generate the above context menu entry automatically. An solution is to add correspoding registry entries.
However, Toolbox save applications in paths which contains version numbers, and when updating application the path changes, making it tiring to manually keep the registry entries, so here comes this script.

To use this script, you need:
 - Python 3.x
 - Change following configs according to your environment and desire

Feel free to share your idea about this script or this purpose with me.
"""

import os
import re
import winreg
from typing import List
import argparse


class App:
    def __init__(self, name, path):
        self.name = name
        self.path = path


class KEY_STORE:
    def __init__(self, path, arg):
        self.path = path
        self.arg = arg


HKCR = 'HKCR'

# where relevant registry entry stores, "HKCR_DIR" is "HKCR\Directory\shell", for example
HKCR_DIR = KEY_STORE(r'Directory\shell', '%1')
HKCR_DIR_BG = KEY_STORE(r'Directory\Background\shell', '%V')
HKCR_FILE = KEY_STORE(r'*\shell', '%1')
HKCR_FOLDER = KEY_STORE(r'folder\shell', '%1')
HKCR_DRIVER = KEY_STORE(r'Driver\shell', '%1')


# config start here
# base path for applications, application paths that are not absolute will be concat to this
base_path = r'C:\D\R\JetBrains\Toolbox'
applications: List[App] = [
    App('Android Studio', r'Android Studio\bin\studio64.exe'),
    App('CLion', r'CLion\bin\clion64.exe'),
    App('GoLand', r'GoLand\bin\goland64.exe'),
    App('Idea', r'IntelliJ IDEA Ultimate\bin\idea64.exe'),
    App('PyCharm', r'PyCharm Professional\bin\pycharm64.exe'),
    App('RustRover', r'RustRover\bin\rustrover64.exe'),
]  # list of applications to be added to context menu, contains name and path, where "*" implies version number
text_wrapper = '使用 {} 打开'  # wrap displayed text in context menu
context_menu_locations = [
    HKCR_DIR,
    HKCR_DIR_BG,
    # HKCR_FILE,
    # HKCR_FOLDER,
    # HKCR_DRIVER,
]  # in which cases should the entries be displayed, "HKCR_DIR" and "HKCR_DIR_BG" covers most cases for me
# add prefix "JB_" to entries, so they will be listed together and be distinguishable from other entries.
prefix = "JB_"
# config end here


def add():
    for location in context_menu_locations:
        for app in applications:
            # replace " " in entry names.
            key_name = f'{location.path}\\{prefix}{app.name.replace(" ", "")}'
            with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, key_name) as key:
                # set displayed name
                winreg.SetValueEx(key, 'MUIVerb', 0, winreg.REG_SZ, f'{text_wrapper.format(app.name)}')
                # set icon
                winreg.SetValueEx(key, 'Icon', 0, winreg.REG_SZ, f'"{app.path}",0')
            key_command_name = f'{key_name}\\command'
            with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, key_command_name) as key:
                # set command to execute
                winreg.SetValueEx(key, '', 0, winreg.REG_SZ, f'"{app.path}" "{location.arg}"')
            print(f'write {HKCR}\\{key_name}')


def delete():
    for location in context_menu_locations:
        for app in applications:
            # replace " " in entry names.
            key_name = f'{location.path}\\{prefix}{app.name.replace(" ", "")}'
            try:
                with winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, key_name) as key:
                    info = winreg.QueryInfoKey(key)
                    for _ in range(0, info[0]):  # info[0] implies the number of sub keys this key has
                        subkey: str = winreg.EnumKey(key, 0)
                        winreg.DeleteKey(key, subkey)
                    winreg.DeleteKey(key, '')
                print(f'delete {HKCR}\\{key_name}')
            except FileNotFoundError:
                print(f'skip {HKCR}\\{key_name} cuz unable to find it')


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument('-a', '--add', action='store_true', dest='add', help='create or update entries')
    action.add_argument('-d', '--delete', action='store_true', dest='delete', help='remove entries')
    args = parser.parse_args()

    for app in applications:
        app.path = os.path.join(base_path, app.path)
        print(f'"{text_wrapper.format(app.name)}" use executable file at {app.path}')

    if args.add:
        add()
    else:
        delete()
