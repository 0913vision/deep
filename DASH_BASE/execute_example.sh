#!/bin/bash
IP=$(hostname -I | awk '{print $1}')
# NP = # of TRAINING NODES + # of REMOTE NODES
mpirun \
-np 11 \
-hostfile hosts \
python3 ./training_example.py \
3 1 \
8 3 \
$IP 1234 \
--batch_size 128 \
--shard_size 8 \
--remote_buffer_size 2 \
--model_name my_model \
--file_name_include_datetime True \
--file_save_in_dictionary True \
| tee my_model.result
