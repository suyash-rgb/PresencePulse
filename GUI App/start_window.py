from PyQt5 import QtCore, QtGui, QtWidgets
from visuals_window import Ui_VisualsWindow  # Import the visuals window class
import subprocess

class Ui_StartWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1124, 899)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(100, 700, 93, 28))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.run_script_add_student)  # Connect button to function

        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(270, 700, 93, 28))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.run_script_process)

        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(420, 700, 121, 28))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.run_script_record_attendance)

        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(790, 690, 221, 28))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.clicked.connect(self.show_visuals_window)  # Connect button to function

        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(100, 40, 911, 601))
        self.textBrowser.setObjectName("textBrowser")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1124, 26))
        self.menubar.setObjectName("menubar")
        self.menuPresensePulse = QtWidgets.QMenu(self.menubar)
        self.menuPresensePulse.setObjectName("menuPresensePulse")
        MainWindow.setMenuBar(self.menubar)
        self.menubar.addAction(self.menuPresensePulse.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Add Student"))
        self.pushButton_2.setText(_translate("MainWindow", "Process"))
        self.pushButton_3.setText(_translate("MainWindow", "Record Attendance"))
        self.pushButton_4.setText(_translate("MainWindow", "Attendance Report and Evaluation"))
        self.menuPresensePulse.setTitle(_translate("MainWindow", "PresensePulse"))

    def run_script_add_student(self):
        self.run_script_and_display_output('1_createDatasets1.py')

    def run_script_process(self):
        self.run_two_scripts_and_display_output('2_preprocessingEmbeddings.py', '3_trainModel.py')

    def run_script_record_attendance(self):
        self.run_script_and_display_output('4_recordAttendance.py')

    def run_script_and_display_output(self, script_name):
        process = subprocess.Popen(['python', script_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()
        if error:
            self.textBrowser.setText(error.decode('utf-8'))
        else:
            self.textBrowser.setText(output.decode('utf-8'))

    def run_two_scripts_and_display_output(self, script1, script2):
        # Run the first script
        process1 = subprocess.Popen(['python', script1], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output1, error1 = process1.communicate()

        # Run the second script
        process2 = subprocess.Popen(['python', script2], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output2, error2 = process2.communicate()

        # Concatenate the outputs and errors
        output = output1 + output2
        error = error1 + error2

        # Display the concatenated output and errors
        if error:
            self.textBrowser.setText(error.decode('utf-8'))
        else:
            self.textBrowser.setText(output.decode('utf-8'))

    def show_visuals_window(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_VisualsWindow()
        self.ui.setupUi(self.window)
        self.window.show()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_StartWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
