import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

urls = [
    "https://adaajaipur.com/collections/a-line-kurta",
    "https://adaajaipur.com/collections/embroidery-kurta",
    "https://adaajaipur.com/collections/straight-kurta",
    "https://adaajaipur.com/collections/festive-suit-sets",
    "https://adaajaipur.com/collections/kurta-pant",
    "https://adaajaipur.com/collections/kurta-pant-and-dupatta",
    "https://adaajaipur.com/collections/ankle-gown",
    "https://adaajaipur.com/collections/festive-mal-gown",
    "https://adaajaipur.com/collections/gown-with-dupatta",
    "https://adaajaipur.com/collections/plazzo",
    "https://adaajaipur.com/collections/co-ords",
    "https://adaajaipur.com/collections/shirt",
    "https://adaajaipur.com/collections/short-top",
    "https://adaajaipur.com/collections/tunics",
]


def scrape_images_from_url(url):
    folder_name = url.split("/")[-1]
    print(f"Processing collection: {folder_name}")
    
    response = requests.get(url)
    if response.status_code == 200:
        print(f"Successfully fetched the page: {url}")
        page_html = response.text
        
        soup = BeautifulSoup(page_html, 'html.parser')

        product_cards = soup.find_all('div', class_="card-wrapper")
        print(f"Found {len(product_cards)} product cards.")

        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        for card in product_cards:
            try:
                product_name_tag = card.find('h3', class_="card__heading")
                if product_name_tag:
                    product_name = product_name_tag.text.strip()
                    safe_product_name = "".join(c if c.isalnum() else "_" for c in product_name)
                else:
                    print("No product name found, skipping...")
                    continue

                img_tag = card.find('img')
                if img_tag and img_tag.get('src'):
                    img_url = urljoin(url, img_tag.get('src'))
                else:
                    print(f"No image URL found for product: {product_name}")
                    continue

                img_extension = img_url.split('.')[-1].split('?')[0]  
                file_path = os.path.join(folder_name, f"{safe_product_name}.{img_extension}")

                print(f"Downloading {product_name} image from {img_url}...")
                img_response = requests.get(img_url, stream=True)

                if img_response.status_code == 200:
                    with open(file_path, 'wb') as img_file:
                        for chunk in img_response.iter_content(1024):
                            img_file.write(chunk)
                    print(f"Image saved as: {file_path}")
                else:
                    print(f"Failed to download {img_url} - Status Code: {img_response.status_code}")

            except Exception as e:
                print(f"Error processing card: {e}")
    else:
        print(f"Failed to retrieve the page. Status Code: {response.status_code}")

for url in urls:
    scrape_images_from_url(url)
