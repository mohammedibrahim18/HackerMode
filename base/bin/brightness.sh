if [ "$#" != 1 ];then
 echo "Usage: brightness <1-100>"
 exit
fi

(echo $(($1*9+76)) > /sys/class/backlight/intel_backlight/brightness) &> /dev/null
if [ $? == 1 ];then
   echo "Usage: brightness <1-100>"
fi
