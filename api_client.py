import requests
from config import base_url, api_key  # Import configuration

# Function to send a GET request to a specific endpoint
def get_data(endpoint=""):
    # Construct the full URL by appending the endpoint to the base URL
    url = f"{base_url}/v1/me{endpoint}" if endpoint else base_url

    # Add the API key to the headers
    headers = {
        "Authorization": f"Bearer {api_key}"  # Common format for API key in headers
    }
    
    # Send the GET request
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print("GET request successful!")
        print(response.json())  # Print the JSON response
    else:
        print(f"GET request failed with status code: {response.status_code}")
        print(response.text)  # Print the error message

if __name__ == "__main__":
    print("Fetching data from the base URL...")
    get_data()  # Fetch data from the base URL

    print("\nFetching data from the 'get_conversations' endpoint...")
    get_data("get_conversations")  # Fetch data from the 'get_conversations' endpoint