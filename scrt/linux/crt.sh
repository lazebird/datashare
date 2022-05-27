#!/bin/bash
# [Ubuntu18.04下安装 并破解 SecureCRT8.5 的方法记录](https://www.tuziang.com/combat/1237.html)

TARGET=scrt-sfx-8.5.3 # scrt-9.2.1
TARNAME=scrt-sfx-8.5.3.1867.ubuntu18-64.tar.gz
test -f ${TARNAME} || wget -O ${TARNAME} https://code.aliyun.com/lazebird/datashare/raw/master/scrt/linux/${TARNAME} || exit 1
test -d ${TARGET} || tar -xf ${TARNAME} || exit 1

(test -f libssl.sh || wget https://code.aliyun.com/lazebird/datashare/raw/master/scrt/linux/libssl.sh) || exit 1
(test -f jpeg.sh || wget https://code.aliyun.com/lazebird/datashare/raw/master/scrt/linux/jpeg.sh) || exit 1

build() {
    sh libssl.sh build
    sh jpeg.sh build
    chmod u+x ${TARGET}/SecureCRT || exit 1
    mkdir -p /opt/ && mv ${TARGET}/ /opt/ || exit 1
    wget https://code.aliyun.com/lazebird/datashare/raw/master/scrt/linux/securecrt_linux_crack.pl || exit 1
    sudo perl securecrt_linux_crack.pl /opt/${TARGET}/SecureCRT | tee crt_reg.txt
}

clean() {
    sh libssl.sh clean
    sh jpeg.sh clean
    rm -rf /opt/${TARGET}/
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
