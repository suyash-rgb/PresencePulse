import numpy as np
import imutils
import pickle
import time
import cv2
import os
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials  
from googleapiclient.errors import HttpError

embeddingModel = "model/openface_nn4.small2.v1.t7"
embeddingFile = "output/embeddings.pickle"
recognizerFile = "output/recognizer.pickle"
labelEncFile = "output/le.pickle"
conf = 0.8  # Confidence threshold adjusted to 90%

print("Loading face detector...")
prototxt = "model/deploy.prototxt"
model = "model/res10_300x300_ssd_iter_140000.caffemodel"
detector = cv2.dnn.readNetFromCaffe(prototxt, model)

print("Loading face recognizer...")
embedder = cv2.dnn.readNetFromTorch(embeddingModel)

recognizer = pickle.loads(open(recognizerFile, "rb").read())
le = pickle.loads(open(labelEncFile, "rb").read())

def mark_attendance(name):
    try:
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        CLIENT_SECRET_FILE = 'client_secret_345628488689-k82iong9nirrts1l6hbc79o3ca12gih1.apps.googleusercontent.com.json'  # Update this path
        creds = None
        
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        service = build('sheets', 'v4', credentials=creds)

        # ID of your Google Sheet
        spreadsheet_id = '1hhXvuRO-IjZgM26YSzJjfzS407UHzHhCsS9IY4FIBKM'
        range_name = 'Attendance!A1:Z1000'

        # Fetch data to find the correct column for today's date
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
        values = result.get('values', [])

        # Find the column for today's date
        today_date = time.strftime("%d/%m/%Y")
        date_row = values[0]
        date_col = -1
        for idx, col_date in enumerate(date_row):
            try:
                if time.strftime("%d/%m/%Y", time.strptime(col_date, "%d/%m/%Y")) == today_date:
                    date_col = idx
                    break
            except ValueError:
                continue
        
        if date_col == -1:
            raise ValueError("Today's date is not found in the header row of the sheet.")

        # Normalize recognized name 
        normalized_name = name.strip().lower()

        # Find the row for the student in the second column 
        for row_index, row in enumerate(values[1:], start=2): # Start from the second row and index 2 
            if row and len(row) > 1 and row[1].strip().lower() == normalized_name: # Check the second column 
                # Mark attendance in the correct column 
                sheet.values().update( 
                    spreadsheetId=spreadsheet_id, 
                    range=f'Attendance!{chr(65+date_col)}{row_index}', 
                    valueInputOption='USER_ENTERED', 
                    body={'values': [['Present']]} 
                ).execute() 
                print(f"Attendance marked for {name}.") 
                return True 
            else: 
                raise ValueError(f"Student name '{name}' not found in the sheet.") 
        
    except HttpError as err: 
        print(f"An error occurred: {err}") 
    return False
box = []
print("Starting face recognition...")
cam = cv2.VideoCapture(0)
time.sleep(2.0)

while True:
    _, frame = cam.read()
    frame = imutils.resize(frame, width=600)
    (h, w) = frame.shape[:2]
    imageBlob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0), swapRB=False)

    detector.setInput(imageBlob)
    detections = detector.forward()

    for i in range(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]

        if confidence > conf:
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            face = frame[startY:endY, startX:endX]
            (fH, fW) = face.shape[:2]

            if fW < 20 or fH < 20:
                continue

            faceBlob = cv2.dnn.blobFromImage(face, 1.0 / 255, (96, 96), (0, 0, 0), swapRB=True, crop=False)
            embedder.setInput(faceBlob)
            vec = embedder.forward()

            preds = recognizer.predict_proba(vec)[0]
            j = np.argmax(preds)
            proba = preds[j]
            name = le.classes_[j]
            text = "{} : {:.2f}%".format(name, proba * 100)
            y = startY - 10 if startY - 10 > 10 else startY + 10
            cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 0, 255), 2)
            cv2.putText(frame, text, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 2)

            # Debugging: Print recognized name and probability
            #print(f"Recognized Name: {name}, Probability: {proba * 100:.2f}%")

            if proba * 100 > 80:  # Check if the accuracy is greater than 90%
                if mark_attendance(name):
                    print(f"Welcome {name}")
                    cam.release()
                    cv2.destroyAllWindows()
                    break

        cv2.imshow("Frame", frame)

    if cv2.getWindowProperty("Frame", cv2.WND_PROP_VISIBLE) < 1:  # Close button clicked
        break

    key = cv2.waitKey(1) & 0xFF 
    if key == 27: # ESC key to quit break
        break

# Release the camera and close all OpenCV windows
cam.release()
cv2.destroyAllWindows()
