#!/bin/bash

shopt -s expand_aliases

alias go="$GOBIN/go1.6.4"

/home/ubuntu/sto/mount_hugepages.sh 102400

export PATH="$PATH:/home/ubuntu/doppel/list-cpus"

cd "$GOPATH/src/github.com/narula/ddtxn/benchmarks"

go install ./single
go install ./buy

cd "/home/ubuntu/doppel"

for p in 20 90 160
do
  OUTFILE="d-${p}p-results.txt"
  printf "# Threads" >> $OUTFILE
  for k in {1..5}
  do
    printf ",Doppel ($p phases) [T$k]" >> $OUTFILE
  done
  printf "\n" >> $OUTFILE
  for i in 1 2 4 12 24 32 40 48 64
  do
    printf "$i" >> $OUTFILE
    for k in {1..5}
    do
      "$GOBIN/buy" -nprocs=$i -ngo=$i -nw=$i -nsec=10 -contention=-1 -rr=10 -allocate=False -sys=0 -rlock=False -wr=2.0 -phase=$p -sr=500 -atomic=False -zipf=1.4 -out=data.out -ncrr=0 -cw=2.00 -rw=0.50 -split=False -latency=False -v=0
      doppel=$(cat data.out | grep '^ total/sec:' | grep -oE '[0-9.e+]+$')
      printf ",$doppel" >> $OUTFILE
      rm -f data.out
      sleep 1
    done
    printf "\n" >> $OUTFILE
  done
done

/home/ubuntu/sto/mount_hugepages.sh 0

python3 /home/ubuntu/send_email.py -e 'Doppel' d-*-results.txt
sudo shutdown -h +1
