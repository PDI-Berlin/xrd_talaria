import requests
from getpass import getpass
import xml.etree.ElementTree as ET
import yaml
import os

base_url = "http://intra8.pdi-berlin.de/nomad-oasis/api/v1"

class xrdml():

    def modify_xrdml(file_path, user_name, sample_id):
        # Register the namespace
        ET.register_namespace('', "http://www.xrdml.com/XRDMeasurement/2.1")
        ET.register_namespace('xsi', "http://www.w3.org/2001/XMLSchema-instance")

        # Parse the XML file
        tree = ET.parse(file_path)
        root = tree.getroot()

        # Modify the author name
        for author in root.findall(".//{http://www.xrdml.com/XRDMeasurement/2.1}author"):
            name = author.find("{http://www.xrdml.com/XRDMeasurement/2.1}name")
            if name is not None:
                name.text = user_name

        # Modify the sample information
        for sample in root.findall(".//{http://www.xrdml.com/XRDMeasurement/2.1}sample"):
            id_elem = sample.find("{http://www.xrdml.com/XRDMeasurement/2.1}id")
            if id_elem is not None:
                id_elem.text = sample_id

        # Save the modified XML to a new file
        new_file_path = file_path.replace('.xrdml', '_modified.xrdml')
        tree.write(new_file_path, encoding='utf-8', xml_declaration=True)
        print(f"Modified file saved as: {new_file_path}")
        return new_file_path

class nomad_api():

    # User Authentication
    def authenticate(username,password):
        '''
        This function gets users e-mail and password to generate
        an access token to be used in API calls.
        '''
        login_url = f"{base_url}/auth/token"

        params = dict(username=username,  password=password)

        response = requests.get(
            login_url, params=params)
        if response.status_code == 200:
            print("Authentication successful!")
            return response.json()['access_token']
        else:
            print(f"Authentication failed: {response.status_code} - {response.text}")
            return None

    def get_username_me(api_token):
        '''
        This function gets user's API token and returns the name of the user.
        This is useful, when a file needs to be modified with the user's name.
        '''
        user_me_url = f"{base_url}/users/me"

        headers = {
            "Authorization": f"Bearer {api_token}"
        }

        try:
            response = requests.get(user_me_url, headers=headers)
            response.raise_for_status()  # Raises an exception for bad status codes

            if response.status_code == 200:
                return response.json()['name']
            else:
                return "Error fetching username!?"

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None

    # File Upload
    def upload_file(file_path, token):

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


    def get_upload_id(token):

        try:
            # Open the file in binary mode
            with open(file_path, 'rb') as file:
                # Set the upload URL and headers
                upload_url = f"{base_url}/uploads?roles=main_author&include_all=true&page_size=10&order=asc"
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

def get_file_path(config, username):
    if username in config and 'file_path' in config[username]:
        current_path = config[username]['file_path']
        change_path = input(f"Current file path is {current_path}. Do you want to change it? (y/n): ").lower()
        if change_path == 'y':
            new_path = input("Enter the new file path: ")
            config[username]['file_path'] = new_path
            return new_path
        return current_path
    else:
        new_path = input("Enter the path of the file you want to upload: ")
        if username not in config:
            config[username] = {}
        config[username]['file_path'] = new_path
        return new_path

def save_config(config):
    with open("config.yml", 'w') as f:
        yaml.dump(config, f)

if __name__ == "__main__":
    username = input("Enter your NOMAD Lab username: ")
    password = getpass("Enter your NOMAD Lab password: ")

    # Load or create config
    if os.path.exists("config.yml"):
        with open("config.yml", 'r') as f:
            config = yaml.safe_load(f) or {}
    else:
        config = {}

    # Authenticate user
    token = nomad_api.authenticate(username, password)

    if token:
        full_name = nomad_api.get_username_me(token)
        sample_id = input("Enter initial Sample name (Load Sample): ")

        while True:
            file_path = get_file_path(config, username)
            save_config(config)

            new_file_path = xrdml.modify_xrdml(file_path, full_name, sample_id)
            nomad_api.upload_file(new_file_path, token)

            upload_more = input("Do you want to upload another growth? (y/n): ").lower()
            if upload_more != 'y':
                break

            change_sample = input("Do you want to change the sample name? (Unload Sample) (y/n): ").lower()
            if change_sample == 'y':
                sample_id = input("Enter new Sample name: ")

        print("File upload process completed.")