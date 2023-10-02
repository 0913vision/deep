#!/bin/bash

WORKERS=(12)


for i in ${WORKERS[@]}; do
  ssh-keygen -R remote
  ssh remote "mkdir -p ~/data"
  scp ./data/cifar-10-python.tar.gz remote:~/data/ &
done
wait
echo "scp1 done."

for i in ${WORKERS[@]}; do
  scp ./download.py ./train.py remote:~/ &
done
wait
echo "scp2 done."

for i in ${WORKERS[@]}; do
  ssh remote "python3 download.py" &
done
wait
echo "download done."
