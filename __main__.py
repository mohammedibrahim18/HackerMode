import sys
from setup import Installer
from base.config import Config

class HackerMode:
    argv = [
        'install',
        'update',
        'check'
    ]

    def start(self,argv):
        if argv[1:]:
            for argv in argv[1:]:
                try:
                    getattr(self,argv)()
                except AttributeError:
                    print ('help msg')
        else:
            from base.shell import BaseCommands
            Shell = BaseCommands()
            while True:
                try:
                    Shell.cmdloop()
                except KeyboardInterrupt:
                    print('')

    def install(self):
        Installer.install()

    def update(self):
        Installer.update()

    def check(self):
        Installer.check()

if __name__ == '__main__':
    HackerMode = HackerMode()
    HackerMode.start(sys.argv)
