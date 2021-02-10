from N4Tools.Design import ThreadAnimation,Square,Color, AnimationTools,Animation
from N4Tools.terminal import terminal
from requests import get
import socket, nmap, getmac

terminal = terminal()
CO = Color()
AN = Animation()

RULER = lambda _del=6,text='╌':'[$LRED]'+text*(terminal.size['width']-_del)

class networkInfo:
    @property
    def internal_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip

    @property
    def external_ip(self):
        return get('http://ipinfo.io/json').json()

    @property
    def IpInfo(self):
        output = '\nIP Info:\n'
        output += RULER()+'\n'
        output += f' [$LYELLOW]internal[$WIHTE]: [$LGREEN]{self.internal_ip}\n'
        for key,val in self.external_ip.items():
            if key not in ['hostname','readme']:
                key = key.replace('ip','external')
                output += f' [$LYELLOW]{key}[$WIHTE]: [$LGREEN]{val}\n'
        return output

    @property
    def wifiUsers(self):
        hosts = self.internal_ip.split('.')
        hosts = '.'.join(hosts[:-1])+'.0/24'
        Nmap = nmap.PortScanner()
        Nmap.scan(hosts=hosts,arguments='-sP')

        output = '\nWIFI Users:\n'
        output += RULER()+'\n'
        for ip in Nmap.all_hosts():
            device_name = socket.getfqdn(ip)
            device_name = 'Unknow' if device_name == ip else device_name
            mac = getmac.get_mac_address(ip=ip)
            output += f' [$LBLUE]{device_name}:[$WIHTE]\n'
            output += f'  [$LYELLOW]IP [$WIHTE]: [$LGREEN]{ip}\n'
            output += f'  [$LYELLOW]MAC[$WIHTE]: [$LGREEN]{mac if mac else "Unknow"}\n\n'
        return output[:-1]

    def result(self,output):
        Sq = Square()
        Sq.cols = 1
        Sq.color = CO.LRED
        Sq.center = True
        temp = '[$LBLUE][[$LGREEN]+[$LBLUE]]'
        Sq.square = [
            temp,
            ' │ ',
            temp,
            '─',
            temp,
            ' │',
            temp,
            '─']
        return Sq.style([output])

text_anim = AnimationTools.set_text_anim('Network scan is in progress...')
kwargs = (lambda **kwargs:kwargs)(text=text_anim)
@ThreadAnimation(Animation=AN.Loading,kwargs=kwargs,timer=.15)
def result(Thread):
    obj = networkInfo()
    output = obj.result(obj.IpInfo+obj.wifiUsers)
    Thread.set_end(output)

result()
