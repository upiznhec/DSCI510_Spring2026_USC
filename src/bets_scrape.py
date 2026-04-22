import requests
from config import get_betting_odd_csv_url, BETS_FILE

def scrape_bets(season):
    url = get_betting_odd_csv_url(season)
    response = requests.get(url)
    response.raise_for_status()

    with open(BETS_FILE,"w") as f:
        f.write(response.text)