#!/usr/bin/python3 -B
'''
Copyright (c) 2021 Arab-developers

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''
import tempfile, sys, os
from HackerMode.base import system
from N4Tools.Design import Color

TOOL_PATH = tempfile.gettempdir()
TOOL_NAME = 'HackerMode'
BIN_PATH = ''.join(sys.executable.split('bin')[:-1])+'bin'
PLATFORME = system.get_platform()

#colors:
RED = '\033[1;31m'
GREEN = '\033[1;32m'
NORMAL = '\033[0m'

class Installer:
    packages = {
        # -----------------------------------
        'dart':{
            'termux': ['pkg install dart'],
            'linux': [
                "sudo apt-get install apt-transport-https",
                "sudo sh -c 'wget -qO- https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -'",
                "sudo sh -c 'wget -qO- https://storage.googleapis.com/download.dartlang.org/linux/debian/dart_stable.list > /etc/apt/sources.list.d/dart_stable.list'",
                "sudo apt-get update",
                "sudo apt-get install dart",
            ],
        },
        # -----------------------------------
        'pip3':{
            'termux': [],
            'linux': ['sudo apt install python3-pip'],
        },
        # -----------------------------------
    }

    python3_modules = {
        'N4Tools':'N4Tools',
        'pyfiglet':'pyfiglet',
        'python-bidi':'bidi',
        'arabic_reshaper':'arabic_reshaper',
    }

    def checker(self):
        # check packages (tool-base):
        SYSTEM_PACKAGES = os.listdir(BIN_PATH)
        for package in self.packages.keys():
            if package in SYSTEM_PACKAGES:
                InstalledMsg = f'{package} has been installed successfully.'
                print(f'[  {GREEN}OK{NORMAL}  ] {InstalledMsg}')

            else:
                NotInstalledMsg = f'The installer was not able to install "{package}".'
                print(f'[ {RED}Error{NORMAL} ] {NotInstalledMsg}')

        # check python3 modules (tool-base):
        for module in self.python3_modules.keys():
            try:
                exec(f'import {self.python3_modules[module]}')
                InstalledMsg = f'{module} has been installed successfully.'
                print(f'[  {GREEN}OK{NORMAL}  ] {InstalledMsg}')

            except ModuleNotFoundError:
                NotInstalledMsg = f'The installer was not able to install "{module}".'
                print(f'[ {RED}Error{NORMAL} ] {NotInstalledMsg}')

Installer().checker()