#!/bin/bash

if [ "$1" == "" ]; then
  echo "Must pass in a directory path as a parameter.";
  exit 1;
fi

printf "$(for f in $(ls -d "$1"/*.txt); do head -n1 $f | grep -oE '[^,]*\[T1\]' | grep -oE '^[^\[(]*' | sed -e 's/[[:space:]]*$//'; done)" | sort | uniq;
