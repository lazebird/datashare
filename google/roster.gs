var spreadsheet = SpreadsheetApp.getActive();

function _getsheet(spreadsheet, name, clear_flag = false) {
  if (name.length == 0) return null;
  var sheet = spreadsheet.getSheetByName(name);
  if (!sheet) return spreadsheet.insertSheet(name);
  if (clear_flag) sheet.clear();
  return sheet;
}

function _val_formatter(v) {
  if (!v || v === '') return v
  var oldval = v
  v = v.replace(/(\d+\.)/, '')
  v = v.replace(/([^\d]+)/g, '?')
  v = v.replace(/(^\?)/, '')
  v = v.replace(/^7([12])\?/, '7$1#')
  v = v.replace(/\?.*/, '')
  // console.log('[val_formatter] val %s -> %s', oldval, v)
  return v
}
function _read_orgData() {
  var sheet = _getsheet(spreadsheet, "origin", false);
  var values = sheet.getRange("A1:A300").getValues();
  // console.log('[read_orgData] values(%d): %s', values.length, JSON.stringify(values))
  return values
}
function _set_newData(values) {
  // console.log('[set_newData] values(%d): %s', values.length, JSON.stringify(values))
  if (!values.length) return
  var sheet = _getsheet(spreadsheet, "process", true);
  sheet.getRange("A2:A" + (1 + values.length)).setValues(values)
}
function _formatter(values) {
  // console.log('[formatter] values %s', JSON.stringify(values))
  values = values.filter(v => v[0].length) // remove empty
  let rawValues = []
  for (var v of values) rawValues.push(v[0])
  for (var i = 0; i < rawValues.length; i++) rawValues[i] = _val_formatter(rawValues[i])
  rawValues = rawValues.filter((e, i) => { return rawValues.indexOf(e) === i }) // remove duplicates
  // console.log('[formatter] rawValues (%d): %s', rawValues.length, JSON.stringify(rawValues))
  values = []
  for (var r of rawValues) values.push([r])
  return values
}
function _sorter(a, b) {
  if (a === [""]) return -1;
  if (b === [""]) return 1;
  var aa = a[0].split('#')
  var bb = b[0].split('#')
  if (aa[0] !== bb[0]) return Number(aa[0] - bb[0])
  return Number(aa[1] - bb[1])
}
function data_process() {
  var values = _read_orgData()
  values = _formatter(values)
  // console.log('[process] values %s', JSON.stringify(values))
  values.sort(_sorter)
  _set_newData(values)
}
function _draw_floor(sheet, name, floors, rooms, base) {
  // sheet.getRange("A" + base).setValues([[name]])
  var missing = ['71#108', '71#109', '71#110']
  for (var i = 0; i < floors.length; i++) {
    let realRooms = []
    for (var r of rooms) realRooms.push(name + '#' + floors[i] + r)
    realRooms = realRooms.filter(r => (missing.indexOf(r) < 0))
    sheet.getRange("A" + (i + base) + ":" + String.fromCharCode('A'.charCodeAt() + realRooms.length - 1) + (i + base)).setValues([realRooms])
  }
}
function draw_buildings() {
  var sheet = _getsheet(spreadsheet, "layout", true);
  _draw_floor(sheet, '71', ['1', '3', '5', '7', '9', '11', '13', '15', '17', '19', '21'].reverse(), ['01', '02', '03', '05', '06', '07', '08', '09', '10'], 1)
  _draw_floor(sheet, '72', ['1', '3', '5', '7', '9', '11', '13', '15', '17', '19'].reverse(), ['01', '02', '03', '05', '06', '07', '08', '09', '10', '11'], 13)
}
function _read_procData() {
  var sheet = _getsheet(spreadsheet, "process", false);
  var values = sheet.getRange("A1:A250").getValues();
  return [].concat(...values).filter(v => v !== '')
}
function _forEachRangeCell(range, f, datas) {
  const numRows = range.getNumRows();
  const numCols = range.getNumColumns();
  for (let i = 1; i <= numCols; i++) {
    for (let j = 1; j <= numRows; j++) {
      const cell = range.getCell(j, i)
      f(cell, datas)
    }
  }
}
function _set_cell_flag(cell, datas) {
  var value = cell.getValue()
  if (!value.length) return
  cell.setBackground(datas.indexOf(value) >= 0 && 'green' || 'red')
}
function set_flag() {
  var datas = _read_procData();
  // console.log('[set_flag] datas %s', JSON.stringify(datas))
  var sheet = _getsheet(spreadsheet, "layout", false);
  _forEachRangeCell(sheet.getRange("A1:M30"), _set_cell_flag, datas)
}
function autorun() {
  data_process();
  draw_buildings();
  set_flag()
}