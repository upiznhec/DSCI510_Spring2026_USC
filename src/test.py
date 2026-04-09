import random
import json
import tweepy
from datetime import datetime, timezone
from games_scrape import scrape_matches, all_kickoff
from X_scrape import scrape_club_tweet

if __name__ == "__main__":
    print("Running tests for Final Project:")

    # Check games_scrape functions
    print("All matches and their kickoff times:")
    with open("../APIkeys/matches_key.txt", 'r') as f:
        API_KEY = f.read().strip()
    URL = "https://api.football-data.org/v4/competitions/PL/matches"
    study_season = 2025

    matches = all_kickoff(API_KEY, URL, study_season)
    home = input("Home team?")
    away = input("Away team?")
    for match in matches:
        if match["home_team"] == home and match["away_team"] == away:
            print(match["kickoff_time"])


    # Check if X scraping is successful
    with open("../APIkeys/X_bearertoken.txt", "r") as f:
        BEARER_TOKEN = f.read().strip()
    client = tweepy.Client(bearer_token=BEARER_TOKEN)

    try: #X authentication check
        with open("../data/EPLClubIDs.json","r") as f:
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
            max_results=10,
            tweet_fields=["created_at", "public_metrics"]
        )
        for tweet in tweets.data:
            print(f"{tweet} \n")
        print("Fetching tweets successful")
    except Exception as e2:
        raise SystemExit("X scrape fetching tweets failed.")

    #Check if scrape_club_tweet is returning the expected results
    dt = datetime(2026, 1, 8, 20, 0, 0, tzinfo=timezone.utc)
    print(scrape_club_tweet("LFC", dt, BEARER_TOKEN))

