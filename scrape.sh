#!/bin/bash

while :
do
    date
    for row in 00 `seq 0 10`; do
        for letter in a b c d e f g h; do
            host="cslab$row$letter"
            echo $host
            ssh -o ConnectTimeout=10 $host who 2>/dev/null
        done
    done
    sleep 300
done
