if [ "$#" != 2 ]; then
  echo "Unarchive: Usage: unarchive <file> <Output folder>" 
  exit 1 
fi
tar -xf $1 $2
