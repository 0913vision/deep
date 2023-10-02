#!/bin/bash

WORKERS=(10)


for i in ${WORKERS[@]}; do
  ssh-keygen -R worker$i
  ssh worker$i "mkdir -p ~/data"
  scp ./data/cifar-10-python.tar.gz worker$i:~/data/ &
done
wait
echo "scp1 done."

for i in ${WORKERS[@]}; do
  scp ./download.py ./training_example.py ./DASH.py ./mpi_module.so worker$i:~/ &
done
wait
echo "scp2 done."

for i in ${WORKERS[@]}; do
  ssh worker$i "python3 download.py" &
done
wait
echo "download done."

for i in ${WORKERS[@]}; do
  ssh worker$i "sudo apt update && sudo apt install iperf" &
done
wait
echo "install done."
