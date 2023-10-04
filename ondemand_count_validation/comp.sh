#!/bin/bash

file="exp_$1.txt"

grep -E '\[serialization\]|\[sending\]' "$file" &> /dev/null
if [ $? -eq 0 ]; then
    echo "=== $file ==="
    grep -E '\[serialization\]|\[sending\]' "$file"
    echo "=================="
fi
