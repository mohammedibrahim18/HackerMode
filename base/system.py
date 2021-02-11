import os, sys, tempfile, pathlib
sys.path.append('/'.join(os.path.abspath(__file__).split('/')[:-1]))
class System:
    TOOL_NAME = 'HackerMode'
    BASE_PATH = pathlib.Path(os.path.abspath(__file__)).parent

    @property
    def BIN_PATH(self):
        return ''.join(sys.executable.split('bin')[:-1]) + 'bin'

    @property
    def TOOL_PATH(self):
        '''To get the tool path'''
        return os.path.abspath(tempfile.gettempdir())

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
        '''To gat all files that is in [/usr/bin] directory'''
        return os.listdir(self.BIN_PATH)

System = System()

if __name__ == '__main__':
    # tests:
    '''print( System.SYSTEM_PACKAGES )
    print( System.PLATFORME )
    print( System.BIN_PATH )'''
    print( System.TOOL_PATH )