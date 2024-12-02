import requests
from bs4 import BeautifulSoup
import json
import re
import os

def scrape_english_monarchs():
    url = "https://en.wikipedia.org/wiki/List_of_English_monarchs"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    monarchs = []

    # Locate the main content table or section
    tables = soup.find_all('table', class_='wikitable')

    for table in tables:
        rows = table.find_all('tr')
        for row in rows[1:]:  # Skip the header row
            columns = row.find_all(['th', 'td'])

            if len(columns) < 2:
                continue  # Skip rows without enough columns

            #All of the relevent data is in the first column
            cell = columns[0]
            text = cell.get_text(strip=True)


            # Extract name
            link = cell.find('b')
            if link:
                name = link.get_text(strip=True)

            # Extract portrait
            portrait = None
            portrait_cell = row.find('img')
            if portrait_cell:
                portrait_link = "https:" + portrait_cell['src']
                # Download the portrait image
                if portrait_link:
                    image_name = name.replace(" ", "_") + ".jpg"
                    image_path = f'./monarchs/england/{image_name}'
                    os.makedirs(os.path.dirname(image_path), exist_ok=True)
                    if not os.path.exists(image_path):
                        image_response = requests.get(portrait_link)
                        with open(image_path, 'wb') as image_file:
                            image_file.write(image_response.content)
            portrait = image_path
            

            # Extract birth and death year
            birth_year = None
            death_year = None
            reign_period = None
            if '–' in text or '-' in text:
                text = re.sub(r"\[\d+", " ", text)
                translation_table = str.maketrans("[]()-–", "^^^ ^^")
                # Replace the characters
                trans_text = text.translate(translation_table)
                with open('debug.txt', 'a') as debug_file:
                    debug_file.write(trans_text + '\n')
                life_split = trans_text.replace('–', '^').split('^')[-3:]
                birth_year = life_split[0].strip()
                if len(life_split) > 1:
                    death_year = life_split[1].strip()
                reign_period = life_split[2].strip()


            monarchs.append({
                'name': name,
                'portrait': portrait,
                'start_year': birth_year,
                'end_year': death_year,
                'reign_time': reign_period,
                'country': 'England'
            })

    return monarchs


# Scrape the data
data = scrape_english_monarchs()

# Save as JSON
with open('./monarchs/english_monarchs.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, indent=4, ensure_ascii=False)

# print("Data saved to english_monarchs.json")
