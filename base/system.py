import os, sys, tempfile

class System:
    TOOL_PATH = tempfile.gettempdir()
    TOOL_NAME = 'HackerMode'
    BIN_PATH = ''.join(sys.executable.split('bin')[:-1]) + 'bin'

    @property
    def PLATFORME(self):
        '''To get the platform name'''

        if sys.platform in ('win32', 'cygwin'):
            return 'win'

        elif sys.platform == 'darwin':
            return 'macosx'

        elif 'PWD' in os.environ and 'com.termux' in os.environ['PWD']:
            return 'termux'

        elif sys.platform.startswith('linux') or sys.platform.startswith('freebsd'):
            return 'linux'

        return 'unknown'

    @property
    def SYSTEM_PACKAGES(self):
        return os.listdir(self.BIN_PATH)

System = System()

if __name__ == '__main__':
    # tests:
    #print( System.SYSTEM_PACKAGES )
    print( type(System.PLATFORME) )
    print( System.BIN_PATH )

