if [ "$#" != 2 ]; then
  echo "Archive: Usage: archive <directory> <Output file>" 
  exit 1
fi

cd $1
tar -cf $2 $(ls)
mv $2 $OLDPWD
