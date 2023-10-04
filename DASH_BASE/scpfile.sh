#!/bin/bash

NUM_WORKERS=8
NUM_REMOTES=3

for((i=2; i<=$NUM_WORKERS;i++)); do
  scp ./DASH_BASE.py ./training_example.py worker$i:~/ &
done
for((i=1; i<=$NUM_REMOTES;i++)); do
  scp ./DASH_BASE.py ./training_example.py remote$i:~/ &
done
wait

# for((i=2; i<=$NUM_WORKERS; i++)); do
#     scp ./training_example.py ./mpi_module.so download.py DASH_BASE.py worker$i:~/ &
# done
# for((i=1; i<=$NUM_REMOTES; i++)); do
#     scp ./training_example.py ./mpi_module.so DASH_BASE.py remote$i:~/ &
# done
# wait
# echo "scp1 done."

# for((i=2;i<=$NUM_WORKERS;i++)); do
#   ssh worker$i "mkdir -p ~/data"
#   scp ./data/cifar-10-python.tar.gz worker$i:~/data/ &
# done
# wait
# echo "scp2 done."

# for((i=2;i<=$NUM_WORKERS;i++)); do
#   ssh worker$i "python3 download.py" &
# done
# wait
# echo "download done."