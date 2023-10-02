#!/bin/bash

REMOTE="remote4"

# scp ./training_example.py $REMOTE:~/ &

# for((i=2; i<=32; i++)); do
#     # ssh worker$i "mkdir -p ~/data"
#     scp ./training_example.py worker$i:~/ &
# done
# wait

scp ./DASH.py ./mpi_module.so ./training_example.py $REMOTE:~/ &

# for((i=2; i<=32; i++)); do
#     # ssh worker$i "mkdir -p ~/data"
#     scp ./DASH.py ./mpi_module.so ./training_example.py worker$i:~/ &
# done
wait

# for((i=2;i<=32;i++)); do
#   ssh worker$i "mkdir -p ~/data"
#   scp ./data/cifar-10-python.tar.gz worker$i:~/data/ &
# done
ssh $REMOTE "mkdir -p ~/data"
scp ./data/cifar-10-python.tar.gz $REMOTE:~/data/ &
wait
echo "scp1 done."

# for((i=2;i<=32;i++)); do
#   scp ./download.py worker$i:~/ &
# done
scp ./download.py $REMOTE:~/ &
wait
echo "scp2 done."

# for((i=2;i<=32;i++)); do
#   ssh worker$i "python3 download.py" &
# done
ssh $REMOTE "python3 download.py" &
wait
echo "download done."

# for((i=1;i<=32;i++)); do
#   ssh worker$i "sudo apt update && sudo apt install iperf" &
# done
ssh $REMOTE "sudo apt update && sudo apt install iperf" &
wait
echo "install done."