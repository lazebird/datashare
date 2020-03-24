// google apps script, similar to javascript
// 本脚本用于构建股票数据跟踪表；目标表格存在sheet名为"Stocks",R2C2~RNC2为股票代码和名称；作为基本信息数据
function _getsheet(spreadsheet, name, reuse_flag) {
  var sheet = spreadsheet.getSheetByName(name);
  if (!sheet) return spreadsheet.insertSheet(name);
  // if no change, should return null here
  if (reuse_flag) {
    sheet.clear();
  } else {
    spreadsheet.deleteSheet(sheet);
    sheet = spreadsheet.insertSheet(name);
  }
  return sheet;
}

var spreadsheet = SpreadsheetApp.getActive();
function clear() {
  var range = spreadsheet.getSheetByName("Stocks").getDataRange();
  for (var row = 2; row <= range.getNumRows(); row++) {
    var sheet = spreadsheet.getSheetByName(range.getCell(row, 2).getValue());
    if (sheet) spreadsheet.deleteSheet(sheet);
  }
}

function main1() {
  var range = spreadsheet.getSheetByName("Stocks").getDataRange();
  for (var row = 2; row <= range.getNumRows(); row++) {
    if ((sheet = _getsheet(spreadsheet, range.getCell(row, 2).getValue(), true))) {
      var value = '=IMPORTHTML("http://quotes.money.163.com/trade/lszjlx_' + range.getCell(row, 3).getValue() + '.html#01b08", "table",4)';
      sheet.getRange("A1").setValue("SUM");
      sheet.getRange("B1").setFormulaR1C1("=AVERAGE(R[2]C[0]:R[60]C[0])");
      sheet.getRange("C1:J1").setFormulaR1C1("=SUM(R[2]C[0]:R[60]C[0])");
      sheet.getRange("A2").setValue(value);
      sheet.setFrozenRows(2);
    }
  }
}

function main2() {
  if ((sheet = _getsheet(spreadsheet, "Trades", true))) {
    var value = '=IMPORTHTML(CONCAT(CONCAT("http://quotes.money.163.com/trade/lszjlx_", M1), ".html#01b08"), "table",4)';
    sheet.getRange("A1").setValue("SUM");
    sheet.getRange("B1").setFormulaR1C1("=AVERAGE(R[2]C[0]:R[60]C[0])");
    sheet.getRange("C1:J1").setFormulaR1C1("=SUM(R[2]C[0]:R[60]C[0])");
    sheet.getRange("A2").setValue(value);
    //sheet.getRange("M1").setBackground("green").setFontColor("white").setDataValidation(SpreadsheetApp.newDataValidation().requireValueInRange(sheet.getRange('M2:L100')).build());
    //sheet.getRange("M1").setBackground("green").setFontColor("white").setFormula("=VLOOKUP(L1,L2:M100,2,FALSE)");  // two line mode: name code
    sheet
      .getRange("M1")
      .setBackground("green")
      .setFontColor("white")
      .setFormula('=REGEXEXTRACT(L1,"\\d+")'); // one line mode: name+code
    sheet.setFrozenRows(2);
  }
}
