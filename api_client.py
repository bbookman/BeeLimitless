import requests
import json
import os  # Import os for directory handling
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
        data = response.json()  # Parse the JSON response
        save_as_markdown(data)  # Save the response as a Markdown file
    else:
        print(f"GET request failed with status code: {response.status_code}")
        print(response.text)  # Print the error message

# Function to save the API response as a Markdown file
def save_as_markdown(data):
    # Define the output directory and file
    output_dir = "markdown"
    output_file = os.path.join(output_dir, "conversations.md")

    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)  # Create the directory if it doesn't exist

    # Open the file for writing
    with open(output_file, "w") as file:
        # Write a title
        file.write("# Conversations\n\n")

        # Iterate through the conversations and format them as Markdown
        for conversation in data.get("conversations", []):
            summary = conversation.get("summary")
            if summary:  # Only include conversations with a non-null summary
                file.write(f"## Date: {conversation.get('updated_at', 'N/A')}\n")
                cleaned_summary = summary.replace("Summary: ", "", 1) 
                file.write(f"### {summary}\n\n")
              
                file.write(f"\nConversation ID: {conversation.get('id')}\n\n")

    print(f"Response saved as Markdown in {output_file}")

if __name__ == "__main__":
    print("\nFetching data ...")
    get_data("conversations")  # Fetch data from the 'conversations' endpoint