function createMonthlyTrigger() {  //Added a trigger to automatically run this program on the last day of each month
  ScriptApp.newTrigger('calculateAttendanceAndNotify')
    .timeBased()
    .onMonthDay(-1)  // Runs on the last day of each month
    .atHour(9)       // Runs at 9 AM 
    .create();
}

function calculateAttendanceAndNotify() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var attendanceSheet = ss.getSheetByName("Attendance");
  var emailSheet = ss.getSheetByName("Email");

  // Get all data from Attendance sheet
  var attendanceDataRange = attendanceSheet.getDataRange();
  var attendanceData = attendanceDataRange.getValues();

  // Get all data from Email sheet
  var emailDataRange = emailSheet.getDataRange();
  var emailData = emailDataRange.getValues();

  var emailMap = {};
  for (var i = 1; i < emailData.length; i++) {
    var rollNo = emailData[i][0];
    emailMap[rollNo] = {
      studentEmail: emailData[i][2],
      guardianEmail: emailData[i][3]
    };
  }

  // Assuming first row is headers
  var headers = attendanceData[0];
  var startDateIndex = 2;  // Start index for dates
  var endDateIndex = headers.length - 2;  // End index for dates
  var percentageIndex = headers.length - 1;  // Index for percentage attendance
  
  var shortAttendance = [];

  for (var i = 1; i < attendanceData.length; i++) {
    var row = attendanceData[i];
    var rollNo = row[0];
    var name = row[1];
    var totalDays = 0;
    var presentDays = 0;
    var allCellsFilled = true;

    for (var j = startDateIndex; j <= endDateIndex; j++) {
      if (row[j] === "") {
        allCellsFilled = false;
        break;
      }
    }

    if (allCellsFilled) {
      for (var j = startDateIndex; j <= endDateIndex; j++) {
        totalDays++;
        if (row[j].toLowerCase() === "present") {
          presentDays++;
        }
      }
      var percentage = (presentDays / totalDays) * 100;
      attendanceSheet.getRange(i + 1, percentageIndex + 1).setValue(percentage.toFixed(2));  // Update percentage

      if (percentage < 75) {
        shortAttendance.push({name: name, rollNo: rollNo, percentage: percentage});
      }
    } else {
      attendanceSheet.getRange(i + 1, percentageIndex + 1).setValue("");  // Clear the percentage cell if not all cells are filled
    }
  }

  notifyShortAttendance(shortAttendance, emailMap);
}

function notifyShortAttendance(shortAttendance, emailMap) {
  shortAttendance.forEach(function(student) {
    var rollNo = student.rollNo;
    var name = student.name;
    var percentage = student.percentage.toFixed(2);
    var email = emailMap[rollNo].studentEmail;
    var guardianEmail = emailMap[rollNo].guardianEmail;

    var subject = "Short Attendance Notification";
    var message = "Hello " + name + ",\n\n";
    message += "We hope this email finds you well. We noticed that your attendance is below the required 75% threshold.\n";
    message += "Your current attendance is " + percentage + "%.\n\n";
    message += "It is important to improve your attendance to meet the academic requirements. Please ensure you attend future sessions regularly.\n\n";
    message += "Best regards,\nTeam PresencePulse";

    MailApp.sendEmail(email, subject, message);
    MailApp.sendEmail(guardianEmail, subject, message);  // Send to guardian
  });
}
