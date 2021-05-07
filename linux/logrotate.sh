#!/bin/bash

die() { echo "$*" 1>&2 ; exit 1; }

workdir=${1:-"./"}
accesstm=${2:-3}
echo "workdir=$workdir, accesstm=$accesstm"
[ $workdir == "/" ] && die "Dangerous!"
find $workdir -type f -atime +$accesstm | xargs rm -f
