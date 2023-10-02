#!/bin/bash
for file in *.txt; do
    grep -E '\[serialization\]|\[sending\]' "$file" &> /dev/null
    if [ $? -eq 0 ]; then
        echo "=== $file ==="
        grep -E '\[serialization\]|\[sending\]' "$file"
        echo "=================="
    fi
done
