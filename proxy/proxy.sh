#!/bin/sh

print_exit() { # parameter: logstr
    echo "$1" >&2 && exit 1
}

fetch_file() { # parameter: filename, path, url
    filename=$1
    path=$2
    url=$3
    if [ -f $path/$filename ]; then
        echo "# $path/$filename already exists."
        return
    fi
    wget -q -O $path/$filename $url >/dev/null || print_exit "# $path/$filename download failed."
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
        echo "# unsupportted arch $arch."
        ;;
    esac
}

[ -z "${BASH_SOURCE}" ] && SCRIPTPATH=$0 || SCRIPTPATH=${BASH_SOURCE[0]}
BASHDIR="$(cd "$(dirname "$SCRIPTPATH")" && pwd)"
workdir=${1-"/tmp"}
configname=config.yaml
urlfile=proxyurl.txt
configurl=$(cat $BASHDIR/$urlfile) # secret
[ -z "$configurl" ] && print_exit "#### config url in $BASHDIR/$urlfile is invalid!"

cd $workdir
echo "#### updating configure files in $workdir:"
mv $configname $configname".bak" 2>/dev/null # force update
fetch_file $configname $workdir $configurl
fetch_file reconf.sh $workdir "https://code.aliyun.com/lazebird/datashare/raw/master/proxy/reconf.sh"
fetch_file Country.mmdb $workdir "https://code.aliyun.com/lazebird/datashare/raw/master/proxy/Country.mmdb"
get_clash
echo "#### processing configure files in $workdir:"
cd $workdir && chmod +x reconf.sh clash
sed -i 's/\r//g' $configname # dos2unix $configname # may not exist, use sed instead?
./reconf.sh $configname || print_exit "# reconf $configname failed."
kill \`pgrep clash\` 2>/dev/null && sleep 3s
./clash -d . >proxy.log &
echo "#### update successfully!"
