// google apps script, similar to javascript; 本脚本用于构建股票数据跟踪表；
var spreadsheet = SpreadsheetApp.getActive();
var stockdbname = "Database"; // 存放所有股票代码 [上证A股](http://www.sse.com.cn/assortment/stock/list/share/) [深证A股](http://www.szse.cn/market/stock/list/index.html)
var defsheetname = "Stocks"; // 存放关注的股票和相关逻辑，当前最多同时关注有限数量股票；参考activezone
var workzone = "A1:M40";
var activetitlezone = "C1";
var activezone = "C2:C30";
var backuptitlezone = "M1";
var backupzone = "M2:M30";
var trade_url_pre = "http://quotes.money.163.com/trade/lszjlx_";
var trade_url_suf = ".html#01b08";

function _getsheet(spreadsheet, name, clear_flag) {
  if (name.length == 0) return null;
  var sheet = spreadsheet.getSheetByName(name);
  if (!sheet) return spreadsheet.insertSheet(name);
  if (clear_flag) sheet.clear();
  return sheet;
}
function _set_checkbox(sheet, prompt, promptpos, cbpos, val) {
  sheet.getRange(promptpos).setHorizontalAlignment("center");
  sheet.getRange(promptpos).setValue(prompt);
  sheet.getRange(cbpos).removeCheckboxes(); // avoid too many checkboxes are created
  sheet.getRange(cbpos).insertCheckboxes("yes", "no");
  sheet.getRange(cbpos).setValue(val);
  sheet.getRange(cbpos).setNote("Last modified: " + new Date());
}
function _init_workzone_layout(sheet) {
  sheet.getRange(workzone).setHorizontalAlignment("center");
  var rule = SpreadsheetApp.newDataValidation().requireValueInRange(spreadsheet.getRange(stockdbname + "!E1:F5000")).build();
  sheet.getRange(activetitlezone).setValue("Active");
  sheet.getRange(activezone).setBackground("yellow").setDataValidation(rule);
  sheet.getRange(backuptitlezone).setValue("Backup");
}
function _init_workzone() {
  var sheet = _getsheet(spreadsheet, defsheetname, true);
  _init_workzone_layout(sheet);
  _set_checkbox(sheet, "Update", "E1", "E2", "no");
}
function _workzone_update(e) {
  if (e.range.getA1Notation() != "E2") return;
  var sheet = spreadsheet.getActiveSheet();
  _init_workzone_layout(sheet); // sheet.getRange(workzone).trimWhitespace(); // trim from source, else validation fails
  _set_checkbox(sheet, "Update", "E1", "E2", "no");

  var newvals = sheet.getRange(activezone).getValues();
  var oldvals = sheet.getRange(backupzone).getValues();
  for (var i = 0; i < newvals.length; i++) {
    for (var j = 0; j < newvals[i].length; j++) {
      if (newvals[i][j] == oldvals[i][j]) continue; // if a stock is moved but not deleted, strict [i][j] compare will still cause a recreation
      if (oldvals[i][j].length > 0) spreadsheet.deleteSheet(spreadsheet.getSheetByName(oldvals[i][j]));
      if (newvals[i][j].length > 0) _create_trade_sheet(newvals[i][j]);
    }
  }
  sheet.getRange(backupzone).setValues(newvals);
}

function _init_database() {
  var sheet = _getsheet(spreadsheet, stockdbname, true);
  sheet.getRange("A1").setValue('=IMPORTRANGE("https://docs.google.com/spreadsheets/d/19Xu0WyPGbD8MUIOY4zqr3QZ-v1OCkFyFR2trP8bjCeU/edit#gid=226774756", "list!A1:B5000")'); // A+B
  sheet.getRange("C1").setValue('=query(IMPORTRANGE("https://docs.google.com/spreadsheets/d/1JtrTGwFax4vENH4xv1zU07ai7gmzeVf0N40EDCsLHtM/edit#gid=1527914076", "list!E1:F5000"), "select Col1, Col2",0)'); // C+D
  sheet.getRange("E1").setValue("上证");
  sheet.getRange("F1").setValue("深证");
  sheet.getRange("E2:E5000").setFormulaR1C1("=TRIM(CONCAT(R[0]C[-3],R[0]C[-4]))"); // E=BA
  sheet.getRange("F2:F5000").setFormulaR1C1("=TRIM(CONCAT(R[0]C[-2],R[0]C[-3]))"); // F=DC
}

function init_stocks() {
  _init_database();
  _init_workzone();
}

function destroy_trades() {
  var sheets = SpreadsheetApp.getActiveSpreadsheet().getSheets(); // Logger.log(sheets.length);
  for (var i = 0; i < sheets.length; i++) if (sheets[i].getName() != defsheetname && sheets[i].getName() != stockdbname) spreadsheet.deleteSheet(sheets[i]);
}

function _create_trade_sheet(name) {
  var sheet = _getsheet(spreadsheet, name, true);
  if (!sheet) return;
  var regExp = new RegExp("(\\d+)", "g");
  var code = regExp.exec(name)[1];
  if (code.length <= 0) {
    var value = '=IMPORTHTML(CONCAT(CONCAT("' + trade_url_pre + '", M1), ' + trade_url_suf + '), "table",4)'; // use M1 to input stock code
    sheet.getRange("M1").setBackground("green").setFontColor("white").setFormula('=REGEXEXTRACT(L1,"\\d+")'); // one line mode: name+code
  } else {
    var value = '=IMPORTHTML("' + trade_url_pre + code + trade_url_suf + '", "table",4)';
  }
  sheet.getRange("A2").setValue(value);
  sheet.getRange("A1").setValue("SUM");
  sheet.getRange("B1").setFormulaR1C1("=AVERAGE(R[2]C[0]:R[60]C[0])");
  sheet.getRange("C1:J1").setFormulaR1C1("=SUM(R[2]C[0]:R[60]C[0])");
  sheet.setFrozenRows(2);
  _set_checkbox(sheet, "Reload", "M1", "M2", "no");
}
function _trade_reload(e) {
  if (e.range.getA1Notation() != "M2") return;
  _create_trade_sheet(spreadsheet.getActiveSheet().getName());
}

function onEdit(e) {
  var name = spreadsheet.getActiveSheet().getName();
  if (name == defsheetname) {
    _workzone_update(e);
  } else if (name != stockdbname) {
    _trade_reload(e);
  }
}
