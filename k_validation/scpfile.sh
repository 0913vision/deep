#!/bin/bash


for((i=2; i<=32; i++)); do
    scp ./train.py ./download.py worker$i:~/ &
done
wait

for((i=2;i<=32;i++)); do
  ssh worker$i "mkdir -p ~/data"
  scp ./data/cifar-10-python.tar.gz worker$i:~/data/ &
done
wait

for((i=2;i<=32;i++)); do
  ssh worker$i "python3 download.py" &
done
wait