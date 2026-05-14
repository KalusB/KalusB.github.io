import requests
import json
import os

# Configuration
# Replace '0000-0002-4578-4019' with your ORCID or use a specific ADS query
ORCID = "0000-0002-4578-4019"
API_TOKEN = os.environ.get("ADS_API_TOKEN") # We will set this in GitHub
SEARCH_URL = "https://api.adsabs.harvard.edu/v1/search/query"

def fetch_publications():
    query = f'orcid:{ORCID} sort:date desc'
    params = {
        "q": query,
        "fl": "title,author,year,pub,bibcode,doi,arxiv_id",
        "rows": 100
    }
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    
    response = requests.get(SEARCH_URL, params=params, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data['response']['docs']
    else:
        print(f"Error: {response.status_code}")
        return None

def save_to_json(pubs):
    # This saves the data to a file your website can read
    with open('publications.json', 'w', encoding='utf-8') as f:
        json.dump(pubs, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    publications = fetch_publications()
    if publications:
        save_to_json(publications)
        print(f"Successfully updated {len(publications)} papers.")
