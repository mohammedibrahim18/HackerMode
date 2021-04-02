for i in $(seq 1 20);do
  redshift -O 6000 &> /dev/null
  sleep 0.02
 done
