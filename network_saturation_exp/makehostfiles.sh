#!/bin/bash

NODES=(1 2 4 8 12 16 20 24 28 32)
REMOTE="remote4"

rm -rf ./hostfiles
mkdir -p ./hostfiles

for k in ${NODES[@]}; do
  for((i=1;i<=k;i++)); do
    echo "worker$i slots=1" >> ./hostfiles/hosts$k
  done
  echo "$REMOTE slots=1" >> ./hostfiles/hosts$k
done