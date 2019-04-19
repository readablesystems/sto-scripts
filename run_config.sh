#!/bin/bash

## Experiment setup documentation
#
# (Sorted in lexicographical order by setup function name)
#
# setup_rubis: RUBiS
# setup_tpcc: TPC-C, 1 and 4 warehouses
# setup_tpcc_opacity: TPC-C with opacity, 1 and 4 warehouses
# setup_tpcc_safe_flatten: TPC-C with safer flattening MVCC, 1 and 4 warehouses
# setup_tpcc_scaled: TPC-C, #warehouses = #threads
# setup_tpcc_gc: TPC-C, 1 warehouse and #wh = #th, gc cycle of 1ms, 100ms, 10s (off)
# setup_wiki: Wikipedia
# setup_ycsba: YCSB-A
# setup_ycsbb: YCSB-B
# setup_ycsbc: YCSB-C

setup_rubis() {
  EXPERIMENT_NAME="RUBiS"

  RUBIS_OCC=(
    "OCC"         "-idefault -s1.0 -g"
    "OCC + CU"    "-idefault -s1.0 -g -x"
  )

  RUBIS_MVCC=(
    "MVCC"        "-imvcc -s1.0 -g"
    "MVCC + CU"   "-imvcc -s1.0 -g -x"
  )

  RUBIS_OCC_BINARIES=(
    "rubis_bench" "-occ" "NDEBUG=1 FINE_GRAINED=1" " + SV"
  )
  RUBIS_MVCC_BINARIES=(
    "rubis_bench" "-mvcc" "NDEBUG=1 SPLIT_TABLE=1 INLINED_VERSIONS=1" " + ST"
  )
  RUBIS_BOTH_BINARIES=(
    "rubis_bench" "-both" "NDEBUG=1 INLINED_VERSIONS=1" ""
  )

  OCC_LABELS=("${RUBIS_OCC[@]}")
  MVCC_LABELS=("${RUBIS_MVCC[@]}")
  OCC_BINARIES=("${RUBIS_OCC_BINARIES[@]}" "${RUBIS_BOTH_BINARIES[@]}")
  MVCC_BINARIES=("${RUBIS_MVCC_BINARIES[@]}" "${RUBIS_BOTH_BINARIES[@]}")

  call_runs() {
    default_call_runs
  }

  update_cmd() {
    ``  # noop
  }
}

setup_tpcc() {
  EXPERIMENT_NAME="TPC-C"

  TPCC_OCC=(
    "OCC (W1)"         "-idefault -g -w1"
    "OCC + CU (W1)"    "-idefault -g -x -w1"
    "OCC (W4)"         "-idefault -g -w4"
    "OCC + CU (W4)"    "-idefault -g -x -w4"
    "OCC (W0)"         "-idefault -g"
    "OCC + CU (W0)"    "-idefault -g -x"
  )

  TPCC_MVCC=(
    "MVCC (W1)"        "-imvcc -g -w1"
    "MVCC + CU (W1)"   "-imvcc -g -x -w1"
    "MVCC (W4)"        "-imvcc -g -w4"
    "MVCC + CU (W4)"   "-imvcc -g -x -w4"
    "MVCC (W0)"        "-imvcc -g"
    "MVCC + CU (W0)"   "-imvcc -g -x"
  )

  TPCC_OCC_BINARIES=(
    "tpcc_bench" "-occ" "NDEBUG=1 OBSERVE_C_BALANCE=1 FINE_GRAINED=1" " + SV"
  )
  TPCC_MVCC_BINARIES=(
    "tpcc_bench" "-mvcc" "NDEBUG=1 OBSERVE_C_BALANCE=1 SPLIT_TABLE=1 INLINED_VERSIONS=1" " + ST"
  )
  TPCC_BOTH_BINARIES=(
    "tpcc_bench" "-both" "NDEBUG=1 OBSERVE_C_BALANCE=1 INLINED_VERSIONS=1" ""
  )

  OCC_LABELS=("${TPCC_OCC[@]}")
  MVCC_LABELS=("${TPCC_MVCC[@]}")
  OCC_BINARIES=("${TPCC_OCC_BINARIES[@]}" "${TPCC_BOTH_BINARIES[@]}")
  MVCC_BINARIES=("${TPCC_MVCC_BINARIES[@]}" "${TPCC_BOTH_BINARIES[@]}")

  call_runs() {
    default_call_runs
  }

  update_cmd() {
    if [[ $cmd != *"-w"* ]]
    then
      cmd="$cmd -w$i"
    fi
  }
}

