import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin
import uuid

def fetch_car_plate_images(url, folder_path, prefix):
    # Ensure the folder exists
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    page_number = 30  # Start with the first page
    while True:
        page_url = f"{url}&PN={page_number}"  # Adjust the URL parameter for pagination
        print(f"Scraping page: {page_url}")
        
        response = requests.get(page_url)
        if response.status_code != 200:
            print(f"Failed to retrieve the webpage: {page_url}")
            break

        soup = BeautifulSoup(response.content, 'html.parser')

        detail_links = [urljoin(url, a['href']) for a in soup.find_all('a', href=True) if 'annonces.cfm?pdtid=' in a['href']]
        for detail_link in detail_links:
            fetch_images_from_detail_page(detail_link, folder_path, prefix)

        next_button = soup.find('a', string='Next')
        if not next_button:
            break
        page_number += 1

def fetch_images_from_detail_page(detail_url, folder_path, prefix):
    response = requests.get(detail_url)
    if response.status_code != 200:
        print(f"Failed to retrieve the webpage: {detail_url}")
        return

    soup = BeautifulSoup(response.content, 'html.parser')
    img_tags = soup.find_all('img', src=lambda value: value and '/produitsedr/produit_bgph/' in value)

    for idx, img in enumerate(img_tags):
        img_url = img['src']
        img_url = urljoin(detail_url, img_url)
        
        try:
            img_data = requests.get(img_url).content
        except Exception as e:
            print(f"Failed to download {img_url}: {e}")
            continue
        
        # Generate a unique filename using UUID
        img_name = os.path.join(folder_path, f'{prefix}{uuid.uuid4()}.jpg')
        try:
            with open(img_name, 'wb') as handler:
                handler.write(img_data)
            print(f"Downloaded {img_name}")
        except Exception as e:
            print(f"Failed to save {img_name}: {e}")

# Example usage
fetch_car_plate_images('https://www.voursa.com/Index.cfm?gct=1&sct=11&gv=1&av=0&bv=0&cv=0&dv=0&ev=0&fv=0&genre=0&pp=0&localisation=0&pmin=0&pmax=0', 'mauritania_car_plates', 'web1_')

