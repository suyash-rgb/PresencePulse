import os
import shutil
import cv2
from pygoogle_image import image as pi
from pathlib import Path
import json
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def download_images_from_google(query, dataset_path, limit=20):
    pi.download(query, limit=limit)
    google_image_folder = Path().resolve() / "images" / query.replace(" ", "_")
    
    # Ensure the directory exists before moving its contents
    target_folder = Path(dataset_path) / query.replace(" ", "_")
    target_folder.mkdir(parents=True, exist_ok=True)
    
    if google_image_folder.exists() and google_image_folder.is_dir():
        for file_path in google_image_folder.iterdir():
            if file_path.is_file():
                shutil.move(str(file_path), str(target_folder))
        shutil.rmtree(google_image_folder.parent)  # Remove the entire 'images' folder
        print(f"Downloaded {limit} images from Google for query: {query} into {target_folder}")
    else:
        print(f"Error: The directory {google_image_folder} does not exist.")

# Function to create a dataset directory if it doesn't exist
def create_dataset_dir(dataset_path):
    if not os.path.exists(dataset_path):
        os.makedirs(dataset_path)

# Function to add images from a folder
def add_images_from_folder(folder_path, dataset_path, subfolder_name):
    target_folder = Path(dataset_path) / subfolder_name
    target_folder.mkdir(parents=True, exist_ok=True)
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            shutil.copy(file_path, target_folder)
    print(f"Added images from folder: {folder_path} to {target_folder}")

# Function to capture images from the camera
def capture_images_from_camera(name, dataset_path, num_images=50):
    target_folder = Path(dataset_path) / name
    target_folder.mkdir(parents=True, exist_ok=True)
    cam = cv2.VideoCapture(0)
    count = 0
    while count < num_images:
        ret, frame = cam.read()
        if not ret:
            print("Failed to capture image")
            break
        cv2.imshow("Press 'q' to exit", frame)
        image_path = os.path.join(target_folder, f"{name}_{count}.jpg")
        cv2.imwrite(image_path, frame)
        count += 1
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cam.release()
    cv2.destroyAllWindows()
    print(f"Captured {count} images from camera for: {name} in {target_folder}")

# Function to get Google Sheets service
def get_sheets_service():
    creds = None
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    # Using OAuth 2.0 for desktop app
    json_file_path = os.path.join(os.getcwd(), 'client_secret_345628488689-k82iong9nirrts1l6hbc79o3ca12gih1.apps.googleusercontent.com.json')
    flow = InstalledAppFlow.from_client_secrets_file(json_file_path, SCOPES)
    creds = flow.run_local_server(port=0)
    
    service = build('sheets', 'v4', credentials=creds)
    return service

# Function to add a student to Google Sheet
def add_student_to_sheet(student_name):
    try:
        service = get_sheets_service()
        spreadsheet_id = '1hhXvuRO-IjZgM26YSzJjfzS407UHzHhCsS9IY4FIBKM'  # Replace this with your actual spreadsheet ID
        range_name = 'Attendance!A:B'

        # Fetch existing data to calculate the next roll number
        result = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
        values = result.get('values', [])

        # Calculate next roll number
        if not values or len(values) == 1:
            next_roll_no = 101
        else:
            next_roll_no = 101 + len(values)
        
        # Format student name to replace underscores with spaces
        formatted_student_name = student_name.replace("_", " ")
        
        # Add new student
        new_row = [next_roll_no, formatted_student_name]
        service.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption='USER_ENTERED',
            body={'values': [new_row]}
        ).execute()

        print(f"Added student '{formatted_student_name}' with roll number {next_roll_no} to the sheet.")
    
    except HttpError as err:
        print(f"An error occurred: {err}")
        if err.resp.status == 404:
            print("The spreadsheet ID or sheet name might be incorrect. Please verify and try again.")

# Function to delete all student records from dataset and Google Sheet
def delete_all_records():
    try:
        service = get_sheets_service()
        spreadsheet_id = '1hhXvuRO-IjZgM26YSzJjfzS407UHzHhCsS9IY4FIBKMet_id'  # Replace this with your actual spreadsheet ID
        range_name = 'Attendance!A:B'

        # Clear the data in the specified range
        service.spreadsheets().values().clear(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            body={}
        ).execute()

        # Clear the dataset directory
        dataset_path = "dataset"
        if os.path.exists(dataset_path):
            shutil.rmtree(dataset_path)
        create_dataset_dir(dataset_path)

        print("Deleted all student records from the dataset and Google Sheet.")
    
    except HttpError as err:
        print(f"An error occurred: {err}")
        if err.resp.status == 404:
            print("The spreadsheet ID or sheet name might be incorrect. Please verify and try again.")

# Main script
if __name__ == "__main__":
    dataset_path = "dataset"
    create_dataset_dir(dataset_path)

    while True:
        print("\nChoose an option to create a dataset:")
        print("1. Add images from a folder")
        print("2. Download images from Google")
        print("3. Capture images from camera")
        print("4. Delete all student records")
        print("5. Exit")
        choice = input("Enter your choice (1/2/3/4/5): ")

        if choice == '1':
            folder_path = input("Enter the folder path: ")
            subfolder_name = input("Enter the name of the person or subfolder: ")
            add_images_from_folder(folder_path, dataset_path, subfolder_name)
            add_student_to_sheet(subfolder_name)
        elif choice == '2':
            query = input("Enter search query: ")
            limit = int(input("Enter number of images to download: "))
            download_images_from_google(query, dataset_path, limit)
            target_folder = Path(dataset_path) / query.replace(" ", "_")
            if target_folder.exists() and len(list(target_folder.glob('*'))) > 0:
                add_student_to_sheet(query.replace(" ", "_"))
            else:
                print("No images were downloaded. Entry not added to Google Sheet.")
        elif choice == '3':
            name = input("Enter the name of the person: ")
            num_images = int(input("Enter number of images to capture: "))
            capture_images_from_camera(name, dataset_path, num_images)
            add_student_to_sheet(name)
        elif choice == '4':
            delete_all_records()
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")
