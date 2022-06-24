#!/bin/bash

for w in 1 4 0
do
  OUTFILE="e-${w}w-results.txt"
  printf "# Threads" >> $OUTFILE
  for k in {1..5}
  do
    printf ",ERMIA (W$w) [T$k]" >> $OUTFILE
  done
  printf "\n" >> $OUTFILE
  for i in 1 2 4 12 24 32 40 48 64
  do
    printf "$i" >> $OUTFILE
    for k in {1..5}
    do
      echo "running $w,$i,$k"
      wh=$w
      if [ $wh -eq 0 ]; then
        wh=$i
      fi
      ermia=$(./run.sh ./ermia_SI_SSN tpcc $wh $i 10 '-node_memory_gb=40 -null_log_device -enable_gc -phantom_prot --retry-aborted-transactions -persist-policy=async' '--new-order-fast-id-gen' 2>/dev/null | grep -oE '^[0-9.]+ commits/s' | grep -oE '[0-9.]+')
      printf ",$ermia" >> $OUTFILE
      sleep 1
    done
    printf "\n" >> $OUTFILE
  done
done
