# coding: utf-8
import os, __main__
from distutils.util import strtobool
from configparser import ConfigParser, DuplicateSectionError

DEFAULT_ENCODING = 'UTF-8'

class UndefinedValueError(Exception):
    pass


class Undefined(object):
    """
    Class to represent undefined type.
    """
    pass


# Reference instance to represent undefined values
undefined = Undefined()


class RepositoryIni:
    """
    Retrieves option keys from .ini files.
    """
    SECTION = 'settings'

    def __init__(self, source, encoding=DEFAULT_ENCODING):
        self.parser = ConfigParser()
        with open(source, encoding=encoding) as file_:
            self.parser.readfp(file_)

    def __contains__(self, key):
        return (key in os.environ or
                self.parser.has_option(self.SECTION, key))

    def __getitem__(self, key):
        return self.parser.get(self.SECTION, key)

class Config(object):
    configfile = os.path.join(
        os.path.dirname(os.path.abspath(__main__.__file__)),'settings.ini'
    )
    def __init__(self):
        self.repository = RepositoryIni(source=self.configfile,encoding=DEFAULT_ENCODING)

    def _cast_boolean(self, value):
        """
        Helper to convert config values to boolean as ConfigParser do.
        """
        value = str(value)
        return bool(value) if value == '' else bool(strtobool(value))

    @staticmethod
    def _cast_do_nothing(value):
        return value

    def _find_file(self, path):
        # look for all files in the current path
        filename = os.path.join(path, self.configfile)
        if os.path.isfile(filename):
            return filename

        # search the parent
        parent = os.path.dirname(path)
        if parent and parent != os.path.abspath(os.sep):
            return self._find_file(parent)

        # reached root without finding any files.
        return ''

    def setFile(self,ConfigFile):
        if os.path.isfile(ConfigFile):
            self.configfile = ConfigFile
            self.repository = RepositoryIni(source=self.configfile, encoding=DEFAULT_ENCODING)

        else:
            raise FileNotFoundError(f'No such file or directory: {ConfigFile}')

    def set(self,section,option,value):
        try:
            # add new section
            self.repository.parser.add_section(section)
        except DuplicateSectionError:
            pass

        # update
        self.repository.parser.set(section,option,value)

        # save
        with open(self._load_file(),'w') as configfile:
            self.repository.parser.write(configfile)

    def get(self, section, option, default=undefined, cast=undefined):
        """
        Return the value for option or default if defined.
        """
        try:
            self.repository.parser.SECTION = section
        except DuplicateSectionError:
            pass
        # We can't avoid __contains__ because value may be empty.

        if option in self.repository:
            value = self.repository[option]
        else:
            if isinstance(default, Undefined):
                raise UndefinedValueError('{} not found. Declare it as envvar or define a default value.'.format(option))

            value = default

        if isinstance(cast, Undefined):
            cast = self._cast_do_nothing
        elif cast is bool:
            cast = self._cast_boolean

        return cast(value)


Config = Config()

if __name__ == '__main__':
    # tests:
    Config.setFile('file.ini')

    # auto update and save
    Config.set('settings','HOME','/home/dir')

    settings_home = Config.get('settings','HOME',cost=str)
    print (settings_home)