setup_tpcc_occ() {
  EXPERIMENT_NAME="TPC-C OCC"

  TPCC_OCC=(
    "OCC (W1)"         "-idefault -g -w1"
    "OCC + CU (W1)"    "-idefault -g -x -w1"
    "OCC (W4)"         "-idefault -g -w4"
    "OCC + CU (W4)"    "-idefault -g -x -w4"
    "OCC (W0)"         "-idefault -g"
    "OCC + CU (W0)"    "-idefault -g -x"
  )

  TPCC_MVCC=(
  )

  TPCC_OCC_BINARIES=(
    "tpcc_bench" "-occ" "NDEBUG=1 OBSERVE_C_BALANCE=1 FINE_GRAINED=1" " + SV"
  )
  TPCC_MVCC_BINARIES=(
  )
  TPCC_BOTH_BINARIES=(
    "tpcc_bench" "-both" "NDEBUG=1 OBSERVE_C_BALANCE=1 INLINED_VERSIONS=1" ""
  )

  OCC_LABELS=("${TPCC_OCC[@]}")
  MVCC_LABELS=()
  OCC_BINARIES=("${TPCC_OCC_BINARIES[@]}" "${TPCC_BOTH_BINARIES[@]}")
  MVCC_BINARIES=()

  call_runs() {
    default_call_runs
  }

  update_cmd() {
    if [[ $cmd != *"-w"* ]]
    then
      cmd="$cmd -w$i"
    fi
  }
}

setup_tpcc_mvcc() {
  EXPERIMENT_NAME="TPC-C MVCC"

  TPCC_OCC=(
  )

  TPCC_MVCC=(
    "MVCC (W1)"        "-imvcc -g -w1"
    "MVCC + CU (W1)"   "-imvcc -g -x -w1"
    "MVCC (W4)"        "-imvcc -g -w4"
    "MVCC + CU (W4)"   "-imvcc -g -x -w4"
    "MVCC (W0)"        "-imvcc -g"
    "MVCC + CU (W0)"   "-imvcc -g -x"
  )

  TPCC_OCC_BINARIES=(
  )
  TPCC_MVCC_BINARIES=(
    "tpcc_bench" "-mvcc" "NDEBUG=1 OBSERVE_C_BALANCE=1 SPLIT_TABLE=1 INLINED_VERSIONS=1" " + ST"
  )
  TPCC_BOTH_BINARIES=(
    "tpcc_bench" "-both" "NDEBUG=1 OBSERVE_C_BALANCE=1 INLINED_VERSIONS=1" ""
  )

  OCC_LABELS=()
  MVCC_LABELS=("${TPCC_MVCC[@]}")
  OCC_BINARIES=()
  MVCC_BINARIES=("${TPCC_MVCC_BINARIES[@]}" "${TPCC_BOTH_BINARIES[@]}")

  call_runs() {
    default_call_runs
  }

  update_cmd() {
    if [[ $cmd != *"-w"* ]]
    then
      cmd="$cmd -w$i"
    fi
  }
}

setup_tpcc_opacity() {
  EXPERIMENT_NAME="TPC-C with Opacity"

  TPCC_OCC=(
    "OPQ (W1)"         "-iopaque -g -w1"
    "OPQ + CU (W1)"    "-iopaque -g -w1 -x"
    "OPQ (W4)"         "-iopaque -g -w4"
    "OPQ + CU (W4)"    "-iopaque -g -x -w4"
    "OPQ (W0)"         "-iopaque -g"
    "OPQ + CU (W0)"    "-iopaque -g -x"
  )

  TPCC_MVCC=(
  )

  TPCC_OCC_BINARIES=(
    "tpcc_bench" "-occ" "NDEBUG=1 OBSERVE_C_BALANCE=1 FINE_GRAINED=1" " + SV"
  )
  TPCC_MVCC_BINARIES=(
  )
  TPCC_BOTH_BINARIES=(
    "tpcc_bench" "-both" "NDEBUG=1 OBSERVE_C_BALANCE=1" ""
  )

  OCC_LABELS=("${TPCC_OCC[@]}")
  MVCC_LABELS=()
  OCC_BINARIES=("${TPCC_OCC_BINARIES[@]}" "${TPCC_BOTH_BINARIES[@]}")
  MVCC_BINARIES=()

  call_runs() {
    default_call_runs
  }

  update_cmd() {
    if [[ $cmd != *"-w"* ]]
    then
      cmd="$cmd -w$i"
    fi
  }
}

