function sync_onEdit(e) {
  const sheet1Name = 'Attendance'; // name of first sheet
  const sheet2Name = 'Email'; // name of second sheet
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheet1 = ss.getSheetByName(sheet1Name);
  const sheet2 = ss.getSheetByName(sheet2Name);
  
  const range = e.range;
  
  if (range.getSheet().getName() === sheet1Name) {
    const row = range.getRow();
    const col = range.getColumn();
    
    // If editing a row within the data range
    if (row > 1 && col <= 2) {
      // Update corresponding cell in Sheet2
      sheet2.getRange(row, col).setValue(range.getValue());
    }
  }
}

function sync_onChange(e) {
  const sheet1Name = 'Attendance'; // name of first sheet
  const sheet2Name = 'Email'; // name of second sheet
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheet1 = ss.getSheetByName(sheet1Name);
  const sheet2 = ss.getSheetByName(sheet2Name);
  
  const sheet1Data = sheet1.getRange(1, 1, sheet1.getLastRow(), 2).getValues(); // Get only the first two columns
  
  // Clear the first two columns in Sheet2 and copy updated data from Sheet1
  sheet2.getRange(1, 1, sheet2.getMaxRows(), 2).clearContent(); 
  for (let i = 0; i < sheet1Data.length; i++) {
    if (sheet1Data[i][0] || sheet1Data[i][1]) { // Copy even if only one of the columns has content
      sheet2.getRange(i + 1, 1, 1, 2).setValues([sheet1Data[i]]);
    }
  }
}
