#!/usr/bin/env python

import requests
from getpass import getpass

# NOMAD API base URL
base_url = "http://intra8.pdi-berlin.de/nomad-oasis/api/v1"

# Step 1: User Authentication
def authenticate(username,password):

    login_url = f"{base_url}/auth/token"

    response = requests.get(
        login_url, params=dict(username=username,  password=password))

    if response.status_code == 200:
        print("Authentication successful!")
        return response.json()['access_token']
    else:
        print(f"Authentication failed: {response.status_code} - {response.text}")
        return None

# Step 2: File Upload
def upload_file(token):
    # Prompt for the file path
    file_path = input("Enter the path of the file you want to upload: ")

    try:
        # Open the file in binary mode
        with open(file_path, 'rb') as file:
            # Set the upload URL and headers
            upload_url = f"{base_url}/uploads"
            headers = {
                "Authorization": f"Bearer {token}"
            }
            files = {
                "file": file
            }

            # Send the POST request to upload the file
            response = requests.post(upload_url, headers=headers, files=files)

            if response.status_code == 200:
                print("File uploaded successfully!")
                print(f"Response: {response.status_code} - {response.text}")
            else:
                print(f"File upload failed: {response.status_code} - {response.text}")

    except FileNotFoundError:
        print("File not found. Please check the path and try again.")

if __name__ == "__main__":
    username = input("Enter your NOMAD Lab username: ")
    password = getpass("Enter your NOMAD Lab password: ")
    # Authenticate user
    token = authenticate(username, password)

    if token:
        # Upload file
        upload_file(token)
