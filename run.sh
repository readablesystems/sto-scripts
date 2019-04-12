#!/bin/bash

MAX_RETRIES=10
ITERS=5
THREADS=(1 2 4 12 24 32 40 48 64)
TIMEOUT=20  # In seconds
HUGEPAGES=49152  # 49152 for stoo, 102400 for AWS

. run_config.sh

setup_tpcc  # Change this accordingly!

ALL_BINARIES=("${OCC_BINARIES[@]}" "${MVCC_BINARIES[@]}")

run_bench () {
  OUTFILE=$1
  shift
  BINARY=$1
  shift
  CT_FLAGS=$1  # Compile-time flags
  shift
  ITERS=$1
  shift
  THREADS=$1
  shift
  FLAGS=()
  LABELS=()
  FL_COUNT=$((${#@} / 2))
  for i in $(seq $FL_COUNT)
  do
    LABELS+=("$1")
    shift
    FLAGS+=("$1")
    shift
  done

  if [ ${#FLAGS[@]} -ne ${#LABELS[@]} ]
  then
    printf "Need equal number of flag parameters (${#FLAGS[@]}) and labels (${#LABELS[@]})\n"
    exit 1
  fi
  printf "# Threads" >> $OUTFILE
  for label in "${LABELS[@]}"
  do
    for k in $(seq 1 $ITERS)
    do
      printf ",$label$CT_FLAGS [T$k]" >> $OUTFILE
    done
  done
  printf "\n" >> $OUTFILE
  for i in ${THREADS[*]}
  do
    printf "$i" >> $OUTFILE
    for f in "${FLAGS[@]}"
    do
      k=0
      while [ $k -lt $ITERS ]
      do
        runs=1
        while [ $runs -le $MAX_RETRIES ]
        do
          cmd="./$BINARY -t$i $f"
          update_cmd
          printf "\rTrial $(($k + 1)), run $runs times: $cmd"
          $cmd 2>$TEMPERR >$TEMPOUT &
          pid=$!
          sleep $TIMEOUT && kill -0 $pid 2&>/dev/null && kill -9 $pid &
          wait $pid
          result=$(tail -n 1 $TEMPOUT | grep -oE '[0-9.]+')
          sleep 2
          #echo "next commit-tid" > /tmp/err  # dry-run
          if [ $(grep 'next commit-tid' $TEMPERR | wc -l) -ne 0 ]
          then
            break
          fi
          runs=$(($runs + 1))
        done
        if [ $runs -gt 1 ]
        then
          printf "\n"
        else
          printf "\r"
          for n in $(seq 1 7)
          do
            printf "           "
          done
          printf "\r"
        fi
        if [ $runs -lt $MAX_RETRIES ]
        then
          printf ",$result" >> $OUTFILE
          k=$(($k + 1))
        else
          while [ $k -lt $ITERS ]
          do
            printf ",DNF" >> $OUTFILE
            k=$(($k + 1))
          done
        fi
      done
    done
    printf "\n" >> $OUTFILE
  done
}

compile() {
  while [ $# -gt 0 ]
  do
    TARGET=$1
    SUFFIX=$2
    BINARY="$TARGET$SUFFIX"
    FLAGS=$3
    shift 4
    if [ -e $BINARY ]
    then
      echo "Reusing existing $BINARY"
    else
      echo "Compiling $BINARY with $FLAGS"
      make clean > /dev/null
      make -j $TARGET $FLAGS > /dev/null
      mv $TARGET $BINARY
    fi
  done
}

run() {
  IS_MVCC=$1
  shift
  printf "stdout and stderr written to: %s\r\n" $TEMPDIR
  while [ $# -gt 0 ]
  do
    TARGET=$1
    SUFFIX=$2
    BINARY="$TARGET$SUFFIX"
    CT_FLAGS=$4
    shift 4

    OUTFILE=$RFILE
    if [ -f $RFILE ]
    then
      OUTFILE=results/rtemp.txt
    fi
    if [ $IS_MVCC -gt 0 ]
    then
      printf "Running MVCC on $BINARY$CT_FLAGS\n"
      run_bench $OUTFILE $BINARY "$CT_FLAGS" $ITERS $THREADS "${MVCC_LABELS[@]}"
    else
      printf "Running OCC on $BINARY$CT_FLAGS\n"
      run_bench $OUTFILE $BINARY "$CT_FLAGS" $ITERS $THREADS "${OCC_LABELS[@]}"
    fi
    if [ $RFILE != $OUTFILE ]
    then
      mv $RFILE results/rcopy.txt
      join --header -t , -j 1 results/rcopy.txt $OUTFILE > $RFILE
      rm results/rcopy.txt $OUTFILE
    fi
  done
}

default_call_runs() {
  ./mount_hugepages.sh $HUGEPAGES

  # Run OCC
  run 1 "${MVCC_BINARIES[@]}"

  # Run MVCC
  run 0 "${OCC_BINARIES[@]}"

  ./mount_hugepages.sh 0
}

estimate_runtime() {
  sets=$1
  seconds=$(($sets * (${#THREADS[@]} * $ITERS * 15 + 60) * 3))
  minutes=$(($seconds / 60 % 60))
  hours=$(($seconds / 3600 % 24))
  days=$(($seconds / 86400))
  seconds=$(($seconds % 60))
  printf "Estimated runtime: %d:%02d:%02d:%02d\r\n" $days $hours $minutes $seconds
}

if [ ${#ALL_BINARIES[@]} -eq 0 ]
then
  echo "No binaries selected! Did you remember to set up an experiment?"
  exit 1
fi

estimate_runtime $(((${#ALL_BINARIES[@]}) / 3))

compile "${ALL_BINARIES[@]}"

rm -rf results
mkdir results
RFILE=results/results.txt
TEMPDIR=$(mktemp -d /tmp/sto-XXXXXX)
TEMPERR="$TEMPDIR/err"
TEMPOUT="$TEMPDIR/out"

call_runs

#python3 /home/yihehuang/send_email.py --exp="$EXPERIMENT_NAME" results/results.txt

#sudo shutdown -h now
