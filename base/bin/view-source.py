from N4Tools.Design import ThreadAnimation
import os,sys
reader     = lambda Thread,path : os.popen(f'pygmentize {path}').read()
if len(out:=sys.argv)>1         : print (ThreadAnimation()(reader)(' '.join(out[1:])))
