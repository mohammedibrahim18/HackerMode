'''
How to use?
just write :
$ ifconfig
'''

# N4Tools version:1.7.1
from N4Tools.Design import ThreadAnimation,Square,Color
from requests import get
import socket

@ThreadAnimation()
def MyIpInfo(Thread):
    r = get('http://ipinfo.io/json')
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    inet_ip = s.getsockname()[0]
    s.close()

    output = f'[$LYELLOW]inet[$WIHTE]: [$LGREEN]{inet_ip}\n'
    for key,val in r.json().items():
        if key not in ['hostname','readme','org']:
            key = key.replace('ip','external')
            output += f'[$LYELLOW]{key}[$WIHTE]: [$LGREEN]{val}\n'
    output = output[:-1]

    Sq = Square()
    Sq.cols = 1
    Sq.padding = [1,0,1,0]
    Sq.color = Color().LRED
    Sq.center = True
    temp = '[$LBLUE][[$LGREEN]+[$LBLUE]]'
    Sq.square = [
        temp,
        ' │',
        temp,
        '─',
        temp,
        '  │',
        temp,
        '─']
    Thread.kill()
    print (Sq.style([output]))

MyIpInfo()
