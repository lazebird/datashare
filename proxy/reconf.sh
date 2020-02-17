#!/bin/bash

filename=${1:-"config.yml"}

# remove game server
sed -i '/游戏.*type/d' $filename
sed -i 's/, "[^"]*游戏[^"]*"//g' $filename
# allow lan
sed -i 's/allow-lan: false/allow-lan: true/' $filename
# use auto group instead
sed -i 's/type: select/type: url-test/' $filename
sed -i 's/\]\}/\], url: http:\/\/www\.gstatic\.com\/generate_204, interval: 300 \}/' $filename
sed -i '/- { name: MunCloud-旗舰加速-Diamond Package-new/d' $filename
sed -i 's/#- { name: auto/- { name: MunCloud-旗舰加速-Diamond Package-new/' $filename
# add rule
sed -i 's/- GEOIP/- DOMAIN-SUFFIX,baidu.com,DIRECT\n- GEOIP/' $filename
sed -i 's/- GEOIP/- DOMAIN-SUFFIX,youku.com,DIRECT\n- GEOIP/' $filename
sed -i 's/- GEOIP/- DOMAIN-SUFFIX,iqiyi.com,DIRECT\n- GEOIP/' $filename
sed -i 's/- GEOIP/- DOMAIN-SUFFIX,aliyun.com,DIRECT\n- GEOIP/' $filename
sed -i 's/- GEOIP/- DOMAIN-SUFFIX,sina.com,DIRECT\n- GEOIP/' $filename
sed -i 's/- GEOIP/- DOMAIN-SUFFIX,weibo.com,DIRECT\n- GEOIP/' $filename
sed -i 's/- GEOIP/- DOMAIN-SUFFIX,163.com,DIRECT\n- GEOIP/' $filename
sed -i 's/- GEOIP/- DOMAIN-SUFFIX,qq.com,DIRECT\n- GEOIP/' $filename
sed -i 's/- GEOIP/- DOMAIN-SUFFIX,taobao.com,DIRECT\n- GEOIP/' $filename
sed -i 's/- GEOIP/- DOMAIN-SUFFIX,jd.com,DIRECT\n- GEOIP/' $filename
sed -i 's/- GEOIP/- IP-CIDR,192.0.0.0\/8,DIRECT\n- GEOIP/' $filename
