#!/bin/bash
REMOTES=2

IP=$(hostname -I | awk '{print $1}')
# NP = # of TRAINING NODES + # of REMOTE NODES
mpirun \
-np $((32+REMOTES)) \
-hostfile hosts$REMOTES \
python3 ./training_example.py \
5 1 \
32 $REMOTES \
$IP 1234 \
--batch_size 128 \
--shard_size 32 \
--remote_buffer_size 2 \
--model_name my_model \
--file_name_include_datetime False \
--file_save_in_dictionary False \
| tee exp_$REMOTES.txt


