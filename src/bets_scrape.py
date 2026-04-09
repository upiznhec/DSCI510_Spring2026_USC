import requests


def scrape_bets(url):
    response = requests.get(url)

    with open("../data/bets.csv","w") as f:
        f.write(response.text)


URL = "https://www.football-data.co.uk/mmz4281/2526/E0.csv"
scrape_bets(URL)