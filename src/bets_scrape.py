import requests
from config import BETS_FILE

def scrape_bets(url):
    response = requests.get(url)

    with open(BETS_FILE,"w") as f:
        f.write(response.text)
