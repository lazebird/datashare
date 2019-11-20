# !/bin/bash

dirname="/tmp/clash/"
tarname="clash-linux-mipsle-v0.15.0.gz"
binname="clash-linux-mipsle"
pkill $binname
rm -rf $dirname && mkdir $dirname && cd $dirname
cp -a /home/root/config.yml ./
loop=true
while $loop; do
    # wget https://github.com/Dreamacro/clash/releases/download/v0.15.0/$tarname && tar -xf $tarname && rm -f $tarname
    wget https://code.aliyun.com/lazebird/datashare/raw/master/proxy/$binname
    if [ $? -eq 0 ]; then
        loop=false
    fi
done
chmod 777 $binname && ./$binname -d . &
