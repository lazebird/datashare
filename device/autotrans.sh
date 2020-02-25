#!/bin/bash

node autotrans.js >translat.jsn.json
if [ "$(pwd)" == "/root/projects/datashare/device" ]; then
    cp translat.jsn.json ../../robo/src/appl/web/web_root/cn/translat.jsn
fi
