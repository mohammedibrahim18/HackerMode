from sys import platform
from os import environ

def get_platform():
    '''To get the platform name'''

    if platform in ('win32', 'cygwin'):
        return 'win'

    elif platform == 'darwin':
        return 'macosx'

    elif 'PWD' in environ and 'com.termux' in environ['PWD']:
        return 'termux'

    elif platform.startswith('linux') or platform.startswith('freebsd'):
        return 'linux'

    return 'unknown'



if __name__ == '__main__':
    print( get_platform() )