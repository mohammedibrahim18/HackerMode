# coding: utf-8
import os, json, shutil, __main__
from system import System

class config(object):
    default_file = os.path.join(
        os.path.dirname('/'.join(os.path.abspath(__main__.__file__).split('/')[:-1])),'settings.json'
    )

    def __init__(self,file=None):
        if file:
            self.file = file
        else:
            self.file = self.default_file

    def create_settings(self):
        file = self.default_file
        if not os.path.isfile(file):
            # default settings
            shutil.copy(os.path.join(System.TOOL_PATH, 'settings.json'), file)

    def set_file(self,file_path):
        if os.path.isfile(file_path):
            self.file = file_path
        else:
            with open(file_path,'w') as f:
                f.write(json.dumps({},indent=4))

    def set(self,section,option,value):
        self.create_settings()
        section = section.lower()
        option = option.upper()
        with open(self.file,'r') as f:
            data = json.loads(f.read())

        data[section][option] = value

        with open(self.file,'w') as f:
            f.write(json.dumps(data,indent=4))

    def get(self,section,option,cast=None):
        self.create_settings()
        section = section.lower()
        option = option.upper()
        with open(self.file,'r') as f:
            data = json.loads(f.read())
        if cast in [str,bool,dict,list,int,set]:
            return cast(data[section][option])
        return data[section][option]

Config = config()

if __name__ == '__main__':
    # tests:
    Config.set_file('file.json')
    # auto update and save
    Config.set('settings','HOME','/home/dir')
    Config.set('settings','DEBUG',True)
    home = Config.get('settings','HOME',cast=str)
    debug = Config.get('settings','DEBUG',cast=bool)
    print (home,type(debug))
    print(Config.default_file)