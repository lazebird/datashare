#!/bin/bash

build() {
    wget https://code.aliyun.com/lazebird/datashare/raw/master/scrt/linux/libssl1.0.0_1.0.1t1+deb8u12_amd64.deb || exit 1
    apt install ./libssl1.0.0_1.0.1t1+deb8u12_amd64.deb -y || exit 1
}

clean() {
    apt remove --purge -y libssl1.0.0* || exit 1
}

case $1 in
build)
    build
    ;;
clean)
    clean
    ;;
*) #echo "Please make sure the option is start/stop."
    clean
    build
    ;;
esac
