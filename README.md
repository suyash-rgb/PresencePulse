# PresencePulse : Face Recognition Based Automated Attendance System


![Alt Text](https://github.com/suyash-rgb/PresencePulse/blob/7546e56fd96b26c27631b5953fbf2097e517c7eb/Images/photo_2024-12-11_11-28-26.jpg)

# Project Description

**PresencePulse** is an innovative face recognition-based automated attendance system designed to streamline the process of attendance tracking in educational institutions and workplaces. Using cutting-edge face recognition technology, PresencePulse aims to enhance accuracy and efficiency in recording attendance.

Structure of the PresencePulse GUI Application: <br> <br>

![Alt Text](https://github.com/suyash-rgb/PresencePulse/blob/1a44656d96c2c7ef4534544058aa45887c14b9c1/Images/PresencePulse%20GUI%20Structure%20and%20Workflow.png)



# Prerequisites

- **Python 3.x**
- **QtDesigner**
  

# Setup Instructions

## Setting Up OAuth Client ID in Google Cloud Console

1. **Go to Google Cloud Console**: Visit the [Google Cloud Console](https://console.cloud.google.com/) and log in with your Google account.

2. **Create or Select a Project**: On the project selector page, select an existing project or create a new one.

3. **Enable APIs & Services**: In the left sidebar, click on "APIs & Services" and then select "Library".

4. **Enable Google Sheets API**: Search for "Google Sheets API" and enable it.

5. **Create Credentials**: Go to "Credentials" and click on "Create Credentials".

6. **Select OAuth Client ID**: Choose "OAuth client ID" from the options.

7. **Configure Consent Screen**: If prompted, configure the consent screen by providing the necessary information like product name, support email, etc.

8. **Create Client ID**: Choose "Web application" as the application type. Add your ngrok domain to the "Authorized redirect URIs" and "Authorized JavaScript origins". Click "Create" to generate the OAuth client ID. Note down the client ID and client secret.

## Using ngrok to Claim a Static Domain

1. **Sign Up for ngrok**: If you don't have an ngrok account, sign up for one on the [ngrok website](https://ngrok.com/).

2. **Log In to ngrok**: Log in to your ngrok account.

3. **Navigate to Domains**: Go to "Cloud Edge" and select "Domains".

4. **Claim Your Static Domain**: Follow the prompts to claim your unique, static domain.

5. **Use Your Static Domain**: Start ngrok with your static domain using the command: <br>
    (e.g., `ngrok http --domain=[your-static-domain] 80`) 


# Understanding ngrok and ngrok Tunnels

## What is ngrok?
ngrok is a powerful tool that allows you to create secure tunnels to your local server, making it accessible from the internet. It is particularly useful for testing webhooks, APIs, and local development projects without needing to deploy them to a remote server.

## What is an ngrok Tunnel?
An ngrok tunnel is a secure, encrypted connection created by ngrok that allows external access to a locally hosted server. When you run ngrok, it assigns a public URL to your local server, enabling anyone with the URL to access your local application. This is extremely useful for:

- **Development and Testing**: Quickly sharing your local development environment with collaborators or clients.
- **API Integration**: Testing webhooks and API integrations that require public URL callbacks.
- **IoT and Device Management**: Connecting IoT devices running in external networks.



# Code Summaries

### 1. **Dataset Preparation and Management Script**
- **Description**: This script manages the creation and organization of the image dataset used for face recognition. It includes functions add images from local folders, capture images using a camera, and manage student records in Google Sheets.
- **Main Functions**:
  - **Add Images from Folder**: Copies images from a local folder to the dataset.
  - **Capture Images from Camera**: Uses the camera to capture images and save them to the dataset.
  - **Add Student to Google Sheet**: Adds a new student record to the Google Sheet with the next available roll number.

### 2. **Face Embeddings Extraction Script**
- **Description**: This script processes images to extract facial embeddings using a pre-trained deep learning model. The extracted embeddings are saved in a pickle file for later use in face recognition tasks.
- **Main Functions**:
  - Verify and load face detection and embedding models.
  - Process each image to extract face embeddings.
  - Save the embeddings and corresponding names to a pickle file.

### 3. **Training Face Recognition Model Script**
- **Description**: This script trains a Support Vector Machine (SVM) model for face recognition using pre-computed face embeddings. It saves the trained recognizer model and the label encoder for later use.
- **Main Functions**:
  - Load face embeddings and encode labels.
  - Train an SVM model for face recognition.
  - Save the trained recognizer model and the label encoder to pickle files.

### 4. **Real-Time Face Recognition and Attendance Marking Script**
- **Description**: This script performs real-time face recognition and marks attendance in a Google Sheets document. It uses pre-trained models for face detection and face embedding extraction.
- **Main Functions**:
  - Initialize and load face detection and embedding models.
  - Capture real-time video from the camera, detect faces, and compute embeddings.
  - Recognize faces using the trained SVM model and mark attendance in Google Sheets.
 
### 5. **Data Visualization Script**
- **Description**: This script generates visual representations of attendance data using the Matplotlib library. It fetches data from Google Apps Script APIs and plot various graphs such as bar graphs, pie charts, and line charts to visualize attendance trends.
- **Main Functions**:
  - Fetch daily attendance data and plot bar and pie charts.
  - Fetch monthly attendance overview and plot a bar graph.
  - Fetch data for the most attentive and least attentive students and plot bar graphs.
  - Fetch attendance trend data and plot a line chart.

### 6. Recording Attendance and Automated Mailing (GAS)

- **Description**: This Google Apps Script (GAS) automates the process of recording attendance and sending personalized emails based on attendance status updates in a Google Sheet.

- **Email Trigger**:  
  The script automatically triggers when a student's attendance status is updated in the "Attendance" sheet.
- **Send Email**:  
  Depending on the attendance status ("Present" or "Absent"), it sends a personalized email with relevant content, such as:  
  - Notes from the session.  
  - Session recording links.  
  - A reminder for follow-up actions, if applicable.


### 7. Attendance Calculation and Automated Mailing (GAS)

- **Description**: This Google Apps Script automates attendance calculation and notification processes at the end of each month.

- **Monthly Trigger Creation**:  
  - The script sets up a trigger that runs automatically on the last day of each month at 9 AM.  
  - This trigger initiates the attendance calculation and notification process. 
- **Calculate Attendance and Notify**:  
    - Computes the attendance percentage for each student in the "Attendance" sheet.  
    - If a student's attendance falls below 75%, their details are added to a notification list.  
- **Notify Short Attendance**:  
    - Sends an email to students (and their guardians) with attendance below the required threshold.  
    - The email includes:  
      - A notification about their short attendance.  
      - Encouragement to attend future sessions regularly.



# Contributing

If you'd like to contribute to this repository, please follow these guidelines:

1. **Fork the repository.**
2. **Create a new branch** (e.g., `git checkout -b feature/your-feature`).
3. **Commit your changes** (e.g., `git commit -m 'Add your feature'`).
4. **Push to the branch** (e.g., `git push origin feature/your-feature`).
5. **Open a Pull Request.**


# Contact

If you have any questions, feel free to reach out:

- **Email**: suyashbaoney58@gmail.com
- **LinkedIn**: [your-linkedin-profile](www.linkedin.com/in/suyash-baoney-bb38b3290)
