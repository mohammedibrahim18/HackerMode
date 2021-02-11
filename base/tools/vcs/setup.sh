if [ "$PREFIX" == '' ];then
    APD='apt'
else
    APD='pkg'
fi
if [ ! -f "$PREFIX/bin/pip3" ];then
    $APD install python3-pip &> /dev/null
fi
if [ ! -f "$PREFIX/bin/python3" ];then
    $APD install python3 &> /dev/null 
fi
echo "[+] Starting Setup.... ($APD) "

chmod +x console/termux/vcs.*
chmod +x console/linux/vcs.*

if [ ! -f '$PREFIX/bin/gcc' ];then
   echo "Installing gcc compiler... (Please be Patient)"
   $APD install clang -y &> /dev/null
fi

if [ ! -f '$PREFIX/bin/nc' ];then
   echo "Installing ncat...         (Please be Patient)"
   $APD install netcat -y &> /dev/null
fi
pip3 install pibyone &> /dev/null
echo "[+] Okay"
