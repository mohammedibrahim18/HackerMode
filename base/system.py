import os, sys, tempfile

class System:
    TOOL_NAME = 'HackerMode'

    @property
    def BIN_PATH(self):
        return ''.join(sys.executable.split('bin')[:-1]) + 'bin'

    @property
    def TOOL_PATH(self):
        '''To get the tool path'''
        path = os.path.abspath(tempfile.gettempdir())
        if path.endswith('/tmp'):
            if not os.path.isdir(path):
                os.mkdir(path)
            path = os.path.join(path,self.TOOL_NAME)
            if not os.path.isdir(path):
                os.mkdir(path)
        return path

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