import requests
from config import base_url, api_key  # Import configuration

# Function to send a GET request to a specific endpoint
def get_data(endpoint=""):
    # Construct the full URL by appending the endpoint to the base URL
    url = f"{base_url}/v1/me/{endpoint}" if endpoint else base_url

    # Add the API key to the headers
    headers = {
        "accept": "application/json",  # Ensure the API accepts JSON responses
        "x-api-key": api_key           # Use 'x-api-key' as required by the API
    }
    
    # Debug: Print the headers and URL
    print("Headers:", headers)
    print("URL:", url)

    # Send the GET request
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print("GET request successful!")
        print(response.json())  # Print the JSON response
    else:
        print(f"GET request failed with status code: {response.status_code}")
        print(response.text)  # Print the error message

if __name__ == "__main__":
    print("\nFetching data ...")
    get_data("conversations")  # Fetch data from the 'conversations' endpoint