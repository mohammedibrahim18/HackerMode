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
        'termux': ['pip3 install --upgrade pip'],
        'linux': [
            'sudo apt install python3-pip',
            'pip3 install --upgrade pip',
        ],
    },
    # -----------------------------------
    'git':{
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
}

PYHTON3_MODULES = {
    'N4Tools==1.7.1':'N4Tools',
    'pyfiglet':'pyfiglet',
    'python-bidi':'bidi',
    'arabic_reshaper':'arabic_reshaper',
    'python-nmap':'nmap',
    'requests':'requests',
    'bs4':'bs4',
    'pyrebase':'pyrebase',
    'pygments':'pygments',
    'getmac':'getmac',
}

from base.system import System
from base.config import Config
import os, shutil

RED = '\033[1;31m'
GREEN = '\033[1;32m'
NORMAL = '\033[0m'
HACKERMODE_PATH = '/'.join(os.path.abspath(__file__).split('/')[:-1])

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

        # Install tools packages:
        tempPath = os.getcwd()
        run = f"python3 {os.path.abspath(os.path.join(HACKERMODE_PATH,'base/bin/run.py'))}"
        TOOLS_PATH = os.path.abspath(os.path.join(HACKERMODE_PATH,'base/tools'))
        print (run)
        print (TOOLS_PATH)
        try:
            for tool in  os.listdir(TOOLS_PATH):
                os.chdir(os.path.join(TOOLS_PATH,tool))
                os.system(f'{run} setup.sh')
        finally:
            os.chdir(tempPath)

        # check:
        print('\n# checking:')
        self.check()
        if Config.get('settings', 'IS_INSTALLED', cast=bool):
            return

        # Move the tool to "System.TOOL_PATH"
        if not all(self.InstalledSuccessfully['base']):
            print(f'# {RED}Error:{NORMAL} some of the basics package not installed!')
            return

        if Config.get('settings','DEBUG',cast=bool):
            print('# In DEBUG mode can"t move the tool\n# to "System.TOOL_PATH"!')
            return

        if os.path.isdir(System.TOOL_NAME):
            HackerMode =  '#!/usr/bin/python3\n'
            HackerMode += 'import sys,os\n'
            HackerMode += f'path=os.path.join("{System.TOOL_PATH}","{System.TOOL_NAME}")\n'
            HackerMode += "try:os.system(f'python3 -B {path} '+' '.join(sys.argv[1:]))\n"
            HackerMode += "except:pass"
            try:
                with open(os.path.join(System.BIN_PATH,System.TOOL_NAME),'w') as f:
                    f.write(HackerMode)
                chmod = 'chmod' if System.PLATFORME == 'termux' else 'sudo chmod'
                os.system(f'{chmod} 777 {os.path.join(System.BIN_PATH,System.TOOL_NAME)}')
            except Exception as e:
                print(e)
                print ('# installed failed!')
                return
            Config.set('settings', 'IS_INSTALLED', True)
            try:
                shutil.move(System.TOOL_NAME,System.TOOL_PATH)
            except shutil.Error as e:
                print(e)
                print ('# installed failed!')
        else:
            print(f'{RED}# Error: the tool path not found!')
            print(f'# try to run tool using\n# {GREEN}"python3 HakcerMode install"{NORMAL}')
            print('# installed failed!')

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
        if not Config.get('settings','DEBUG'):
            os.system(f'cd {System.TOOL_PATH} && rm -rif {System.TOOL_NAME} && git clone https://github.com/Arab-developers/{System.TOOL_NAME}')
        else:
            print ("# can't update in the DEUBG mode!")

Installer = Installer()

if __name__ == '__main__':
    # tests:
    print ('# To install write "python3 HackerMode install"')
