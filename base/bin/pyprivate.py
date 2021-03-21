from argparse import ArgumentParser
import marshal as m
import base64 as b
from N4Tools.Design import ThreadAnimation
class pyprivate:
        def read(self,path):
                try:
                        return open(path,'r').read()
                except Exception as e:print(e);exit()
        def write(self,path,text):
                open(path,'w').write(text)
        def Marshal(self,path):
                code=self.read(path)
                en=f'import marshal as m\nexec(m.loads({m.dumps(compile(code,"<String>","exec"))}))'
                self.write(path,en)

        def Base64(self,path):
                en=f"import base64 as b\ndata=lambda x:x({b.b16encode(self.read(path).encode())})\nexec(compile(data(b.b16decode),'<String>','exec'))"
                self.write(path,en)

        def Layers(self,path):
                code=self.read(path)
                for x in range(4):
                        self.Base64(path)
                        self.Marshal(path)


parser=ArgumentParser()
parser.add_argument('-m','--marshal',help='pyprivate -m file.py')
parser.add_argument('-b','--base64',help='pyprivate -b file.py')
parser.add_argument('-l','--layers',help='pyprivate -l file.py')
args=parser.parse_args()
@ThreadAnimation()
def App(Thread):
        out=[]
        if args.marshal:
                pyprivate().Marshal(args.marshal)
                out.append(f'\033[93mMarshal :\033[92m {args.marshal}\033[0m')
        if args.base64:
                pyprivate().Base64(args.base64)
                out.append(f'\033[93mBase64 :\033[92m {args.base64}\033[0m')
        if args.layers:
                pyprivate().Layers(args.layers)
                out.append(f'\033[93mLayers :\033[92m {args.layers}\033[0m')
        Thread.kill()
        print('\n'.join(out))

App()
