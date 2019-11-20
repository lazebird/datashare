#!/bin/bash

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
prj=$1

cd $prj
product=${prj%%/*}
branch=$(git rev-parse --abbrev-ref HEAD)
branch=${branch/\//-}
output=$DIR/output/
logfile=$product-$branch-output.txt

echo "INFO: prj=$prj, branch=$branch, output=$output, logfile=$logfile"
mkdir -p $output
git pull --rebase && time ./release.sh >$output/$logfile 2>&1
rm -rf $output/$product
cp -a release/ $output/$product
