#!/bin/bash
NODES=(1 2 4 8 12 16 20 24 28 32)
IP=$(hostname -I | awk '{print $1}')
PORT=6133
REMOTEINS="c4-xlarge"
FILE="bandwidth.txt"

for((k=1; k<=5; k++)); do
    ssh remote2 "iperf -s > /dev/null 2>&1 & echo \$! > /tmp/iperf_pid" &

    ./networkbd.sh

    awk '/Mbits\/sec/ { sum += $7; count++ }
     /Gbits\/sec/ { sum += $7*1000; count++ } 
     END { print "Average:", sum/count, "Mbits/sec" }' $FILE >> bwlog.result

    IPERF_PID=$(ssh remote2 "cat /tmp/iperf_pid")
    ssh remote2 "kill $IPERF_PID"
    ssh remote2 "rm /tmp/iperf_pid"

    rm $FILE

    for NODE in ${NODES[@]}; do
        echo "shard size = $NODE"
        # NP = # of TRAINING NODES + 1 (REMOTE NODE)
        mpirun \
        -np $((NODE+1)) \
        -hostfile ./hostfiles/hosts$NODE \
        python3 ~/training_example.py \
        3 1 $IP $PORT \
        --batch_size 128 \
        --shard_size $NODE \
        --remote_buffer_size 2 \
        --model_name resnet152 \
        | tee "1002exp_result_${NODE}_nodes_${REMOTEINS}.txt"
        
        PORT=$((PORT+1))
    done
    ./comp.sh > "comp_${REMOTEINS}_${k}.result"
    rm ./*.txt
    sleep 60
done

