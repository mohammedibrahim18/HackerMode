import os
import sys
import json
import base64
import marshal
import pathlib
import datetime

from typing import List

sys.path.append('/'.join(os.path.abspath(__file__).split('/')[:-1]))


class System:
    TOOL_NAME: str = 'HackerMode'
    BASE_PATH: str = pathlib.Path(os.path.abspath(__file__)).parent

    def __init__(self):
        self.HACKERMODE_PACKAGES = self.HACKERMODE_PACKAGES()

    @property
    def BIN_PATH(self) -> str:
        return ''.join(sys.executable.split('bin')[:-1]) + 'bin'

    @property
    def TOOL_PATH(self) -> str:
        '''To get the tool path'''
        ToolPath = os.path.join(os.environ['HOME'],'.HackerMode')
        if not os.path.isdir(ToolPath):
            os.mkdir(ToolPath)
        return ToolPath

    @property
    def PLATFORME(self) -> str:
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
    def SYSTEM_PACKAGES(self) -> str:
        '''To gat all files that is in [/usr/bin] directory'''
        return os.listdir(self.BIN_PATH)

    def HACKERMODE_PACKAGES(self) -> List[str]:
        HackerModePackages = lambda path: [
            a for a in os.listdir(
                os.path.abspath(os.path.join(self.BASE_PATH,path)))
        ]
        packages: List[str] = []
        for file_name in HackerModePackages('bin'):
            for ext in ['.c','.py','.sh','.dart','.java','.php','.js','.pyc','.cpp']:
                if file_name.endswith(ext):
                    packages.append(file_name[0:-len(ext)])
        for tool_name in HackerModePackages('tools'):
            if tool_name not in packages:
                packages.append(tool_name)
        return list(set(packages))


System = System()

class DataBase:
    config = {
        "apiKey": "AIzaSyAlPn686R3pA4K1WrszyXbqME1O92kpcNA",
        "authDomain": "hackermode-c542d.firebaseapp.com",
        "databaseURL": "https://hackermode-c542d.firebaseapp.com",
        "storageBucket": "hackermode-c542d.appspot.com"
    }

    def __init__(self):
        import pyrebase, requests
        self.requests = requests
        self.firebase = pyrebase.initialize_app(self.config)
        self.auth = self.firebase.auth()

    def sign_in(self,email,password):
        try:
            user = self.auth.sign_in_with_email_and_password(email,password)
            return {
                'status_code':200,
                'data':user,
            }
        except self.requests.exceptions.HTTPError as e:
            return {
                'status_code':400,
                'data':json.loads(e.strerror)
            }

    def sign_up(self,email,password,repeat_password):
        if password != repeat_password:
            return {
                'status_code': 400,
                'data': {
                    'error':{
                        'message':'PASSWORD_ERROR'
                    }
                }
            }
        try:
            user = self.auth.create_user_with_email_and_password(email,password)
            return {
                'status_code':200,
                'data':user,
            }
        except self.requests.exceptions.HTTPError as e:
            return {
                'status_code':400,
                'data':json.loads(e.strerror)
            }

    def send_email_verification(self,token):
        if (data:=self.auth.get_account_info(token)).get('users')[0].get('emailVerified'):
           return {
                'status_code':200,
                'data':data
            }
        try:
            self.auth.send_email_verification(token)
            return {
                'status_code':200,
                'data':self.auth.get_account_info(token)
            }
        except self.requests.exceptions.HTTPError as e:
            return {
                'status_code': 400,
                'data': json.loads(e.strerror)
            }

class AppApi:
    exec(marshal.loads(b'c\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00@\x00\x00\x00s\x0c\x00\x00\x00d\x00d\x01\x84\x00Z\x00d\x02S\x00)\x03c\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x05\x00\x00\x00\x06\x00\x00\x00C\x00\x00\x00sZ\x00\x00\x00t\x00j\x01d\x01k\x02rRd\x02d\x03\x84\x00}\x01z t\x02j\x02\xa0\x03\xa1\x00}\x02|\x02|\x01\x83\x00\x18\x00\xa0\x04\xa1\x00}\x03d\x04}\x04W\x00n\x0e\x01\x00\x01\x00\x01\x00Y\x00d\x05S\x000\x00|\x03|\x04k\x00rNd\x06S\x00d\x05S\x00d\x06S\x00d\x00S\x00)\x07NZ\x06termuxc\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x08\x00\x00\x00S\x00\x00\x00sz\x00\x00\x00t\x00d\x01d\x00d\x00d\x02\x85\x03\x19\x00d\x03\x83\x02\x8fH}\x00|\x00\xa0\x01\xa1\x00\xa0\x02\xa1\x00\xa0\x03d\x04d\x00d\x00d\x02\x85\x03\x19\x00d\x05\xa1\x02}\x01t\x04\xa0\x05|\x01d\x00d\x00d\x02\x85\x03\x19\x00\xa1\x01\xa0\x06d\x06\xa1\x01}\x01W\x00d\x00\x04\x00\x04\x00\x83\x03\x01\x00n\x101\x00sb0\x00\x01\x00\x01\x00\x01\x00Y\x00\x01\x00t\x07j\x07\xa0\x08|\x01d\x07\xa1\x02S\x00)\x08Nz\x19nekot./edoMrekcaH/dracds/\xe9\xff\xff\xff\xff\xda\x01rz\x06=nekot\xda\x00z\x05utf-8z\x14%Y-%m-%d %H:%M:%S.%f)\t\xda\x04open\xda\x04read\xda\x05strip\xda\x07replace\xda\x06base64\xda\tb64decode\xda\x06decode\xda\x08datetime\xda\x08strptime)\x02\xda\x01fZ\x06dt_str\xa9\x00r\r\x00\x00\x00\xfa\x08<String>\xda\x04date\x03\x00\x00\x00s\x0c\x00\x00\x00\x00\x01\x16\x01\x1e\x018\x01\x06\x01\x04\xffz\x13activ.<locals>.datei\x80Q\x01\x00FT)\x05Z\x06SystemZ\tPLATFORMEr\n\x00\x00\x00\xda\x03nowZ\rtotal_seconds)\x05\xda\x04selfr\x0f\x00\x00\x00r\x10\x00\x00\x00Z\x02dtZ\x0fper_day_secondsr\r\x00\x00\x00r\r\x00\x00\x00r\x0e\x00\x00\x00\xda\x05activ\x01\x00\x00\x00s\x18\x00\x00\x00\x00\x01\n\x01\x08\x07\x02\x01\n\x01\x0e\x01\x08\x01\x06\x01\x08\x01\x08\x01\x04\x01\x04\x02r\x12\x00\x00\x00N)\x01r\x12\x00\x00\x00r\r\x00\x00\x00r\r\x00\x00\x00r\r\x00\x00\x00r\x0e\x00\x00\x00\xda\x08<module>\x01\x00\x00\x00\xf3\x00\x00\x00\x00'))

AppApi = AppApi()

if __name__ == '__main__':
    # tests:
    '''print( System.SYSTEM_PACKAGES )
    print( System.PLATFORME )
    print( System.BIN_PATH )'''
    print( System.TOOL_PATH )
