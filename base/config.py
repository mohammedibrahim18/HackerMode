# coding: utf-8
import os, json, __main__

class Config(object):
    file = os.path.join(
        os.path.dirname(os.path.abspath(__main__.__file__)),'settings.json'
    )

    def set_file(self,file_path):
        if os.path.isfile(file_path):
            self.file = file_path
        else:
            with open(file_path,'w') as f:
                f.write(json.dumps({},indent=4))

    def set(self,section,option,value):
        section = section.lower()
        option = option.upper()
        with open(self.file,'r') as f:
            data = json.loads(f.read())
        data[section] = {option:value}
        with open(self.file,'w') as f:
            f.write(json.dumps(data,indent=4))

    def get(self,section,option,cast=None):
        section = section.lower()
        option = option.upper()
        with open(self.file,'r') as f:
            data = json.loads(f.read())
        if cast in [str,bool,dict,list,int,set]:
            return cast(data[section][option])
        return data[section][option]

Config = Config()

if __name__ == '__main__':
    # tests:
    Config.set_file('file.json')
    # auto update and save
    Config.set('settings','HOME','/home/dir')
    settings_home = Config.get('settings','HOME',cast=str)
    print (settings_home)
