import requests
import json
import os

from config import *

output_directory = "articles"
os.makedirs(output_directory, exist_ok=True)


for key, url in bad_patterns.items():
    response = requests.get(url, headers=headers_v3_api)
    if response.status_code == 200:
        data = response.json()
        
        all_articles = []

        total_pages = data.get("total_pages", 1)
        
        for page in range(1, total_pages + 1):
            page_url = f"{url}&page={page}"
            response = requests.get(page_url, headers=headers_v3_api)
            if response.status_code == 200:
                page_data = response.json()
                articles = page_data.get("articles", [])
                all_articles.extend(articles)

        filename = os.path.join(output_directory, f"{key}.json")
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(all_articles, file, ensure_ascii=False, indent=4)
        print(f"Saved {filename}")
    else:
        print(f"Failed to fetch URL for key '{key}': {response.status_code}")
