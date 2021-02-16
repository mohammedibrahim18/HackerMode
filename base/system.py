import os, sys, tempfile, pathlib, pyrebase, requests, json

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

class DataBase:
    config = {
        "apiKey": "AIzaSyAlPn686R3pA4K1WrszyXbqME1O92kpcNA",
        "authDomain": "hackermode-c542d.firebaseapp.com",
        "databaseURL": "https://hackermode-c542d.firebaseapp.com",
        "storageBucket": "hackermode-c542d.appspot.com"
    }

    def __init__(self):
        self.firebase = pyrebase.initialize_app(self.config)
        self.auth = self.firebase.auth()

    def sign_in(self,email,password):
        try:
            user = self.auth.sign_in_with_email_and_password(email,password)
            return {
                'status_code':200,
                'data':user,
            }
        except requests.exceptions.HTTPError as e:
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
        except requests.exceptions.HTTPError as e:
            return {
                'status_code':400,
                'data':json.loads(e.strerror)
            }

    def send_email_verification(self,token):
        if data:=self.auth.get_account_info(token).get('users')[0].get('emailVerified'):
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
        except requests.exceptions.HTTPError as e:
            return {
                'status_code': 400,
                'data': json.loads(e.strerror)
            }

if __name__ == '__main__':
    # tests:
    '''print( System.SYSTEM_PACKAGES )
    print( System.PLATFORME )
    print( System.BIN_PATH )'''
    print( System.TOOL_PATH )