setup_tpcc_tictoc() {
  EXPERIMENT_NAME="TPC-C TicToc"

  TPCC_OCC=(
    "TicToc (W1)"         "-itictoc -g -w1"
    "TicToc (W4)"         "-itictoc -g -w4"
    "TicToc (W0)"         "-itictoc -g"
  )

  TPCC_MVCC=(
  )

  TPCC_OCC_BINARIES=(
  )
  TPCC_MVCC_BINARIES=(
  )
  TPCC_BOTH_BINARIES=(
    "tpcc_bench" "-both" "NDEBUG=1 OBSERVE_C_BALANCE=1" ""
  )

  OCC_LABELS=("${TPCC_OCC[@]}")
  MVCC_LABELS=()
  OCC_BINARIES=("${TPCC_BOTH_BINARIES[@]}")
  MVCC_BINARIES=()

  call_runs() {
    default_call_runs
  }

  update_cmd() {
    if [[ $cmd != *"-w"* ]]
    then
      cmd="$cmd -w$i"
    fi
  }
}

setup_tpcc_safe_flatten() {
  EXPERIMENT_NAME="TPC-C MVCC aborting unsafe flattens in CU"

  TPCC_OCC=(
  )

  TPCC_MVCC=(
    "MVCC (W1)"         "-imvcc -g -w1"
    "MVCC + CU (W1)"    "-imvcc -g -w1 -x"
    "MVCC (W4)"         "-imvcc -g -w4"
    "MVCC + CU (W4)"    "-imvcc -g -x -w4"
    "MVCC (W0)"         "-imvcc -g"
    "MVCC + CU (W0)"    "-imvcc -g -x"
  )

  TPCC_OCC_BINARIES=(
  )
  TPCC_MVCC_BINARIES=(
    "tpcc_bench" "-mvcc" "NDEBUG=1 INLINED_VERSIONS=1 SPLIT_TABLE=1 OBSERVE_C_BALANCE=1 SAFE_FLATTEN=1" " + ST"
  )
  TPCC_BOTH_BINARIES=(
    "tpcc_bench" "-both" "NDEBUG=1 INLINED_VERSIONS=1 OBSERVE_C_BALANCE=1 SAFE_FLATTEN=1" ""
  )

  OCC_LABELS=()
  MVCC_LABELS=("${TPCC_MVCC[@]}")
  OCC_BINARIES=()
  MVCC_BINARIES=("${TPCC_MVCC_BINARIES[@]}" "${TPCC_BOTH_BINARIES[@]}")

  call_runs() {
    default_call_runs
  }

  update_cmd() {
    if [[ $cmd != *"-w"* ]]
    then
      cmd="$cmd -w$i"
    fi
  }
}

