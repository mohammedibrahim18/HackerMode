import os
import sys
class runfile:
        def __init__(self):
                self.path='.'
                self.args=['.py',".sh",'.c','.php']
        def isfile(self):
                for x in self.args:
                        if self.path.endswith(x):return True
        def run(self):
                if not os.path.isfile(self.path):
                        print (f"[Errno 2] No such file or directory: '/{os.path.join(*__file__.split('/')[:-1],sys.argv[1])}'")
                elif self.isfile():os.system(f'python {self.path}')
        def run_shell(self):
                try:
                        self.path=sys.argv[1]
                        self.run()
                except IndexError:pass
runfile().run_shell()
