#!/bin/bash
# wait instructions and process them

die() { echo "$*" 1>&2 ; exit 1; }

[ -d "$COMPILE_CMD_DIR" ] || die "source dir [COMPILE_CMD_DIR=$COMPILE_CMD_DIR] not found"
CWD=$(pwd)

while true; do
    inotifywait -e 'create,moved_to' $COMPILE_CMD_DIR >/dev/null 2>&1
    for name in Q-*; do 
        echo "name=$name"
        [ $name = "Q-*" ] && break
        arg=${name/Q-/}
        mv $name ${name/Q-/R-}
        name=${name/Q-/R-}
        if ./compile.sh ${arg//-/ } 2>&1 1>$name; then
            mv $name ${name/R-/S-}
            rm -rf $COMPILE_OUTPUT_DIR/$arg && cp -a $COMPILE_SRC_DIR/release $COMPILE_OUTPUT_DIR/$arg
        else 
            mv $name ${name/R-/E-}
        fi
    done
done
