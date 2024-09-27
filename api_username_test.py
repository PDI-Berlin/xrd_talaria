import requests
from getpass import getpass

base_url = "http://intra8.pdi-berlin.de/nomad-oasis/api/v1"

# Step 1: User Authentication
def authenticate(username,password):
    '''
    This function gets users e-mail and password to generate
    an access token to be used in API calls.
    '''
    login_url = f"{base_url}/auth/token"

    params = dict(username=username,  password=password)

    response = requests.get(
        login_url, params=params)
    print(login_url, params)
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

if __name__ == "__main__":
    username = input("Enter your NOMAD Lab username: ")
    password = getpass("Enter your NOMAD Lab password: ")
    # Authenticate user
    token = authenticate(username, password)

    if token:
        # Upload file
        full_name = get_username_me(token)
        print(f"Full name: {full_name}")
