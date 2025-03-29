import requests
import json
import os
from config import base_url, api_key
from datetime import datetime
import re

# Function to send a GET request to a specific endpoint with paging
def get_data(endpoint=""):
    current_page = 1  # Start with the first page
    total_pages = 1  # Initialize total_pages to 1 to enter the loop

    while current_page <= total_pages:
        # Construct the full URL with the page parameter
        url = f"{base_url}/v1/me/{endpoint}?page={current_page}"
        
        # Add the API key to the headers
        headers = {
            "accept": "application/json",
            "x-api-key": api_key
        }
        
        # Debug: Print the headers and URL
        print("Headers:", headers)
        print("URL:", url)

        # Send the GET request
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            print(f"GET request successful for page {current_page}!")
            data = response.json()  # Parse the JSON response
            
            # Process the data and save Markdown files
            save_as_markdown(data)
            
            # Update paging information
            current_page = data.get("currentPage", current_page)  # Get the current page from the response
            total_pages = data.get("totalPages", total_pages)  # Get the total pages from the response
            current_page += 1  # Increment to the next page
        else:
            print(f"GET request failed with status code: {response.status_code}")
            print(response.text)  # Print the error message
            break

# Function to save the API response as Markdown files, one per day
def save_as_markdown(data):
    # Define the output directory
    base_dir = "data"  # Higher-level directory
    markdown_dir = os.path.join(base_dir, "markdown")  # Markdown directory inside /data

    # Ensure the directories exist
    if not os.path.exists(markdown_dir):
        os.makedirs(markdown_dir)  # Create the directories if they don't exist

    # Iterate through the conversations and format them as Markdown
    for conversation in data.get("conversations", []):
        summary = conversation.get("summary")
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
                    file_date = parsed_date.strftime("%Y-%m-%d")  # For the filename
                except ValueError:
                    formatted_date = raw_date  # Fallback to raw date if parsing fails
                    file_date = "unknown"
            else:
                formatted_date = "N/A"
                file_date = "unknown"

            # Extract segments: summary, atmosphere, and key takeaways
            cleaned_summary, atmosphere, key_takeaways = extract_segments(summary)

            # Define the output file for this day
            output_file = os.path.join(markdown_dir, f"{file_date}.md")

            # Open the file for appending (to handle multiple conversations on the same day)
            with open(output_file, "a") as file:
                # Write the formatted Markdown
                if cleaned_summary:
                    file.write(f"## Date: {formatted_date}\n")
                    file.write(f"### {cleaned_summary}\n\n")
                   
                if atmosphere:
                    file.write(f"#### Atmosphere\n{atmosphere}\n\n")
                if key_takeaways:
                    file.write(f"#### Key Takeaways\n{key_takeaways}\n\n")
                if cleaned_summary:
                    file.write(f"Conversation ID: {conversation.get('id')}\n\n")
                    file.write("---\n")  # Separator for multiple conversations
                    file.write("\n")  # Extra newline for readability
                
    # Print the location of saved files
    if os.path.exists(markdown_dir):
        print(f"Markdown files saved in {markdown_dir}")
    else:
        print("Failed to create output directory.")

# Function to extract segments: summary, atmosphere, and key takeaways
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