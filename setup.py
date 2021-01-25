PACKAGES = {
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
    'git':{
        'termux': ['pkg install git'],
        'linux': ['sudo apt install git'],
    },
    # -----------------------------------
}

PYHTON3_MODULES = {
    'N4Tools==1.7.0':'N4Tools',
    'pyfiglet':'pyfiglet',
    'python-bidi':'bidi',
    'arabic_reshaper':'arabic_reshaper',
}

RED = '\033[1;31m'
GREEN = '\033[1;32m'
NORMAL = '\033[0m'

from base.system import System
from base.config import Config
import os, shutil

class Installer:
    InstalledSuccessfully = {
        'base':[]
    }

    def InstalledMsg(self,package,message=False):
        DefaultMessage = f'{package} installed successfully.'
        return f'[  {GREEN}OK{NORMAL}  ] {DefaultMessage if not message else message}'

    def NotInstalledMsg(self, package, message=False):
        DefaultMessage = f' not able to install "{package}".'
        return f'[ {RED}Error{NORMAL} ] {DefaultMessage if not message else message}'

    def install(self):
        if System.PLATFORME in ('termux','linux'):
            pass
        else:
            if System.PLATFORME == 'unknown':
                print ("# The tool could not recognize the system!")
                print ("# Do You want to continue anyway?")
                while True:
                    if input('# [Y/N]: ').lower() == 'y':
                        break
                    else:
                        print('# good bye :D')
                        return
            else:
                print (f"# The tool does not support {System.PLATFORME}")
                print ('# good bye :D')
                return

        # Install the basics packages:
        for PACKAGE_NAME,SETUP in PACKAGES.items():
            for COMMANDS in SETUP[System.PLATFORME]:
                os.system(COMMANDS)

        # Install the basics python3 modules:
        for MODULES in PYHTON3_MODULES.keys():
            if System.PLATFORME == 'linux':
                os.system(f'sudo pip3 install {MODULES}')
            elif System.PLATFORME == 'termux':
                os.system(f'pip install {MODULES}')

        # check:
        print('\n# checking:')
        self.check()
        if Config.get('settings', 'IS_INSTALLED', cast=bool):
            return

        # Move the tool to "System.TOOL_PATH"
        if all(self.InstalledSuccessfully['base']):
            if not Config.get('settings','DEBUG',cast=bool):
                if os.path.isdir(f'/{System.TOOL_NAME}'):
                    to = System.TOOL_PATH
                    shutil.move(f'/{System.TOOL_NAME}',to)
                    Config.set('settings', 'IS_INSTALLED', 'True')
                else:
                    print(f'{RED}# Error: the tool path not found!')
                    print(f'# try to run tool using {GREEN}"python3 HakcerMode install"{NORMAL}')
            else:
                print(f'{RED}# In DEBUG mode can"t move the tool\n# to "System.TOOL_PATH"!{NORMAL}')
        else:
            print(f'# {RED}Error:{NORMAL} some of the basics package not installed!')

    def check(self):
        '''To check if the packages has been
           installed successfully. '''

        # check the basics packages:
        for package in PACKAGES.keys():
            if package in System.SYSTEM_PACKAGES:
                print (self.InstalledMsg(package))
                self.InstalledSuccessfully['base'].append(True)
            else:
                print (self.NotInstalledMsg(package))
                self.InstalledSuccessfully['base'].append(False)

        # check the basics python3 modules:
        for module in PYHTON3_MODULES.keys():
            try:
                exec(f'import {PYHTON3_MODULES[module]}')
                print(self.InstalledMsg(module))
                self.InstalledSuccessfully['base'].append(True)

            except ModuleNotFoundError:
                print (self.NotInstalledMsg(module))
                self.InstalledSuccessfully['base'].append(False)

    def update(self):
        os.system(f'cd {os.path.join(System.TOOL_PATH,System.TOOL_NAME)} && git pull')

Installer = Installer()

if __name__ == '__main__':
    # tests:
    Installer.InstalledSuccessfully()
    Installer.check()
    Installer.InstalledSuccessfully()
    Installer.install()
    Installer.update()
    Installer.NotInstalledMsg()
    Installer.InstalledMsg()