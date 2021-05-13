#!/bin/bash

apt install wget git -y
apt install lib32z1 -y
apt install build-essential -y
apt install mtd-utils -y
apt install bc texinfo libc6-i386 automake autotools-dev qemu-user-static flex byacc bison -y
apt install u-boot-tools libtool -y
ln -s /usr/bin/aclocal-1.15 /usr/bin/aclocal-1.14
ln -s /usr/bin/make /usr/bin/gmake
wget https://ftp.gnu.org/gnu/automake/automake-1.14.1.tar.xz && tar -xf automake-1.14.1.tar.xz && cd automake-1.14.1 && ./configure && make && make install && cd .. && rm -rf automake-1.14.1*
