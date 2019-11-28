#!/bin/bash

prjdir=(lite/projects/prj_sw_lite ac3/projects/prj_sw_ac3 xcat/projects/prj_xcat)
# prjdir=(lite ac3 xcat)
relscript=pull_release.sh

start() {
    trap "" INT
    for prj in ${prjdir[@]}; do
        ./${relscript} $prj &
    done
    wait
}
stop() {
    pkill ${relscript}
}

case $1 in
start)
    start
    ;;
stop)
    stop
    ;;
*) #echo "Please make sure the option is start/stop."
    stop
    start
    ;;
esac
