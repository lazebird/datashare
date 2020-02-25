// execute with: node picker.js
"use strict";

const fs = require("fs");
let srcfile = "translat.jsn";

function dumpkey(obj) {
  for (var key in obj) {
    if (typeof obj[key] == "object") {
      dumpkey(obj[key]);
    } else if (typeof obj[key] == "string") {
      // console.log(key + ": " + obj[key]);
      if (obj[key].length > 0)
        console.log(obj[key].replace(/&quot;(.+)&quot;/g, "[$1]")); // replace &quot; to []
    } else {
      console.error("invalid type for key: " + key);
    }
  }
}

fs.readFile(srcfile, (err, data) => {
  if (err) throw err;
  let strs = JSON.parse(data);
  //   console.log("length is " + strs.length);
  dumpkey(strs);
  //   console.log(strs);
});
