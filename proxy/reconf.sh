#!/bin/bash

# remove game server
sed -i '/游戏.*type/d' config.yml
sed -i 's/, "[^"]*游戏[^"]*"//g' config.yml
# allow lan
sed -i 's/allow-lan: false/allow-lan: true/' config.yml
# use auto group instead
sed -i 's/type: select/type: url-test/' config.yml
sed -i 's/\]\}/\], url: http:\/\/www\.gstatic\.com\/generate_204, interval: 300 \}/' config.yml
sed -i 's/#- { name: auto/- { name: MunCloud-旗舰加速-Diamond Package-new/' config.yml
# add rule
sed -i 's/- GEOIP/- DOMAIN-SUFFIX,baidu.com,DIRECT\n- GEOIP/' config.yml
sed -i 's/- GEOIP/- DOMAIN-SUFFIX,youku.com,DIRECT\n- GEOIP/' config.yml
sed -i 's/- GEOIP/- DOMAIN-SUFFIX,iqiyi.com,DIRECT\n- GEOIP/' config.yml
sed -i 's/- GEOIP/- DOMAIN-SUFFIX,aliyun.com,DIRECT\n- GEOIP/' config.yml
sed -i 's/- GEOIP/- DOMAIN-SUFFIX,sina.com,DIRECT\n- GEOIP/' config.yml
sed -i 's/- GEOIP/- DOMAIN-SUFFIX,weibo.com,DIRECT\n- GEOIP/' config.yml
sed -i 's/- GEOIP/- DOMAIN-SUFFIX,163.com,DIRECT\n- GEOIP/' config.yml
sed -i 's/- GEOIP/- DOMAIN-SUFFIX,qq.com,DIRECT\n- GEOIP/' config.yml
sed -i 's/- GEOIP/- DOMAIN-SUFFIX,taobao.com,DIRECT\n- GEOIP/' config.yml
sed -i 's/- GEOIP/- DOMAIN-SUFFIX,jd.com,DIRECT\n- GEOIP/' config.yml
sed -i 's/- GEOIP/- IP-CIDR,192.0.0.0\/8,DIRECT\n- GEOIP/' config.yml
