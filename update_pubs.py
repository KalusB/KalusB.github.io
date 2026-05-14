import requests
import json
import os
import sys

# Konfiguration
ORCID = "0000-0002-4578-4019"
API_TOKEN = os.environ.get("ADS_API_TOKEN")

if not API_TOKEN:
    print("❌ FEHLER: ADS_API_TOKEN ist in der Umgebung nicht gesetzt!")
    sys.exit(1)

def fetch_publications():
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    # Wir suchen nach deiner ORCID
    query = f'orcid:{ORCID} sort:date desc'
    params = {
        "q": query,
        "fl": "title,author,year,pub,bibcode",
        "rows": 100
    }
    
    print(f"📡 Starte ADS-Abfrage für ORCID: {ORCID}...")
    response = requests.get("https://api.adsabs.harvard.edu/v1/search/query", params=params, headers=headers)
    
    if response.status_code == 200:
        docs = response.json().get('response', {}).get('docs', [])
        print(f"✅ Erfolg: {len(docs)} Publikationen gefunden.")
        return docs
    else:
        print(f"❌ ADS API Fehler: {response.status_code}")
        print(f"Antwort: {response.text}")
        return None

pubs = fetch_publications()

if pubs is not None:
    # Wir erstellen die Datei IMMER, auch wenn sie leer ist, damit 'git add' nicht abstürzt
    with open('publications.json', 'w', encoding='utf-8') as f:
        json.dump(pubs, f, ensure_ascii=False, indent=4)
    print("💾 publications.json wurde geschrieben.")
else:
    print("⚠️ Skript abgebrochen, keine Datei erstellt.")
    sys.exit(1)