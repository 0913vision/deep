#!/bin/bash

FILE="bandwidth.txt"
# rm $FILE

# for((i=1; i<=32; i++)); do
#   ssh worker$i "sudo apt install iperf" &
# done
# # wait
# ssh remote3 "sudo apt install iperf"
# ssh remote3 "iperf -s" &

exec >> $FILE 2>&1
SERVER_IP=$(ssh remote2 "hostname -I")

for((k=0; k<1; k++)); do
  for((i=1; i<=32; i++)); do
    ssh worker$i "iperf -c $SERVER_IP" &
  done
  wait
done

exec > /dev/tty 2>&1

# awk '/Mbits\/sec/ { sum += $7; count++ }
#      /Gbits\/sec/ { sum += $7*1000; count++ } 
#      END { print "Average:", sum/count, "Mbits/sec" }' $FILE