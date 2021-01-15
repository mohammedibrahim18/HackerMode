from sys import platform
from os import environ

def get_platform():
    # On Android sys.platform returns 'linux2', so prefer to check the
    # existence of environ variables set during Python initialization
    kivy_build = environ.get('KIVY_BUILD', '')
    if kivy_build in {'android', 'ios'}:
        return kivy_build
    elif 'P4A_BOOTSTRAP' in environ:
        return 'android'
    elif 'ANDROID_ARGUMENT' in environ:
        # We used to use this method to detect android platform,
        # leaving it here to be backwards compatible with `pydroid3`
        # and similar tools outside kivy's ecosystem
        return 'android'
    elif platform in ('win32', 'cygwin'):
        return 'win'
    elif platform == 'darwin':
        return 'macosx'
    elif platform.startswith('linux'):
        return 'linux'
    elif platform.startswith('freebsd'):
        return 'linux'

    return 'unknown'

if __name__ == '__main__':
    print(get_platform())