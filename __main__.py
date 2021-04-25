import os
import sys
import base64
from setup import Installer


class HackerMode:
    argv = [
        'install',
        'update',
        'upgrade',
        'check'
    ]

    def start(self, argv):
        if argv[1:]:
            for argv in argv[1:]:
                try:
                    getattr(self, argv)()
                except AttributeError:
                    print('help msg')
        else:
            from base.shell import MainShell
            from rich.traceback import install

            install()
            Shell = MainShell()
            
            while True:
                try:
                    Shell.cmdloop()
                except KeyboardInterrupt:
                    print('')

    def install(self):
        Installer.install()

    def update(self):
        Installer.update()

    def upgrade(self):
        Installer.install()

    def check(self):
        Installer.check()
    
    def delete(self):
        root_path = os.path.join(os.environ["SHELL"].split("/bin/")[0]+"/bin/","sudo")
        bin_path = os.path.join(os.environ["SHELL"].split("/bin/")[0]+"/bin/","HackerMode")
        tool_path = os.path.join(os.environ["HOME"],".HackerMode")
        status = input("# Do you really want to delete the tool?\n [n/y]: ").lower()
        if status in ("y","yes","ok","yep"):
            root = ""
            if os.path.exists(root_path):
                root = "sudo"
            if os.path.exists(bin_path):
                os.system(f"{root} rm {bin_path}")
            if os.path.exists(tool_path):
                os.system(f"{root} rm -rif {tool_path}")
            if not os.path.exists(tool_path) and not os.path.exists(bin_path):
                print("# The deletion was successful...")
            else:
                print("# Error: could not delete the tool!")
if __name__ == '__main__':
    HackerMode = HackerMode()
    HackerMode.start(sys.argv)
