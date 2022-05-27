#!/bin/bash
# [libssl.so.1.0.0下载安装](https://packages.debian.org/jessie/amd64/libssl1.0.0/download)
TARGET=libssl1.0.0_1.0.1t-1+deb8u12_amd64.deb

build() {
    test -f ${TARGET} || wget https://code.aliyun.com/lazebird/datashare/raw/master/scrt/linux/${TARGET} || exit 1
    apt install ./${TARGET} -y || exit 1
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
