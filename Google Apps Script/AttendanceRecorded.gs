function mailAttendanceStatusonEdit(e) {
  var range = e.range;
  var sheet = range.getSheet();

  if (sheet.getName() === "Attendance" && range.getColumn() > 1) {  // Only trigger on the 'Attendance' sheet and for attendance columns
    var column = range.getColumn();
    var row = range.getRow();
    var status = range.getValue();
    var name = sheet.getRange(row, 2).getValue();  // Assuming the second column has student names
    var rollNo = sheet.getRange(row, 1).getValue();  // Assuming the first column has roll numbers

    if (status === "Present" || status === "Absent") {
      var email = getEmailFromRollNo(rollNo);  // Fetch email from the 'Email' sheet
      if (email) {
        sendEmail(name, email, status);
      } else {
        Logger.log("Email not found for Roll No: " + rollNo);
      }
    }
  }
}

function getEmailFromRollNo(rollNo) {
  var emailSheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Email");
  var dataRange = emailSheet.getDataRange();
  var data = dataRange.getValues();

  for (var i = 1; i < data.length; i++) {
    if (data[i][0] == rollNo) {  // Assuming the first column has roll numbers
      return data[i][2];  // Assuming the third column has emails
    }
  }
  return null;
}

function sendEmail(name, email, status) {
  var subject = status === "Present" ? "Thank You for Attending Today's Session!" : "We Missed You in Today's Session";
  var message = "Hello " + name + ",\n\n";
  
  if (status === "Present") {
    message += "Thanks for attending today's session!\n\n";
    message += "These are some curated notes about the topics discussed today, and here's a link to some resources if you want to learn more:\n";
    message += "[Insert Link Here]\n\n";
    message += "If you have any doubts from today’s session, feel free to join the doubt session at 9 PM:\n";
    message += "[Insert Doubt Session Link Here]\n\n";
  } else if (status === "Absent") {
    message += "I hope this email finds you well. We missed you at today's session and would really like to see you in action.\n\n";
    message += "Here's a recording of today’s session:\n";
    message += "[Insert Recording Link Here]\n\n";
  }

  message += "Regards,\nTeam PresencePulse";
  MailApp.sendEmail(email, subject, message);
}

