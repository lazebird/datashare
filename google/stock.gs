// google apps script, similar to javascript
function reuse(spreadsheet, name) {
  var sheet = spreadsheet.getSheetByName(name);
  if (sheet) {
    sheet.clear();
  } else {
    sheet = spreadsheet.insertSheet(name);
  }
  return sheet;
}

function renew(spreadsheet, name) {
  var sheet = spreadsheet.getSheetByName(name);
  if (sheet) {
    spreadsheet.deleteSheet(sheet);
  }
  return (sheet = spreadsheet.insertSheet(name));
}

function skip(spreadsheet, name) {
  var sheet = spreadsheet.getSheetByName(name);
  if (sheet) {
    return null;
  }
  return (sheet = spreadsheet.insertSheet(name));
}

var getsheet = reuse;
var spreadsheet = SpreadsheetApp.getActive();

function clear() {
  var sheet0 = spreadsheet.getSheetByName("我的股票"); //第一个电子表格
  var range0 = sheet0.getDataRange();

  //从第2行开始  range0.getNumRows()
  for (var row = 2; row <= range0.getNumRows(); row++) {
    var sheet = spreadsheet.getSheetByName(range0.getCell(row, 2).getValue());
    if (sheet) {
      spreadsheet.deleteSheet(sheet);
    }
  }
}

function main1() {
  var sheet0 = spreadsheet.getSheetByName("我的股票"); //第一个电子表格
  var range0 = sheet0.getDataRange();

  //从第2行开始  range0.getNumRows()
  for (var row = 2; row <= range0.getNumRows(); row++) {
    if ((sheet = getsheet(spreadsheet, range0.getCell(row, 2).getValue()))) {
      var value = '=IMPORTHTML("http://quotes.money.163.com/trade/lszjlx_' + range0.getCell(row, 3).getValue() + '.html#01b08", "table",4)';
      sheet.getRange("A1").setValue("自动求和");
      sheet.getRange("B1").setFormulaR1C1("=AVERAGE(R[2]C[0]:R[60]C[0])"); // 收盘价求平均值
      sheet.getRange("C1:J1").setFormulaR1C1("=SUM(R[2]C[0]:R[60]C[0])"); // 求累计值
      sheet.getRange("A2").setValue(value);
      sheet.setFrozenRows(2);
    }
  }
}

function main2() {
  if ((sheet = getsheet(spreadsheet, "历史资金流向"))) {
    var value = '=IMPORTHTML(CONCAT(CONCAT("http://quotes.money.163.com/trade/lszjlx_", M1), ".html#01b08"), "table",4)';
    sheet.getRange("A1").setValue("自动求和");
    sheet.getRange("B1").setFormulaR1C1("=AVERAGE(R[2]C[0]:R[60]C[0])"); // 收盘价求平均值
    sheet.getRange("C1:J1").setFormulaR1C1("=SUM(R[2]C[0]:R[60]C[0])"); // 求累计值
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
