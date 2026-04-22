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
    data = response.json()
    all_matches = data["matches"]

    with open(MATCHES_FILE, "w") as f:
        json.dump(all_matches, f, ensure_ascii=False, indent=2)

    return all_matches


def all_kickoff(season) -> list: # returns a list of the starting time and ending time for each match
    all_matches = scrape_matches(season)

    kickoff_times = []
    for match in all_matches:
        kickoff_dt = datetime.fromisoformat(match["utcDate"].replace("Z", "+00:00"))
        kickoff_times.append({
            "home_team": match["homeTeam"]["shortName"],
            "away_team": match["awayTeam"]["shortName"],
            "kickoff_time": kickoff_dt
        })

    return kickoff_times

