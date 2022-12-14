#!/bin/bash
# [启动secureCRT报错 libjpeg.so.8: cannot open shared object file: No such file or direct](https://blog.csdn.net/HYESC/article/details/88238242)

TARGET=jpeg-8d1
TARNAME=${TARGET}.tar.gz
test -f ${TARNAME} || wget https://code.aliyun.com/lazebird/datashare/raw/master/scrt/linux/${TARNAME} || exit 1
test -d ${TARGET} || tar -xf ${TARNAME} || exit 1
cd ${TARGET}

build() {
    ./configure && make -j || exit 1
    make install || exit 1
}

clean() {
    make uninstall && make distclean || exit 1
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
