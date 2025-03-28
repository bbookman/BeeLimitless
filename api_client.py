import requests
import json
import os  # Import os for directory handling
from config import base_url, api_key  # Import configuration
from datetime import datetime  # Import datetime for date formatting
import re  # Import regular expressions for flexible matching

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
            short_summary = conversation.get("short_summary")
            if not short_summary:
                short_summary = "N/A"  # Use the short summary if available
                
            if summary:  # Only include conversations with a non-null summary
                # Parse and format the date
                raw_date = conversation.get("updated_at", "N/A")
                if raw_date != "N/A":
                    try:
                        if "." in raw_date:
                            parsed_date = datetime.strptime(raw_date, "%Y-%m-%dT%H:%M:%S.%fZ")
                        else:
                            parsed_date = datetime.strptime(raw_date, "%Y-%m-%dT%H:%M:%SZ")
                        formatted_date = parsed_date.strftime("%B %A %d, %Y")
                    except ValueError:
                        formatted_date = raw_date  # Fallback to raw date if parsing fails
                else:
                    formatted_date = "N/A"

                # Extract segments: summary, atmosphere, and key takeaways
                cleaned_summary, atmosphere, key_takeaways = extract_segments(summary)

                # Write the formatted Markdown
                file.write(f"## {formatted_date}\n")
                if short_summary:
                    file.write(f"### Short Summary\n{short_summary}\n\n")

                if atmosphere:
                    file.write(f"#### Atmosphere\n{atmosphere}\n\n")
                if key_takeaways:
                    file.write(f"#### Key Takeaways\n{key_takeaways}\n\n")
                file.write(f"Conversation ID: {conversation.get('id')}\n\n")
                if cleaned_summary:
                    file.write(f"#### Full Summary\n{cleaned_summary}\n\n")

    print(f"Response saved as Markdown in {output_file}")

def extract_segments(summary):
    """
    Extracts the summary, atmosphere, and key takeaways as separate variables.
    Searches for the specific section headers and extracts text between them.
    Returns cleaned_summary, atmosphere, and key_takeaways.
    """
    # Initialize variables
    cleaned_summary = None
    atmosphere = None
    key_takeaways = None

    # Use regular expressions to identify and extract each section
    # Match "Summary:" followed by any text up to "Atmosphere:" or "Key Takeaways:"
    summary_match = re.search(r"Summary:\s*(.*?)\s*(Atmosphere:|Key Takeaways:|$)", summary, re.DOTALL)
    if summary_match:
        cleaned_summary = summary_match.group(1).strip()  # Extract and clean the summary text

    # Match "Atmosphere:" followed by any text up to "Key Takeaways:" or the end
    atmosphere_match = re.search(r"Atmosphere:\s*(.*?)\s*(Key Takeaways:|$)", summary, re.DOTALL)
    if atmosphere_match:
        atmosphere = atmosphere_match.group(1).strip()  # Extract and clean the atmosphere text

    # Match "Key Takeaways:" followed by any text up to the end
    key_takeaways_match = re.search(r"Key Takeaways:\s*(.*)", summary, re.DOTALL)
    if key_takeaways_match:
        key_takeaways = key_takeaways_match.group(1).strip()  # Extract and clean the key takeaways text

    return cleaned_summary, atmosphere, key_takeaways

if __name__ == "__main__":
    print("\nFetching data ...")
    get_data("conversations")  # Fetch data from the 'conversations' endpoint