setup_tpcc_scaled() {
  EXPERIMENT_NAME="TPC-C, #W = #T"

  TPCC_OCC=(
    "OCC (W0)"         "-idefault -g"
    "OCC + CU (W0)"    "-idefault -g -x"
    "OPQ (W0)"         "-iopaque -g"
    "OPQ +CU (W0)"     "-iopaque -g -x"
  )

  TPCC_MVCC=(
    "MVCC (W0)"        "-imvcc -g"
    "MVCC +CU (W0)"    "-imvcc -g -x"
  )

  TPCC_OCC_BINARIES=(
    "tpcc_bench" "-occ" "NDEBUG=1 OBSERVE_C_BALANCE=1 FINE_GRAINED=1" " + SV"
  )
  TPCC_MVCC_BINARIES=(
    "tpcc_bench" "-mvcc" "NDEBUG=1 OBSERVE_C_BALANCE=1 SPLIT_TABLE=1 INLINED_VERSIONS=1" " + ST"
  )
  TPCC_BOTH_BINARIES=(
    "tpcc_bench" "-both" "NDEBUG=1 OBSERVE_C_BALANCE=1 INLINED_VERSIONS=1" ""
  )

  OCC_LABELS=("${TPCC_OCC[@]}")
  MVCC_LABELS=("${TPCC_MVCC[@]}")
  OCC_BINARIES=("${TPCC_OCC_BINARIES[@]}" "${TPCC_BOTH_BINARIES[@]}")
  MVCC_BINARIES=("${TPCC_MVCC_BINARIES[@]}" "${TPCC_BOTH_BINARIES[@]}")

  call_runs() {
    default_call_runs
  }

  update_cmd() {
    cmd="$cmd -w$i"
  }
}

setup_tpcc_gc() {
  EXPERIMENT_NAME="TPC-C, variable GC"

  TPCC_OCC=(
  )

  TPCC_MVCC=(
    "MVCC (W1, R1000)"     "-imvcc -g -r1000 -w1"
    "MVCC (W0, R1000)"     "-imvcc -g -r1000"
    "MVCC (W1, R100000)"   "-imvcc -g -r100000 -w1"
    "MVCC (W0, R100000)"   "-imvcc -g -r100000"
    "MVCC (W1, R0)"        "-imvcc -w1"
    "MVCC (W0, R0)"        "-imvcc"
  )

  TPCC_OCC_BINARIES=(
  )
  TPCC_MVCC_BINARIES=(
  )
  TPCC_BOTH_BINARIES=(
    "tpcc_bench" "-both" "DEBUG=1 OBSERVE_C_BALANCE=1 INLINED_VERSIONS=1" ""
  )

  OCC_LABELS=("${TPCC_OCC[@]}")
  MVCC_LABELS=("${TPCC_MVCC[@]}")
  OCC_BINARIES=("${TPCC_OCC_BINARIES[@]}" "${TPCC_BOTH_BINARIES[@]}")
  MVCC_BINARIES=("${TPCC_MVCC_BINARIES[@]}" "${TPCC_BOTH_BINARIES[@]}")

  call_runs() {
    default_call_runs
  }

  update_cmd() {
    if [[ $cmd != *"-w"* ]]
    then
      cmd="$cmd -w$i"
    fi
  }
}

setup_wiki() {
  EXPERIMENT_NAME="Wikipedia"

  WIKI_OCC=(
    "OCC"         "-idefault -b"
    "OCC + CU"    "-idefault -b -x"
  )

  WIKI_MVCC=(
    "MVCC"        "-imvcc -b"
    "MVCC + CU"   "-imvcc -b -x"
  )

  WIKI_OCC_BINARIES=(
    "wiki_bench" "-occ" "NDEBUG=1 FINE_GRAINED=1" " + SV"
  )
  WIKI_MVCC_BINARIES=(
    "wiki_bench" "-mvcc" "NDEBUG=1 SPLIT_TABLE=1 INLINED_VERSIONS=1" " + ST"
  )
  WIKI_BOTH_BINARIES=(
    "wiki_bench" "-both" "NDEBUG=1 INLINED_VERSIONS=1" ""
  )

  OCC_LABELS=("${WIKI_OCC[@]}")
  MVCC_LABELS=("${WIKI_MVCC[@]}")
  OCC_BINARIES=("${WIKI_OCC_BINARIES[@]}" "${WIKI_BOTH_BINARIES[@]}")
  MVCC_BINARIES=("${WIKI_MVCC_BINARIES[@]}" "${WIKI_BOTH_BINARIES[@]}")

  call_runs() {
    default_call_runs
  }

  update_cmd() {
    ``  # noop
  }
}

