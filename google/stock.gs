// google apps script, similar to javascript; 本脚本用于构建股票数据跟踪表；
var spreadsheet = SpreadsheetApp.getActive();
var stockdbname = "Database"; // 存放所有股票代码 [上证A股](http://www.sse.com.cn/assortment/stock/list/share/) [深证A股](http://www.szse.cn/market/stock/list/index.html)
var defsheetname = "Stocks"; // 存放关注的股票和相关逻辑，当前最多同时关注19只；参考activezone
var activezone = "C2:C20";
var trade_url_pre = "http://quotes.money.163.com/trade/lszjlx_";
var trade_url_suf = ".html#01b08";
var my_stocks = [];

function _getsheet(spreadsheet, name, clear_flag) {
  if (name.length == 0) return null;
  var sheet = spreadsheet.getSheetByName(name);
  if (!sheet) return spreadsheet.insertSheet(name);
  if (clear_flag) sheet.clear();
  return sheet;
}
function _init_active_zone(clear_flag) {
  var sheet = _getsheet(spreadsheet, defsheetname, clear_flag);
  sheet.getRange("A1").setValue("在黄色区域中选择待监控股票，删除Refresh单元完成监控数据更新!");
  sheet.getRange("E2").setValue("Refresh");
  sheet.getRange("E2").setNote("Last modified: " + new Date());
  var dbsheet = _getsheet(spreadsheet, stockdbname, false);
  var rule = SpreadsheetApp.newDataValidation()
    .requireValueInRange(spreadsheet.getRange(stockdbname + "!E1:F5000"))
    .build();
  var range = sheet.getRange(activezone);
  range.setBackground("yellow").setDataValidation(rule);
}
function _init_database(clear_flag) {
  var sheet = _getsheet(spreadsheet, stockdbname, clear_flag);
  sheet.getRange("A1").setValue('=IMPORTRANGE("https://docs.google.com/spreadsheets/d/15pUouNMIJyuxyMbPaY9c7ddMpmLL8xAy1lKOwOstLRA/edit#gid=102777648", "list!A1:B5000")'); // A+B
  sheet.getRange("C1").setValue('=IMPORTRANGE("https://docs.google.com/spreadsheets/d/1r_VW-KpV4HFMJxP-ms2HYco5GxpDUVoHpLwo2U19C1Y/edit#gid=436989383", "list!A1:B5000")'); // C+D
  sheet.getRange("E1").setValue("上证");
  sheet.getRange("F1").setValue("深证");
  for (var i = 2; i < 5000; i++) sheet.getRange("E" + i).setValue("=CONCAT(B" + i + ",A" + i + ")"); // E=AB
  for (var i = 2; i < 5000; i++) sheet.getRange("F" + i).setValue("=CONCAT(D" + i + ",C" + i + ")"); // F=CD
}

function init_stocks() {
  _init_database(true);
  _init_active_zone(true);
}

function destroy_trades() {
  var sheets = SpreadsheetApp.getActiveSpreadsheet().getSheets(); // Logger.log(sheets.length);
  for (var i = 0; i < sheets.length; i++) {
    if (sheets[i].getName() != defsheetname && sheets[i].getName() != stockdbname) spreadsheet.deleteSheet(sheets[i]);
  }
}

function _create_trade_sheet(name) {
  var sheet = _getsheet(spreadsheet, name, false);
  if (!sheet) return;
  var regExp = new RegExp("(\\d+)", "g");
  var code = regExp.exec(name)[1];
  if (code.length == 0) {
    var value = '=IMPORTHTML(CONCAT(CONCAT("' + trade_url_pre + '", M1), ' + trade_url_suf + '), "table",4)';
    sheet.getRange("M1").setBackground("green"); // .setFontColor("white").setFormula('=REGEXEXTRACT(L1,"\\d+")'); // one line mode: name+code
  } else {
    var value = '=IMPORTHTML("' + trade_url_pre + code + trade_url_suf + '", "table",4)';
  }
  sheet.getRange("A2").setValue(value);
  sheet.getRange("A1").setValue("SUM");
  sheet.getRange("B1").setFormulaR1C1("=AVERAGE(R[2]C[0]:R[60]C[0])");
  sheet.getRange("C1:J1").setFormulaR1C1("=SUM(R[2]C[0]:R[60]C[0])");
  sheet.setFrozenRows(2);
}

function create_trades() {
  var range = spreadsheet.getSheetByName(defsheetname).getRange(activezone);
  for (var row = 1; row <= range.getNumRows(); row++) {
    _create_trade_sheet(range.getCell(row, 1).getValue());
  }
}

function onEdit(e) {
  var sheet = spreadsheet.getActiveSheet();
  if (sheet.getName() != defsheetname || e.range.getA1Notation() != "E2") return;
  _init_active_zone(false);
  var values = sheet.getRange(activezone).getValues();
  for (var i = 0; i < values.length; i++) {
    for (var j = 0; j < values[i].length; j++) {
      if (my_stocks == null || my_stocks[i] == null || my_stocks[i][j] == null) my_stocks[i] = [""];
      if (my_stocks[i][j] == values[i][j]) continue;
      Logger.log("[" + i + "][" + j + "]: " + "old " + my_stocks[i][j] + ", new " + values[i][j]);
      if (my_stocks[i][j].length > 0) spreadsheet.deleteSheet(spreadsheet.getSheetByName(my_stocks[i][j]));
      if (values[i][j].length > 0) _create_trade_sheet(values[i][j]);
      my_stocks[i][j] = values[i][j];
    }
  }
}
function onOpen(e) {
  var sheet = _getsheet(spreadsheet, defsheetname, false);
  my_stocks = sheet.getRange(activezone).getValues();
  Logger.log(my_stocks);
}
