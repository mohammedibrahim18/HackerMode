import os
import shutil

from base.system import System
from base.config import Config

PACKAGES = {
    'apt': {
        'termux':['apt --fix-broken install'],
        'linux':['apt --fix-broken install'],
    },
    # -----------------------------------
    'pip3': {
        'termux': [
            'pkg install openssl',
            'pip3 install --upgrade pip',
        ],
        'linux': [
            'sudo apt install python3-pip',
            'pip3 install --upgrade pip',
        ],
    },
    # -----------------------------------
    'git': {
        'termux': ['pkg install git'],
        'linux': ['sudo apt install git'],
    },
    # -----------------------------------
    'gcc': {
        'termux': ['pkg install clang'],
        'linux': ['sudo apt install clang'],
    },
    # -----------------------------------
    'nmap': {
        'termux': ['pkg install nmap'],
        'linux': ['sudo apt install nmap'],
    },
    # -----------------------------------
    'dart': {
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
    'redshift':{
        'termux': [],
        'linux': ['sudo apt install redshift'],

    }
}

PYHTON_MODULES = {
    'N4Tools==1.7.1': 'N4Tools',
    'rich': 'rich',
    'pyfiglet': 'pyfiglet',
    'python-bidi': 'bidi',
    'arabic_reshaper': 'arabic_reshaper',
    'bs4': 'bs4',
    'pyrebase': 'pyrebase',
    'pygments': 'pygments',
    'python-nmap': 'nmap',
    'requests': 'requests',
    'getmac': 'getmac',
    'pibyone': 'pibyone',
}

BASE_PYHTON_MODULES = (
    'requests',
    'rich',
    'N4Tools==1.7.1',
    'bs4',
    'pyfiglet',
    'arabic_reshaper',
    'python-bidi',
)

BASE_PACKAGES = (
    'git',
    'pip',
)

RED = '\033[1;31m'
GREEN = '\033[1;32m'
YELLOW = '\033[1;33m'
NORMAL = '\033[0m'
HACKERMODE_PATH = '/'.join(os.path.abspath(__file__).split('/')[:-1])


class Installer:
    InstalledSuccessfully = {
        'base': []
    }

    def InstalledMsg(self, package, message=False):
        DefaultMessage = f'{package} installed successfully.'
        return f'{NORMAL}[  {GREEN}OK{NORMAL}  ] {DefaultMessage if not message else message}'

    def NotInstalledMsg(self, package, message=False, is_base=False):
        DefaultMessage = f' not able to install "{package}".'
        return f'{NORMAL}[ {RED if is_base else YELLOW}{"error" if is_base else "warning"}{NORMAL} ] {DefaultMessage if not message else message}'

    def installer(self):
        '''Install all HackerMode packages and modules'''

        # Install the basics packages:
        for PACKAGE_NAME, SETUP in PACKAGES.items():
            for COMMANDS in SETUP[System.PLATFORME]:
                os.system(COMMANDS)

        # Install the basics python3 modules:
        for MODULES in PYHTON_MODULES.keys():
            if System.PLATFORME == 'linux':
                os.system(f'sudo pip3 install {MODULES}')
            elif System.PLATFORME == 'termux':
                os.system(f'pip install {MODULES}')

        # Install tools packages:
        if Config.get('actions', 'DEBUG', default=False):
            print('# In debug mode can"t run setup.sh')
            return
        tempPath = os.getcwd()
        run = f"python3 {os.path.abspath(os.path.join(HACKERMODE_PATH, 'base/bin/run.py'))}"
        TOOLS_PATH = os.path.abspath(os.path.join(HACKERMODE_PATH, 'base/tools'))
        try:
            for tool in os.listdir(TOOLS_PATH):
                os.chdir(os.path.join(TOOLS_PATH, tool))
                if os.path.isfile('setup.sh'):
                    os.system(f'{run} setup.sh')
        finally:
            os.chdir(tempPath)

    def install(self):
        if not System.PLATFORME in ('termux', 'linux'):
            if System.PLATFORME == 'unknown':
                print("# The tool could not recognize the system!")
                print("# Do You want to continue anyway?")
                while True:
                    if input('# [Y/N]: ').lower() == 'y':
                        break
                    else:
                        print('# good bye :D')
                        return
            else:
                print(f"# The tool does not support {System.PLATFORME}")
                print('# good bye :D')
                return

        self.installer()

        # check:
        print('\n# checking:')
        self.check()

        if System.PLATFORME == "termux":
            try:
                os.listdir("/sdcard")
            except PermissionError:
                os.system("termux-setup-storage")

        if Config.get('actions', 'IS_INSTALLED', cast=bool, default=False):
            return

        # Move the tool to "System.TOOL_PATH"
        if not all(self.InstalledSuccessfully['base']):
            print(f'# {RED}Error:{NORMAL} some of the basics package not installed!')
            return

        if Config.get('actions', 'DEBUG', cast=bool, default=True):
            print('# In DEBUG mode can"t move the tool\n# to "System.TOOL_PATH"!')
            return

        if os.path.isdir(System.TOOL_NAME):
            HackerMode = '#!/usr/bin/python3\n'
            HackerMode += 'import sys,os\n'
            HackerMode += f'path=os.path.join("{System.TOOL_PATH}","{System.TOOL_NAME}")\n'
            HackerMode += "try:os.system(f'python3 -B {path} '+' '.join(sys.argv[1:]))\n"
            HackerMode += "except:pass"
            try:
                with open(os.path.join(System.BIN_PATH, System.TOOL_NAME), 'w') as f:
                    f.write(HackerMode)
                chmod = 'chmod' if System.PLATFORME == 'termux' else 'sudo chmod'
                os.system(f'{chmod} 777 {os.path.join(System.BIN_PATH, System.TOOL_NAME)}')
            except Exception as e:
                print(e)
                print('# installed failed!')
                return
            Config.set('actions', 'IS_INSTALLED', True)
            try:
                shutil.move(System.TOOL_NAME, System.TOOL_PATH)
                print(f'# {GREEN}HackerMode installed successfully...{NORMAL}')
            except shutil.Error as e:
                print(e)
                print('# installed failed!')
        else:
            print(f'{RED}# Error: the tool path not found!')
            print(f'# try to run tool using\n# {GREEN}"python3 HakcerMode install"{NORMAL}')
            print('# installed failed!')

    def check(self):
        '''To check if the packages has been
        installed successfully.

        '''

        # check packages:
        for package in PACKAGES.keys():
            if not PACKAGES[package][System.PLATFORME]:
                continue
            if package in System.SYSTEM_PACKAGES:
                print(self.InstalledMsg(package))
                if package in BASE_PACKAGES:
                    self.InstalledSuccessfully['base'].append(True)
            else:
                print(self.NotInstalledMsg(package, is_base=(package in BASE_PACKAGES)))
                if package in BASE_PACKAGES:
                    self.InstalledSuccessfully['base'].append(False)

        # check python modules:
        for module in PYHTON_MODULES.keys():
            try:
                exec(f'import {PYHTON_MODULES[module]}')
                print(self.InstalledMsg(module))
                if module in BASE_PYHTON_MODULES:
                    self.InstalledSuccessfully['base'].append(True)

            except ModuleNotFoundError:
                print(self.NotInstalledMsg(module, is_base=(module in BASE_PYHTON_MODULES)))
                if module in BASE_PYHTON_MODULES:
                    self.InstalledSuccessfully['base'].append(False)

    def update(self):
        if not Config.get('actions', 'DEBUG', cast=bool, default=False):
            os.system(
                f'cd {System.TOOL_PATH} && rm -rif {System.TOOL_NAME} && git clone https://github.com/Arab-developers/{System.TOOL_NAME}')
            tempPath = os.getcwd()
            run = f"python3 {os.path.abspath(os.path.join(HACKERMODE_PATH, 'base/bin/run.py'))}"
            TOOLS_PATH = os.path.abspath(os.path.join(HACKERMODE_PATH, 'base/tools'))
            try:
                for tool in os.listdir(TOOLS_PATH):
                    os.chdir(os.path.join(TOOLS_PATH, tool))
                    if os.path.isfile('setup.sh'):
                        os.system(f'{run} setup.sh')
            finally:
                os.chdir(tempPath)
        else:
            print("# can't update in the DEUBG mode!")


Installer = Installer()

if __name__ == '__main__':
    # tests:
    print('# To install write "python3 HackerMode install"')
