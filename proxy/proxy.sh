cat > updater.sh <<EOF && bash updater.sh
#!/bin/bash

echo "#### this is an updater for proxy"

# parameter: filename, path, url
fetch_file() {
    filename=\$1
    path=\$2
    url=\$3 
    if [ -f \$path/\$filename ]; then
        echo "# \$path/\$filename already exists"
        return
    fi
    wget -O \$path/\$filename \$url || exit 1
}

configname=config.yaml
workdir=.
configurl="$1" # secret

echo "#### updating configure files"
mv \$workdir/\$configname \$workdir/\$configname".bak" 2>/dev/null # force update
fetch_file \$configname \$workdir \$configurl
fetch_file clashr \$workdir "https://code.aliyun.com/lazebird/datashare/raw/master/proxy/clashr-linux-mipsle-hardfloat"
fetch_file reconf.sh \$workdir "https://code.aliyun.com/lazebird/datashare/raw/master/proxy/reconf.sh"
fetch_file Country.mmdb \$workdir "https://code.aliyun.com/lazebird/datashare/raw/master/proxy/Country.mmdb"
echo "#### processing configure files"
dos2unix \$filename && ./reconf.sh \$filename
kill `pgrep clash`; sleep 1s &&  ./clashr -d . &
echo "#### update successfully!"
EOF
