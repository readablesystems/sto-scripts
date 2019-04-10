#!/bin/bash

## Experiment setup documentation
#
# (Sorted in lexicographical order by setup function name)
#
# setup_rubic: RUBiS
# setup_tpcc: TPC-C, 1 and 4 warehouses
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
}

setup_tpcc() {
  EXPERIMENT_NAME="TPC-C"

  TPCC_OCC=(
    "OCC (W1)"         "-idefault -g"
    "OCC + CU (W1)"    "-idefault -g -x"
    "OCC (W4)"         "-idefault -g -w4"
    "OCC + CU (W4)"    "-idefault -g -x -w4"
  )

  TPCC_MVCC=(
    "MVCC (W1)"        "-imvcc -g"
    "MVCC + CU (W1)"   "-imvcc -g -x"
    "MVCC (W4)"        "-imvcc -g -w4"
    "MVCC + CU (W4)"   "-imvcc -g -x -w4"
  )

  TPCC_OCC_BINARIES=(
    "tpcc_bench" "-occ" "NDEBUG=1 FINE_GRAINED=1" " + SV"
  )
  TPCC_MVCC_BINARIES=(
    "tpcc_bench" "-mvcc" "NDEBUG=1 SPLIT_TABLE=1 INLINED_VERSIONS=1" " + ST"
  )
  TPCC_BOTH_BINARIES=(
    "tpcc_bench" "-both" "NDEBUG=1 INLINED_VERSIONS=1" ""
  )

  OCC_LABELS=("${TPCC_OCC[@]}")
  MVCC_LABELS=("${TPCC_MVCC[@]}")
  OCC_BINARIES=("${TPCC_OCC_BINARIES[@]}" "${TPCC_BOTH_BINARIES[@]}")
  MVCC_BINARIES=("${TPCC_MVCC_BINARIES[@]}" "${TPCC_BOTH_BINARIES[@]}")

  call_runs() {
    default_call_runs
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
}

setup_ycsba() {
  EXPERIMENT_NAME="YCSB-A"

  YCSB_OCC=(
    "OCC"         "-mA -idefault -g"
    "OCC + CU"    "-mA -idefault -g -x"
  )

  YCSB_MVCC=(
    "MVCC"        "-mA -imvcc -g"
    "MVCC + CU"   "-mA -imvcc -g -x"
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
}

setup_ycsbb() {
  EXPERIMENT_NAME="YCSB-B"

  YCSB_OCC=(
    "OCC"         "-mB -idefault -g"
    "OCC + CU"    "-mB -idefault -g -x"
  )

  YCSB_MVCC=(
    "MVCC"        "-mB -imvcc -g"
    "MVCC + CU"   "-mB -imvcc -g -x"
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
}

setup_ycsbc() {
  EXPERIMENT_NAME="YCSB-C"

  YCSB_OCC=(
    "OCC"         "-mC -idefault -g"
    "OCC + CU"    "-mC -idefault -g -x"
  )

  YCSB_MVCC=(
    "MVCC"        "-mC -imvcc -g"
    "MVCC + CU"   "-mC -imvcc -g -x"
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
}
