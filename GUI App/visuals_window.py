from PyQt5 import QtCore, QtGui, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import requests
import json

class Ui_VisualsWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1123, 916)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(32, 680, 131, 28))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.show_daily_attendance)

        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(200, 680, 191, 28))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.show_monthly_attendance_overview)

        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(432, 680, 151, 28))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.show_most_attentive_students)

        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(610, 680, 161, 28))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.clicked.connect(self.show_least_attentive_students)

        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(960, 680, 131, 28))
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_5.clicked.connect(self.show_attendance_trend)

        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(30, 50, 1061, 621))
        self.frame.setAutoFillBackground(True)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1123, 26))
        self.menubar.setObjectName("menubar")
        self.menuPresencePulse = QtWidgets.QMenu(self.menubar)
        self.menuPresencePulse.setObjectName("menuPresencePulse")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuPresencePulse.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Daily Attendance"))
        self.pushButton_2.setText(_translate("MainWindow", "Monthly Attendance Overview"))
        self.pushButton_3.setText(_translate("MainWindow", "Most Attentive Students"))
        self.pushButton_4.setText(_translate("MainWindow", "Least Attentive Students"))
        self.pushButton_5.setText(_translate("MainWindow", "Attendance Trend"))
        self.menuPresencePulse.setTitle(_translate("MainWindow", "PresencePulse"))

    def show_daily_attendance(self):
        # Fetch data from the API
        response = requests.get('https://script.google.com/macros/s/AKfycby1wqVBWoqiW_Yk4MW83lChn9QpYsYUZvmnTpN4yRLiz00BZ0qPjtAH4DrCCjyQ-SFWzg/exec?action=DailyAttendance')
        data = response.json()

        # Create the plot
        fig, ax = Figure(), Figure().add_subplot(111)
        ax.bar(['Present', 'Absent'], [float(data['presentPercentage']), float(data['absentPercentage'])])
        ax.set_title('Daily Attendance')

        # Embed the plot in the frame
        self.embed_plot(fig)

    def show_monthly_attendance_overview(self):
        # Fetch data from the API
        response = requests.get('https://script.google.com/macros/s/AKfycby1wqVBWoqiW_Yk4MW83lChn9QpYsYUZvmnTpN4yRLiz00BZ0qPjtAH4DrCCjyQ-SFWzg/exec?action=MonthlyAttendanceOverview')
        data = response.json()

        # Create the plot
        fig, ax = Figure(), Figure().add_subplot(111)
        students = list(data.keys())
        attendance = [float(data[student]) for student in students]
        ax.bar(students, attendance)
        ax.set_title('Monthly Attendance Overview')
        ax.set_xticklabels(students, rotation=45, ha='right')

        # Embed the plot in the frame
        self.embed_plot(fig)

    def show_most_attentive_students(self):
        # Fetch data from the API
        response = requests.get('https://script.google.com/macros/s/AKfycby1wqVBWoqiW_Yk4MW83lChn9QpYsYUZvmnTpN4yRLiz00BZ0qPjtAH4DrCCjyQ-SFWzg/exec?action=mostAttentiveStudents')
        data = response.json()

        # Create the plot
        fig, ax = Figure(), Figure().add_subplot(111)
        students = list(data.keys())
        attendance = [float(data[student]) for student in students]
        ax.bar(students, attendance)
        ax.set_title('Most Attentive Students')
        ax.set_xticklabels(students, rotation=45, ha='right')

        # Embed the plot in the frame
        self.embed_plot(fig)

    def show_least_attentive_students(self):
        # Fetch data from the API
        response = requests.get('https://script.google.com/macros/s/AKfycby1wqVBWoqiW_Yk4MW83lChn9QpYsYUZvmnTpN4yRLiz00BZ0qPjtAH4DrCCjyQ-SFWzg/exec?action=leastAttentiveStudents')
        data = response.json()

        # Create the plot
        fig, ax = Figure(), Figure().add_subplot(111)
        students = list(data.keys())
        attendance = [float(data[student]) for student in students]
        ax.bar(students, attendance)
        ax.set_title('Least Attentive Students')
        ax.set_xticklabels(students, rotation=45, ha='right')

        # Embed the plot in the frame
        self.embed_plot(fig)

    def show_attendance_trend(self):
        # Fetch data from the API
        response = requests.get('https://script.google.com/macros/s/AKfycby1wqVBWoqiW_Yk4MW83lChn9QpYsYUZvmnTpN4yRLiz00BZ0qPjtAH4DrCCjyQ-SFWzg/exec?action=AttendanceTrend')
        data = response.json()

        # Create the plot
        fig, ax = Figure(), Figure().add_subplot(111)
        dates = list(data.keys())
        present_percentages = [float(data[date]['presentPercentage']) for date in dates]
        absent_percentages = [float(data[date]['absentPercentage']) for date in dates]

        ax.plot(dates, present_percentages, label='Present Percentage')
        ax.plot(dates, absent_percentages, label='Absent Percentage')
        ax.set_title('Attendance Trend')
        ax.set_xticklabels(dates, rotation=45, ha='right')
        ax.legend()

        # Embed the plot in the frame
        self.embed_plot(fig)

    def embed_plot(self, fig):
        # Clear any existing widgets in the frame
        for i in reversed(range(self.frame.layout().count())):
            self.frame.layout().itemAt(i).widget().setParent(None)

        # Create the canvas and add it to the frame
        canvas = FigureCanvas(fig)
        layout = QtWidgets.QVBoxLayout(self.frame)
        layout.addWidget(canvas)
        canvas.draw()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_VisualsWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
