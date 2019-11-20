#!/bin/bash

prjdir=(lite/projects/prj_sw_lite ac3/projects/prj_sw_ac3 xcat/projects/prj_xcat)

release_start() {
    trap "" INT
    rm -rf output/
    for prj in ${prjdir[@]}; do
        ./u_rel.sh $prj &
    done
    wait
}
release_stop() {
    pkill u_rel.sh
    pkill release.sh
}

case $1 in
start)
    release_start
    ;;
stop)
    release_stop
    ;;
*)
    release_stop
    release_start
    #echo "Please make sure the option is start/stop."
    ;;
esac
