#!/bin/sh

print_exit() { # parameter: logstr
    echo "$1" >&2 && exit 1
}

fetch_file() { # parameter: filename, path, url, alternate
    filename=$1
    path=$2
    url=$3
    alt=$4
    if [ -f $path/$filename ]; then
        echo "# $path/$filename already exists."
        return
    fi
    wget -q -O $path/$filename $url >/dev/null || (echo "# $path/$filename download failed." >&2 && rm -f $path/$filename && mv $path/$alt $path/$filename 2>/dev/null) || exit 1
    echo "# $path/$filename download success."
}

get_clash() {
    arch=$(uname -m)
    case $arch in
    x86_64)
        fetch_file clash $workdir "https://code.aliyun.com/lazebird/datashare/raw/master/proxy/clash-linux-amd64"
        ;;
    mips)
        fetch_file clash $workdir "https://code.aliyun.com/lazebird/datashare/raw/master/proxy/clash-linux-mipsle-hardfloat"
        ;;
    *)
        print_exit "# unsupportted arch $arch."
        ;;
    esac
}

[ -z "${BASH_SOURCE}" ] && SCRIPTPATH=$0 || SCRIPTPATH=${BASH_SOURCE[0]}
BASHDIR="$(cd "$(dirname "$SCRIPTPATH")" && pwd)"
workdir=${1-"/tmp"}
configname=config.yaml
configbak=config.bak
urlfile=proxyurl.txt
configurl=$(cat $BASHDIR/$urlfile) # secret
[ -z "$configurl" ] && print_exit "#### config url in $BASHDIR/$urlfile is invalid!"

cd $workdir
echo "#### starting proxy temporally in $workdir:"
get_clash && chmod +x clash
fetch_file Country.mmdb $workdir "https://code.aliyun.com/lazebird/datashare/raw/master/proxy/Country.mmdb"
mv $configname $configbak # save last config
fetch_file $configname $workdir "https://code.aliyun.com/lazebird/datashare/raw/master/proxy/config.yaml"
kill $(pgrep clash) 2>/dev/null && sleep 3s
ls $configname >/dev/null && (./clash -d . >proxy.log 2>&1 &) && sleep 1s

echo "#### updating configure files in $workdir:"
mv $configname $configname".bak" 2>/dev/null # save empty config
fetch_file $configname $workdir $configurl $configbak
fetch_file reconf.lua $workdir "https://code.aliyun.com/lazebird/datashare/raw/master/proxy/reconf.lua"

echo "#### processing configure files in $workdir:"
lua reconf.lua $configname || print_exit "# reconf $configname failed."

echo "#### restarting proxy in $workdir:"
kill $(pgrep clash) 2>/dev/null && sleep 3s
./clash -d . >proxy.log 2>&1 &
echo "#### update successfully!"
