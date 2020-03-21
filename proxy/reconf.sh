#!/bin/bash

filename=${1:-"config.yml"}

# remove game server
sed -i '/游戏.*type/d' $filename
sed -i 's/, "[^"]*游戏[^"]*"//g' $filename
# allow lan
sed -i 's/allow-lan: false/allow-lan: true/' $filename
# use auto group instead
sed -i -e ":begin; /节点选择/,/type: select/ { /type: select/! { $! { N; b begin }; }; s/节点选择\n    type: select/节点选择\n    type: url-test\n    url: http:\/\/www\.gstatic\.com\/generate_204\n    interval: 300/; };" $filename
# add rule
# sed -i 's/- GEOIP/- DOMAIN-SUFFIX,baidu.com,DIRECT\n- GEOIP/' $filename
# sed -i 's/- GEOIP/- DOMAIN-SUFFIX,youku.com,DIRECT\n- GEOIP/' $filename
# sed -i 's/- GEOIP/- DOMAIN-SUFFIX,iqiyi.com,DIRECT\n- GEOIP/' $filename
# sed -i 's/- GEOIP/- DOMAIN-SUFFIX,aliyun.com,DIRECT\n- GEOIP/' $filename
# sed -i 's/- GEOIP/- DOMAIN-SUFFIX,sina.com,DIRECT\n- GEOIP/' $filename
# sed -i 's/- GEOIP/- DOMAIN-SUFFIX,weibo.com,DIRECT\n- GEOIP/' $filename
# sed -i 's/- GEOIP/- DOMAIN-SUFFIX,163.com,DIRECT\n- GEOIP/' $filename
# sed -i 's/- GEOIP/- DOMAIN-SUFFIX,qq.com,DIRECT\n- GEOIP/' $filename
# sed -i 's/- GEOIP/- DOMAIN-SUFFIX,taobao.com,DIRECT\n- GEOIP/' $filename
# sed -i 's/- GEOIP/- DOMAIN-SUFFIX,jd.com,DIRECT\n- GEOIP/' $filename
# sed -i 's/- GEOIP/- IP-CIDR,192.0.0.0\/8,DIRECT\n- GEOIP/' $filename
