#!/bin/bash

node autotrans.js | jq . >translat.jsn.json
if [ "$(pwd)" == "/root/projects/datashare/device" ]; then
    cp translat.jsn ../../robo/src/appl/web/web_root/en/translat.jsn
    cp translat.jsn.json ../../robo/src/appl/web/web_root/cn/translat.jsn
fi
