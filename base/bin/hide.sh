if [ "$#" != 1 ];then
  echo "Usage: hide <file_name>"
  exit
fi
mv $1 .$1 &> /dev/null
