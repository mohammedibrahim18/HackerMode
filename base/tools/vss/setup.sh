#!/bin/bash

if [ "$PREFIX" == '' ];then
    APD='apt'
    PREFIX="/"
else
    APD='pkg'
fi

echo "|----> [+] Starting Setup.... ($APD) "

chmod +x console/*/*/vcs.*
chmod +x scripts/*

if [ ! -f $PREFIX'/bin/nc' ];then
   echo "| Installing ncat...         (Please be Patient)"
   $APD install netcat -y &> /dev/null
fi

if [ ! -f $PREFIX"/bin/xterm" ]; then
   $APD install xterm -y &> /dev/null
fi

if [ ! -f $PREFIX"/bin/morse" ]; then
   echo "| installing seffect (Morse)"
   $APD install morse -y &> /dev/null
fi


if [ -f .term.vcc ]; then
   echo "Before, You agree to the term of usage attached here:  "
   printf "Continue [Y/n]  "
   read ans
   if [ "$ans" == "Y" ] || [ "$ans" == "y" ]; then
      echo "Done, Good luck with testing"

      rm .term.vcc
      echo "Please Subscribe to Vairous7x on youtube Before starting (:"
      (firefox https://www.youtube.com/c/Vairous7x/videos &) &> /dev/null
      sleep 5
   else
      echo "Aborted"

   fi
fi
