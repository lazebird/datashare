// google apps script, similar to javascript; 本脚本用于构建股票数据跟踪表；
var spreadsheet = SpreadsheetApp.getActive();
var stockdbname = "Database"; // 存放所有股票代码
var defsheetname = "Stocks"; // 存放关注的股票和相关逻辑，当前最多同时关注19只；参考activezone
var activezone = "C2:C20";
var stocks_url1 = "https://www.banban.cn/gupiao/list_sh.html"; //"http://quote.eastmoney.com/stocklist.html";
var stocks_url2 = "https://www.banban.cn/gupiao/list_sz.html";
var trade_url_pre = "http://quotes.money.163.com/trade/lszjlx_";
var trade_url_suf = ".html#01b08";

function _getsheet(spreadsheet, name, clear_flag) {
  if (name.length == 0) return null;
  var sheet = spreadsheet.getSheetByName(name);
  if (!sheet) return spreadsheet.insertSheet(name);
  if (clear_flag) sheet.clear();
  return sheet;
}

function init_active_zone(clear_flag) {
  var sheet = _getsheet(spreadsheet, defsheetname, clear_flag);
  sheet.getRange("A1").setValue("在黄色区域中选择待监控股票，删除Refresh单元完成监控数据更新!");
  sheet.getRange("E2").setValue("Refresh");
  sheet.getRange("E2").setNote("Last modified: " + new Date());
  var dbsheet = _getsheet(spreadsheet, stockdbname, false);
  var rule = SpreadsheetApp.newDataValidation()
    .requireValueInRange(spreadsheet.getRange(stockdbname + "!" + dbsheet.getDataRange().getA1Notation()))
    .build();
  var range = sheet.getRange(activezone);
  range.setBackground("yellow").setDataValidation(rule);
}

function init_database(clear_flag) {
  var sheet = _getsheet(spreadsheet, stockdbname, clear_flag);
  sheet.getRange("A1").setValue('=IMPORTHTML("' + stocks_url1 + '", "list",4)');
  sheet.getRange("B1").setValue('=IMPORTHTML("' + stocks_url2 + '", "list",4)');
}
function init_stocks() {
  init_database(true);
  init_active_zone(true);
}

function destroy_trades() {
  var sheets = SpreadsheetApp.getActiveSpreadsheet().getSheets(); // Logger.log(sheets.length);
  for (var i = 0; i < sheets.length; i++) {
    if (sheets[i].getName() != defsheetname && sheets[i].getName() != stockdbname) spreadsheet.deleteSheet(sheets[i]);
  }
}

function create_trade_sheet(name) {
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
    create_trade_sheet(range.getCell(row, 1).getValue());
  }
}

function onEdit(e) {
  var sheet = spreadsheet.getActiveSheet();
  if (sheet.getName() != defsheetname || e.range.getA1Notation() != "E2") return;
  init_active_zone(false);
  destroy_trades();
  create_trades(); // spreadsheet.setActiveSheet(sheet);
}
