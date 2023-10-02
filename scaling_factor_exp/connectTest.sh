#!/bin/bash

for i in {1..32}
do
  ssh -o ConnectTimeout=3 worker$i "exit" &> /dev/null
  if [ $? -ne 0 ]; then
    echo "Connection to worker$i failed"
  fi
done

