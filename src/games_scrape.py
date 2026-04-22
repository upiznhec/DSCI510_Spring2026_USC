import requests
import json
from config import MATCHES_FILE, MATCHES_KEY_FILE, FOOTBALL_DATA_URL
from datetime import datetime

def scrape_matches(season) -> list: #download all match data from https://www.football-data.org/
    #load match key token
    with open(MATCHES_KEY_FILE, "r") as f_match_token:
        api_key = f_match_token.read().strip()
    params = {"season": season}
    headers = {"X-Auth-Token": api_key}

    response = requests.get(FOOTBALL_DATA_URL, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()
    all_matches = data["matches"]

    with open(MATCHES_FILE, "w") as f:
        json.dump(all_matches, f, ensure_ascii=False, indent=2)

    return all_matches