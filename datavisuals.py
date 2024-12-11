import matplotlib.pyplot as plt
import requests
import json

def DailyAttendance():
  # API endpoint
  api_url = 'https://script.google.com/macros/s/AKfycby1wqVBWoqiW_Yk4MW83lChn9QpYsYUZvmnTpN4yRLiz00BZ0qPjtAH4DrCCjyQ-SFWzg/exec?action=DailyAttendance'

  print("Fetching data from the API...")
  # Fetch data from the API
  response = requests.get(api_url)
  print("API response code: ", response.status_code)
  data = response.json()

  # Parse the JSON response
  present_percentage = float(data['presentPercentage'])
  absent_percentage = float(data['absentPercentage'])

  # Data for plotting
  labels = ['Present', 'Absent']
  percentages = [present_percentage, absent_percentage]
  colors = ['#1f77b4', '#ff7f0e']

  # Bar Graph
  plt.figure(figsize=(10, 5))

  plt.subplot(1, 2, 1)
  plt.bar(labels, percentages, color=colors)
  plt.title('Daily Attendance - Bar Graph')
  plt.xlabel('Attendance')
  plt.ylabel('Percentage')

  # Pie Chart
  plt.subplot(1, 2, 2)
  plt.pie(percentages, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
  plt.title('Daily Attendance - Pie Chart')

  plt.tight_layout()
  plt.show()

def MonthlyAttendanceOverview():
    api_url = 'https://script.google.com/macros/s/AKfycby1wqVBWoqiW_Yk4MW83lChn9QpYsYUZvmnTpN4yRLiz00BZ0qPjtAH4DrCCjyQ-SFWzg/exec?action=MonthlyAttendanceOverview'

    # Fetch data from the API
    response = requests.get(api_url)
    data = response.json()

    # Parse the JSON response
    names = list(data.keys())
    percentages = [float(data[name].strip('%')) for name in names]

    # Data for plotting
    colors = ['#1f77b4' if i % 2 == 0 else '#ff7f0e' for i in range(len(names))]

    # Plot Bar Graph
    plt.figure(figsize=(12, 6))
    plt.bar(names, percentages, color=colors)
    plt.title('Monthly Attendance Overview - Bar Graph')
    plt.xlabel('Students')
    plt.ylabel('Attendance Percentage')
    plt.xticks(rotation=45, ha='right')

    plt.tight_layout()
    plt.show()


def MostAttentiveStudents():
    # API endpoint
    api_url = 'https://script.google.com/macros/s/AKfycby1wqVBWoqiW_Yk4MW83lChn9QpYsYUZvmnTpN4yRLiz00BZ0qPjtAH4DrCCjyQ-SFWzg/exec?action=mostAttentiveStudents'

    # Fetch data from the API
    response = requests.get(api_url)
    data = response.json()

    # Parse the JSON response
    names = list(data.keys())
    percentages = [float(data[name].strip('%')) for name in names]

    # Data for plotting
    colors = ['#1f77b4' if i % 2 == 0 else '#ff7f0e' for i in range(len(names))]

    # Plot Bar Graph
    plt.figure(figsize=(12, 6))
    plt.bar(names, percentages, color=colors)
    plt.title('Most Attentive Students - Bar Graph')
    plt.xlabel('Students')
    plt.ylabel('Attendance Percentage')
    plt.xticks(rotation=45, ha='right')

    plt.tight_layout()
    plt.show()

def LeastAttentiveStudents():
    # API endpoint
    api_url = 'https://script.google.com/macros/s/AKfycby1wqVBWoqiW_Yk4MW83lChn9QpYsYUZvmnTpN4yRLiz00BZ0qPjtAH4DrCCjyQ-SFWzg/exec?action=leastAttentiveStudents'

    # Fetch data from the API
    response = requests.get(api_url)
    data = response.json()

    # Parse the JSON response
    names = list(data.keys())
    percentages = [float(data[name].strip('%')) for name in names]

    # Data for plotting
    colors = ['#1f77b4' if i % 2 == 0 else '#ff7f0e' for i in range(len(names))]

    # Plot Bar Graph
    plt.figure(figsize=(12, 6))
    plt.bar(names, percentages, color=colors)
    plt.title('Least Attentive Students - Bar Graph')
    plt.xlabel('Students')
    plt.ylabel('Attendance Percentage')
    plt.xticks(rotation=45, ha='right')

    plt.tight_layout()
    plt.show()

def AttendanceTrend():
    # API endpoint
    api_url = 'https://script.google.com/macros/s/AKfycby1wqVBWoqiW_Yk4MW83lChn9QpYsYUZvmnTpN4yRLiz00BZ0qPjtAH4DrCCjyQ-SFWzg/exec?action=AttendanceTrend'

    # Fetch data from the API
    response = requests.get(api_url)
    data = response.json()

    # Parse the JSON response
    dates = list(data.keys())
    present_percentages = [float(data[date]['presentPercentage']) for date in dates]
    absent_percentages = [float(data[date]['absentPercentage']) for date in dates]

    # Plot Line Chart
    plt.figure(figsize=(12, 6))
    plt.plot(dates, present_percentages, label='Present Percentage', marker='o')
    plt.plot(dates, absent_percentages, label='Absent Percentage', marker='o')
    plt.title('Attendance Trend - Line Chart')
    plt.xlabel('Date')
    plt.ylabel('Percentage')
    plt.xticks(rotation=45, ha='right')
    plt.legend()

    plt.tight_layout()
    plt.show()


# Main script
if __name__ == "__main__":

    while True:
        print("\nChoose an option to generate visual:- ")
        print("1. Daily Attendance")
        print("2. Monthly Attendance Overview")
        print("3. Most Attentive Students")
        print("4. Least Attentive Students")
        print("5. Attendance Trend")
        print("6. Exit")
        choice = input("Enter your choice (1/2/3/4/5/6): ")

        if choice == '1':
            DailyAttendance()
        elif choice == '2':
            MonthlyAttendanceOverview() 
        elif choice == '3':
            MostAttentiveStudents() 
        elif choice == '4':
            LeastAttentiveStudents()
        elif choice == '5':
            AttendanceTrend()
        elif choice == '6':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")