setup_ycsba() {
  EXPERIMENT_NAME="YCSB-A"
  TIMEOUT=60

  YCSB_OCC=(
    "OCC (A)"         "-mA -idefault -g"
    "OCC (A) + CU"    "-mA -idefault -g -x"
  )

  YCSB_MVCC=(
    "MVCC (A)"        "-mA -imvcc -g"
    "MVCC (A) + CU"   "-mA -imvcc -g -x"
  )

  YCSB_OCC_BINARIES=(
    "ycsb_bench" "-occ" "NDEBUG=1 FINE_GRAINED=1" " + SV"
  )
  YCSB_MVCC_BINARIES=(
    "ycsb_bench" "-mvcc" "NDEBUG=1 SPLIT_TABLE=1 INLINED_VERSIONS=1" " + ST"
  )
  YCSB_BOTH_BINARIES=(
    "ycsb_bench" "-both" "NDEBUG=1 INLINED_VERSIONS=1" ""
  )

  OCC_LABELS=("${YCSB_OCC[@]}")
  MVCC_LABELS=("${YCSB_MVCC[@]}")
  OCC_BINARIES=("${YCSB_OCC_BINARIES[@]}" "${YCSB_BOTH_BINARIES[@]}")
  MVCC_BINARIES=("${YCSB_MVCC_BINARIES[@]}" "${YCSB_BOTH_BINARIES[@]}")

  call_runs() {
    default_call_runs
  }

  update_cmd() {
    ``  # noop
  }
}

setup_ycsbb() {
  EXPERIMENT_NAME="YCSB-B"
  TIMEOUT=60

  YCSB_OCC=(
    "OCC (B)"         "-mB -idefault -g"
    "OCC (B) + CU"    "-mB -idefault -g -x"
  )

  YCSB_MVCC=(
    "MVCC (B)"        "-mB -imvcc -g"
    "MVCC (B) + CU"   "-mB -imvcc -g -x"
  )

  YCSB_OCC_BINARIES=(
    "ycsb_bench" "-occ" "NDEBUG=1 FINE_GRAINED=1" " + SV"
  )
  YCSB_MVCC_BINARIES=(
    "ycsb_bench" "-mvcc" "NDEBUG=1 SPLIT_TABLE=1 INLINED_VERSIONS=1" " + ST"
  )
  YCSB_BOTH_BINARIES=(
    "ycsb_bench" "-both" "NDEBUG=1 INLINED_VERSIONS=1" ""
  )

  OCC_LABELS=("${YCSB_OCC[@]}")
  MVCC_LABELS=("${YCSB_MVCC[@]}")
  OCC_BINARIES=("${YCSB_OCC_BINARIES[@]}" "${YCSB_BOTH_BINARIES[@]}")
  MVCC_BINARIES=("${YCSB_MVCC_BINARIES[@]}" "${YCSB_BOTH_BINARIES[@]}")

  call_runs() {
    default_call_runs
  }

  update_cmd() {
    ``  # noop
  }
}

setup_ycsbc() {
  EXPERIMENT_NAME="YCSB-C"
  TIMEOUT=60

  YCSB_OCC=(
    "OCC (C)"         "-mC -idefault -g"
    "OCC (C) + CU"    "-mC -idefault -g -x"
  )

  YCSB_MVCC=(
    "MVCC (C)"        "-mC -imvcc -g"
    "MVCC (C) + CU"   "-mC -imvcc -g -x"
  )

  YCSB_OCC_BINARIES=(
    "ycsb_bench" "-occ" "NDEBUG=1 FINE_GRAINED=1" " + SV"
  )
  YCSB_MVCC_BINARIES=(
    "ycsb_bench" "-mvcc" "NDEBUG=1 SPLIT_TABLE=1 INLINED_VERSIONS=1" " + ST"
  )
  YCSB_BOTH_BINARIES=(
    "ycsb_bench" "-both" "NDEBUG=1 INLINED_VERSIONS=1" ""
  )

  OCC_LABELS=("${YCSB_OCC[@]}")
  MVCC_LABELS=("${YCSB_MVCC[@]}")
  OCC_BINARIES=("${YCSB_OCC_BINARIES[@]}" "${YCSB_BOTH_BINARIES[@]}")
  MVCC_BINARIES=("${YCSB_MVCC_BINARIES[@]}" "${YCSB_BOTH_BINARIES[@]}")

  call_runs() {
    default_call_runs
  }

  update_cmd() {
    ``  # noop
  }
}
