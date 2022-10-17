#!/bin/sh

logcmd="logger -is -p user.debug -t proxy"
repoURL="https://github.com/lazebird/datashare/raw/master"

print_exit() { # parameter: logstr
    $logcmd "$1" >&2 && exit 1
}

fetch_file() { # parameter: filename, path, url, alternate
    filename=$1
    path=$2
    url=$3
    alt=$4
    if [ -f $path/$filename ]; then
        $logcmd "# $path/$filename already exists."
        return
    fi
    wget -q --no-check-certificate -O $path/$filename $url >/dev/null
    if [ $? -ne 0 ]; then
        rm -f $path/$filename                     # remove empty file
        mv $path/$alt $path/$filename 2>/dev/null # try revert
        $logcmd "# $url download failed." >&2
        exit 1
    fi
    $logcmd "# $path/$filename download success."
}

get_clash() {
    arch=$(uname -m)
    case $arch in
    x86_64)
        fetch_file clash $workdir "$repoURL/proxy/clash-linux-amd64"
        ;;
    mips)
        fetch_file clash $workdir "$repoURL/proxy/clash-linux-mipsle-hardfloat"
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
$logcmd "#### starting proxy temporally in $workdir:"
get_clash && chmod +x clash
fetch_file Country.mmdb $workdir "$repoURL/proxy/Country.mmdb"
mv $configname $configbak 2>/dev/null # save last config
fetch_file $configname $workdir "$repoURL/proxy/config.yaml"
while [ kill $(pgrep clash) ] 2>/dev/null; do sleep 1s; done
ls $configname >/dev/null && (./clash -d . >proxy.log 2>&1 &) && $logcmd "# starting proxy temporally success"

$logcmd "#### updating configure files in $workdir:"
[ ! -e "$configbak" ] && mv $configname $configbak 2>/dev/null || rm -f $configname # save/remove empty config
fetch_file $configname $workdir $configurl $configbak
fetch_file reconf.lua $workdir "$repoURL/proxy/reconf.lua"

$logcmd "#### processing configure files in $workdir:"
lua reconf.lua $configname || print_exit "# reconf $configname failed."

$logcmd "#### restarting proxy in $workdir:"
kill $(pgrep clash) 2>/dev/null && sleep 3s
./clash -d . >proxy.log 2>&1 &
$logcmd "#### update successfully!"
