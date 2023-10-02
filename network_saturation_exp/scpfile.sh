#!/bin/bash

scp ./training_example.py remote:~/ &

for((i=2; i<=32; i++)); do
    # ssh worker$i "mkdir -p ~/data"
    scp ./training_example.py worker$i:~/ &
done
wait

# scp ./DASH.py ./mpi_module.so ./training_example.py remote:~/ &

# for((i=2; i<=32; i++)); do
#     # ssh worker$i "mkdir -p ~/data"
#     scp ./DASH.py ./mpi_module.so ./training_example.py worker$i:~/ &
# done
# wait

# for((i=2;i<=32;i++)); do
#   ssh worker$i "mkdir -p ~/data"
#   scp ./data/cifar-10-python.tar.gz worker$i:~/data/ &
# done
# ssh remote "mkdir -p ~/data"
# scp ./data/cifar-10-python.tar.gz remote:~/data/ &
# wait
# echo "scp1 done."

# for((i=2;i<=32;i++)); do
#   scp ./download.py worker$i:~/ &
# done
# scp ./download.py remote:~/ &
# wait
# echo "scp2 done."

# for((i=2;i<=32;i++)); do
#   ssh worker$i "python3 download.py" &
# done
# ssh remote "python3 download.py" &
# wait
# echo "download done."

# for((i=2;i<=32;i++)); do
#   ssh worker$i "sudo apt update && sudo apt install iperf" &
# done
# ssh remote "sudo apt update && sudo apt install iperf" &
# wait
