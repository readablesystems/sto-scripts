#!/bin/bash

MAX_RETRIES=10
ITERS=5
THREADS=(1 2 4 12 24 36 48)
TIMEOUT=20  # In seconds
TEMPDIR=$(mktemp -d /tmp/sto-XXXXXX)
TEMPERR="$TEMPDIR/err"
TEMPOUT="$TEMPDIR/out"

RUN_FLAGS=(
  "-iopaque -g -w1"
  "-iopaque -g -w4"
  "-idefault -g -w1"
  "-idefault -g -w4"
  #"-imvcc -g"
)
RUN_LABELS=(
  "OCC + OP (W1)"
  "OCC + OP (W4)"
  "OCC (W1)"
  "OCC (W4)"
  #"MVCC (W0)"
)

BASE_BINARIES=(
  "tpcc_bench" "-base" "NDEBUG=1 INLINED_VERSIONS=1 USE_JEMALLOC=1 OBSERVE_C_BALANCE=1" ""
)
HASH_BINARIES=(
  "tpcc_bench" "-hash" "NDEBUG=1 INLINED_VERSIONS=1 USE_HASH_INDEX=1 USE_JEMALLOC=1 OBSERVE_C_BALANCE=1" " + HT"
)
ALOC_BINARIES=(
  "tpcc_bench" "-aloc" "NDEBUG=1 INLINED_VERSIONS=1 OBSERVE_C_BALANCE=1" " + RP"
)
FULL_BINARIES=(
  "tpcc_bench" "-full" "NDEBUG=1 INLINED_VERSIONS=1 USE_HASH_INDEX=1 OBSERVE_C_BALANCE=1" " + HT + RP"
)

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
    FLAGS+=("$1")
    shift
  done
  for i in $(seq $FL_COUNT)
  do
    LABELS+=("$1")
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
          if [[ $f != *"-w"* ]]
          then
            cmd="$cmd -w$i"
          fi
          printf "\rRun $runs times: $cmd"
          $cmd 2>$TEMPERR >$TEMPOUT &
          pid=$!
          sleep $TIMEOUT && kill -0 $pid 2&>/dev/null && echo "noo!" &
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
    printf "Running OCC on $BINARY$CT_FLAGS\n"
    run_bench $OUTFILE $BINARY "$CT_FLAGS" $ITERS $THREADS "${RUN_FLAGS[@]}" "${RUN_LABELS[@]}"
    if [ $RFILE != $OUTFILE ]
    then
      mv $RFILE results/rcopy.txt
      join --header -t , -j 1 results/rcopy.txt $OUTFILE > $RFILE
      rm results/rcopy.txt $OUTFILE
    fi
  done
}

estimate_runtime () {
  sets=$1
  seconds=$(($sets * (${#THREADS[@]} * $ITERS * 15 + 60) * 3))
  minutes=$(($seconds / 60 % 60))
  hours=$(($seconds / 3600 % 24))
  days=$(($seconds / 86400))
  seconds=$(($seconds % 60))
  printf "Estimated runtime: %d:%02d:%02d:%02d\r\n" $days $hours $minutes $seconds
}

estimate_runtime $(((${#BASE_BINARIES[@]} + ${#HASH_BINARIES[@]} + ${#ALOC_BINARIES[@]} + ${#FULL_BINARIES[@]}) / 3))

compile "${BASE_BINARIES[@]}" "${HASH_BINARIES[@]}" "${ALOC_BINARIES[@]}" "${FULL_BINARIES[@]}"
#compile "${BASE_BINARIES[@]}" "${FULL_BINARIES[@]}"

rm -rf results
mkdir results
RFILE=results/results.txt

# Run all
run "${BASE_BINARIES[@]}" "${HASH_BINARIES[@]}"
#run "${BASE_BINARIES[@]}"

./mount_hugepages.sh 102400

run "${ALOC_BINARIES[@]}" "${FULL_BINARIES[@]}"
#run "${FULL_BINARIES[@]}"

./mount_hugepages.sh 0

python3 /home/yihehuang/send_email.py --exp="TPC-C factors" results/results.txt

sudo shutdown -h now
