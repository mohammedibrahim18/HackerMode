import os
import sys
import json
import marshal
import pathlib

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
