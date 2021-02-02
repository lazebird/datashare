src=arg[1] or "config.yaml"
dst=arg[2] or src
-- read
f = io.open(src, "r")
text = f:read("*a")
f:close()

-- proc
text = string.gsub(text, "\r", "")
-- remove game server, for game server's access to google is not very stable
text = string.gsub(text, "[^\n]+游戏[^\n]+\n", "")
-- allow lan
text = string.gsub(text, "allow-lan: false", "allow-lan: true")
if string.find(text, "url%-test") == nil then
    text = string.gsub(text, "节点选择\n    type: select", "节点选择\n    type: url-test\n    url: http://www.gstatic.com/generate_204\n    interval: 300")
end

-- write
f = io.open(dst, "w")
text = f:write(text)
f:close()
