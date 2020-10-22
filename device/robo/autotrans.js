// execute with: node picker.js
"use strict";

const fs = require("fs");
let srcfile = "translat.jsn";
let dictfile = "table.json";

function transkey(obj, dobj) {
  for (var key in obj) {
    if (typeof obj[key] == "object") {
      transkey(obj[key], dobj);
    } else if (typeof obj[key] == "string") {
      // console.log(key + ": " + obj[key]);
      if (obj[key].length > 0 && typeof dobj[obj[key]] == "string") obj[key] = dobj[obj[key]];
    } else {
      console.error("invalid type for key: " + key);
    }
  }
}

fs.readFile(srcfile, (err, data) => {
  if (err) throw err;
  let sstrs = JSON.parse(data);
  fs.readFile(dictfile, (err2, data2) => {
    if (err2) throw err2;
    let dstrs = JSON.parse(data2);
    transkey(sstrs, dstrs);
    console.log(JSON.stringify(sstrs));
  });
});
