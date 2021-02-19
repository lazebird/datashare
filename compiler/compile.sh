#!/bin/bash
# compile a specific product+version

die() { echo "$*" 1>&2 ; exit 1; }

product=${1:-"lite"}
branch=${2:-"develop"}
commitid=${3:-"HEAD"}
echo "INFO: product=$product, branch=$branch, commitid=$commitid, COMPILE_SRC_DIR=$COMPILE_SRC_DIR"
[ -d "$COMPILE_SRC_DIR" ] || die "source dir [COMPILE_SRC_DIR=$COMPILE_SRC_DIR] not found"
CWD=$(pwd)

# src prepare
cd $COMPILE_SRC_DIR || die "change to source dir failed"
git pull --rebase || die "git pull --rebase failed"
git checkout --track origin/$branch || die "git checkout --track origin/$branch failed"
git pull --rebase || die "git pull --rebase failed"
git checkout $commitid || die "git checkout $commitid failed"

# src compile
. env/$product-env.sh
./script/release.sh
