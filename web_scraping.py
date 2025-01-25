import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# The URL of the page to scrape images from
page_url = "https://adaajaipur.com/"

# Send a request to fetch the HTML content of the page
response = requests.get(page_url)

# Check if the request was successful
if response.status_code == 200:
    print("Successfully fetched the page")
    page_html = response.text
    
    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(page_html, 'html.parser')
    
    # Find all image tags
    img_tags = soup.find_all('img')

    # List to store all the image URLs
    img_urls = []

    # Extract the image URLs
    for img in img_tags:
        img_url = img.get('src')
        if img_url:
            # Convert relative URLs to absolute URLs
            img_url = urljoin(page_url, img_url)
            img_urls.append(img_url)

    # Base directory to save images
    base_directory = "downloaded_images"

    # Create the base directory if it doesn't exist
    if not os.path.exists(base_directory):
        os.makedirs(base_directory)

    # Download each image
    for img_url in img_urls:
        # Extract the image name from the URL (e.g., SSY_2319copy.jpg)
        img_name = img_url.split("/")[-1].split("?")[0]  # Handle query params in URLs
        
        # Define the file path
        file_path = os.path.join(base_directory, img_name)
        
        # Try to download the image
        try:
            print(f"Trying to download: {img_url}")
            img_response = requests.get(img_url, stream=True)
            
            # Check if the request was successful
            if img_response.status_code == 200:
                with open(file_path, 'wb') as img_file:
                    for chunk in img_response.iter_content(1024):
                        img_file.write(chunk)
                print(f"Downloaded: {file_path}")
            else:
                print(f"Failed to download {img_url} - Status Code: {img_response.status_code}")
        except Exception as e:
            print(f"Error downloading {img_url}: {e}")
else:
    print(f"Failed to retrieve the page. Status Code: {response.status_code}")
