for i in $(seq 0 10);do
   redshift -O 7000 &> /dev/null
   sleep 0.1
done
