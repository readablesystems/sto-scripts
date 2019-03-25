#!/bin/bash

MAX_RETRIES=10
ITERS=5
THREADS=(1 2 4 12 23 24 36 47 48)
OCC_FLAGS=(
  "-idefault -g"
  "-idefault -g -x"
#  "-idefault -g -w4"
#  "-idefault -g -x -w4"
)
OCC_LABELS=(
  "OCC"
  "OCC + CU"
#  "OCC (W1)"
#  "OCC + CU (W1)"
#  "OCC (W4)"
#  "OCC + CU (W4)"
)
MVCC_FLAGS=(
  "-imvcc -g"
  "-imvcc -g -x"
#  "-imvcc -g -w4"
#  "-imvcc -g -x -w4"
)
MVCC_LABELS=(
  "MVCC"
  "MVCC + CU"
#  "MVCC (W1)"
#  "MVCC + CU (W1)"
#  "MVCC (W4)"
#  "MVCC + CU (W4)"
)

OCC_BINARIES=(
#  "tpcc_bench" "-occ" "FINE_GRAINED=1 INLINED_VERSIONS=1 OBSERVE_C_BALANCE=1" " + SV + OB"
  "ycsb_bench" "-occ" "FINE_GRAINED=1 INLINED_VERSIONS=1" " + SV"
)
MVCC_BINARIES=(
#  "tpcc_bench" "-mvcc" "SPLIT_TABLE=1 INLINED_VERSIONS=1 OBSERVE_C_BALANCE=1" " + ST + OB"
  "ycsb_bench" "-mvcc" "SPLIT_TABLE=1 INLINED_VERSIONS=1" " + ST"
)
BOTH_BINARIES=(
#  "tpcc_bench" "-both" "INLINED_VERSIONS=1 OBSERVE_C_BALANCE=1" " + OB"
  "ycsb_bench" "-both" "INLINED_VERSIONS=1" ""
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
    preopts=
    if [ $i -eq 1 ]
    then
      preopts="taskset -c 0,2"
    fi
    for f in "${FLAGS[@]}"
    do
      k=0
      while [ $k -lt $ITERS ]
      do
        runs=1
        while [ $runs -le $MAX_RETRIES ]
        do
          cmd="$preopts ./$BINARY -t$i $f"
          printf "\rRun $runs times: $cmd"
          result=$($cmd 2>/tmp/err | tail -n 1 | grep -oE '[0-9.]+')
          sleep 0.5
          #echo "next commit-tid" > /tmp/err  # dry-run
          if [ $(grep 'next commit-tid' /tmp/err | wc -l) -ne 0 ]
          then
            break
          fi
          runs=$(($runs + 1))
        done
        rm /tmp/err
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
      run_bench $OUTFILE $BINARY "$CT_FLAGS" $ITERS $THREADS "${MVCC_FLAGS[@]}" "${MVCC_LABELS[@]}"
    else
      printf "Running OCC on $BINARY$CT_FLAGS\n"
      run_bench $OUTFILE $BINARY "$CT_FLAGS" $ITERS $THREADS "${OCC_FLAGS[@]}" "${OCC_LABELS[@]}"
    fi
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
  seconds=$(($sets * (${#THREADS[@]} * $ITERS * 15 + 180) * 3))
  minutes=$(($seconds / 60 % 60))
  hours=$(($seconds / 3600 % 24))
  days=$(($seconds / 86400))
  seconds=$(($seconds % 60))
  echo "Estimated runtime: $days:$hours:$minutes:$seconds"
}

estimate_runtime $(((${#OCC_BINARIES[@]} + ${#MVCC_BINARIES[@]} + 2 * ${#BOTH_BINARIES[@]}) / 3))

compile "${OCC_BINARIES[@]}" "${MVCC_BINARIES[@]}" "${BOTH_BINARIES[@]}"

rm -rf results
mkdir results
RFILE=results/results.txt

# Run OCC
run 0 "${OCC_BINARIES[@]}" "${BOTH_BINARIES[@]}"

# Run MVCC
run 1 "${MVCC_BINARIES[@]}" "${BOTH_BINARIES[@]}"
