import random
import json
import tweepy
import os
from config import *
from datetime import datetime, timezone
from games_scrape import scrape_matches
from X_scrape import scrape_club_tweet
from bets_scrape import scrape_bets


def test_games_scrape():
    print("Checking games scraping function...")
    # Check games_scrape functions
    assert os.path.exists(MATCHES_KEY_FILE), "The MATCHES_KEY_FILE path doesn't exist"
    print("All matches and their kickoff times:")
    study_season = 2025
    matches = scrape_matches(study_season)
    assert os.path.exists(MATCHES_FILE), "MATCHES_FILE was not created"
    num = random.randint(0,len(matches))
    assert "homeTeam" in matches[num] and "awayTeam" in matches[num] and "utcDate" in matches[num], "The scraped match structure is incorrect"
    print("games scraping successful")

def test_bets_scrape():
    print("Checking bets scraping function...")
    # Check bets_scrape functions
    study_season = 2025
    try:
        get_betting_odd_csv_url(study_season)
    except:
        raise Exception("Failed to get betting odd csv url")
    scrape_bets(study_season)
    assert os.path.exists(BETS_FILE), "The BETS_FILE was not created"
    assert os.path.getsize(BETS_FILE) > 0, "The BETS_FILE was empty"
    print("bets scraping successful")

def test_X_scrape():
    print("Checking X scraping function...")
    # Check if X scraping is successful
    assert os.path.exists(X_TOKEN_FILE), "The X_TOKEN_FILE path doesn't exist"
    with open(X_TOKEN_FILE, "r") as f:
        BEARER_TOKEN = f.read().strip()
    client = tweepy.Client(bearer_token=BEARER_TOKEN)

    assert os.path.exists(CLUB_IDS_FILE), "The CLUB_IDS_FILE path doesn't exist"
    try: #X authentication check
        with open(CLUB_IDS_FILE,"r") as f:
            clubIDs = json.load(f)
        random_club = random.choice(list(clubIDs.keys()))
        random_clubID = clubIDs[random_club]
        print(f"Testing club {random_club} with ID \"{random_clubID}\"")
        user = client.get_user(id=random_clubID)
        print("Authentication successful")
    except Exception as e1:
        raise SystemExit("X scrape authentification failed.")

    try: #tweet fetching check
        tweets = client.get_users_tweets(
            id=random_clubID,
            max_results=5,
            tweet_fields=["created_at", "public_metrics"]
        )
        for tweet in tweets.data:
            print(f"{tweet} \n")
        print("Fetching tweets successful")
    except Exception as e2:
        raise SystemExit("X scrape fetching tweets failed.")

if __name__ == "__main__":
    print("Running tests for Final Project:")

    test_games_scrape()
    test_bets_scrape()
    test_X_scrape()
    #REMINDER: the test_X_scrape() function would need X API token to run and will cost you a few cents per each test
    print("All tests passed")

