#!/bin/bash

# ippre="192.168.10."
# ipsufs=($(seq 40 1 64))
ippre="192.168.1."
ipsufs=(95 98)

del_log() {
    (
        sleep 1s
        echo "admin"
        sleep 1s
        echo "admin"
        sleep 2s
        echo "entershell"
        echo "rm -rf /var/log/*"
        echo "reboot"
        sleep 3s
    ) | telnet $1 > $1.result
}

for ipsuf in ${ipsufs[@]}; do
    del_log $ippre$ipsuf &
done
wait
cat *.result | grep "Connected to" | awk -F " " '{print $3}' > alive.result
echo "alive host below:"
cat alive.result
rm -f *.result
