import sys
from setup import Installer
from base.config import Config
from base.shell import BaseCommands

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
            while True:
                try:
                    BaseCommands().cmdloop()
                except KeyboardInterrupt:
                    print('')


    def install(self):
        Installer.install()
        if all(Installer.InstalledSuccessfully['base']):
            pass

    def update(self):
        if not Config.get('settings','DEBUG',cast=bool):
            pass
            Installer.update()
        else:
            print ("# can't update in the DEUBG mode!")

    def check(self):
        Installer.check()

if __name__ == '__main__':
    HackerMode = HackerMode()
    HackerMode.start(sys.argv)
