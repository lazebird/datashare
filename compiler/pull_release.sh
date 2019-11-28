#!/bin/bash
# pull + release
prj=$1
CWD=$(pwd)

cd $prj
product=${prj%%/*}
branch=$(git rev-parse --abbrev-ref HEAD)
branch=${branch/\//-}
output=${CWD}/output/
logfile=$product-$branch-output.txt

version=${branch##*-}

echo "INFO: cwd=$CWD, prj=$prj, branch=$branch, output=$output, logfile=$logfile"
mkdir -p $output && rm -rf $output/$product
if [ $version \< "5" ]; then
    echo "version=$version, use old script"
    git pull --rebase && time ./release.sh >$output/$logfile 2>&1
else
    echo "version=$version, use new script"
    git pull --rebase && . env/${product}-env.sh && time ./script/release.sh >$output/$logfile 2>&1
fi
cp -a release/ $output/$product
