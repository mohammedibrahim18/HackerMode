import os
import sys
class runfile:
        def __init__(self):
                self.commands={
                        '.py':'python3',
                        '.pyc':'python3',
                        '.sh':'bash',
                        '.php':'php',
                        '.dart':'dart',
                        '.js':'node',
                }
                self.path='.'
        def isfile(self):
                for x in self.commands.keys():
                        if self.path.endswith(x):return True
        def run(self):
                if not os.path.isfile(self.path):
                        print (f"[Errno 2] No such file or directory: '/{os.path.join(*__file__.split('/')[:-1],sys.argv[1])}'")
                        return
                if not self.isfile():
                        print (f'# run not support this file "{self.path}"')
                        return
                ext = self.path.split('.')[-1]
                os.system(f'{self.commands["."+ext]} {self.path}')
        def run_shell(self):
                try:
                        self.path=sys.argv[1]
                        self.run()
                except IndexError:pass

runfile().run_shell()