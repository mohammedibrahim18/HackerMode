gcc scr/or_send.c -o scr/or_send
gcc scr/or_server.c -o scr/or_server
gcc scr/remote.c -o scr/remote
chmod +x scr/*
if [ "$1" == "remote" ];then
   printf "Enter Server IP---: "
   read IP
   printf "Enter Server Port-: "
   read PORT
   printf "Service Started, "
   (scr/remote $IP $PORT &)
   printf "To Stop Kill the proccess with command 'kill' \n"
elif [ "$1" == "redout" ];then
   printf "Enter Program Name To Run--: "
   read prog
   printf "Enter Server (Receiver) IP-: "
   read IP
   printf "Enter Server Port----------: "
   read PORT
   printf "Program $prog Started, Output redirected to $IP\n"
   scr/redout $prog $IP $PORT
elif [ "$1" == "recout" ];then
   printf "Your IP-----------------: "
   read ip
   printf "Your Port---------------: "
   read port
   printf "Filname To store output-: "
   read file
   printf "Service Started, ($ip:$port)\n\n"
   scr/recout $ip $port $file
elif [ "$1" == "remcon" ];then
   printf "Enter Your IP------: "
   read iP
   printf "Enter Port---------: "
   read Port
   printf "Waiting for Remote HackerMode Service to Connect...\n"
   nc -lt $iP $Port
else
   printf "|----------------------|\n"
   printf "Usage: aioc <command>\n"
   printf "       aioc remote\n"
   printf "       aioc recout\n"
   printf "       aioc redout\n"
   printf "       aioc remcon\n"
   printf "|----------------------|\n"
fi
