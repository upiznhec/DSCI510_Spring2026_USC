import tweepy
import json
from config import X_TOKEN_FILE, CLUB_IDS_FILE, CLUB_NAMES_FILE
from datetime import datetime, timedelta

def find_and_store_club_id():
    #load X_API_Token
    with open(X_TOKEN_FILE, "r") as f_xtoken:
        api_key = f_xtoken.read().strip()
    client = tweepy.Client(bearer_token=api_key)
    club_ids = {}

    with open(CLUB_NAMES_FILE, "r") as f1:
        for line in f1:
            club_handle = line.strip()
            club_user = client.get_user(username=club_handle)
            club_ids[club_handle] = club_user.data.id

    with open(CLUB_IDS_FILE,"w",encoding="utf-8") as f2:
        json.dump(club_ids,f2,indent=2)


def scrape_club_tweet(club_name, kickoff_utc):
    #scrapes tweets of a given club in a time certain window related to the kickoff time
    # and returns a dictionary that contains data of X engagement changes pre- and post-match

    #load X_API_Token
    with open(X_TOKEN_FILE, "r") as f_xtoken:
        api_key = f_xtoken.read().strip()

    #reach club X account for scraping
    with open(CLUB_IDS_FILE,"r") as f3:
        club_ids = json.load(f3)
    try:
        club_id = club_ids[club_name]
    except KeyError:
        raise ValueError(f"{club_name} incorrect")
    client = tweepy.Client(bearer_token=api_key)

    #Define time window
    pre_start = kickoff_utc - timedelta(hours=6)
    pre_end = kickoff_utc
    pre_start_iso = pre_start.isoformat().replace("+00:00", "Z")
    pre_end_iso = pre_end.isoformat().replace("+00:00", "Z")

    post_start = kickoff_utc + timedelta(minutes=105)
    post_end = kickoff_utc + timedelta(minutes=6*60+105)
    post_start_iso = post_start.isoformat().replace("+00:00", "Z")
    post_end_iso = post_end.isoformat().replace("+00:00", "Z")

    #Scrape all tweets within the pre-match time window and find tweet with the highest engagement
    pre_response = client.get_users_tweets(
        id=club_id,
        max_results=100,
        tweet_fields=["created_at", "public_metrics", "text"],
        start_time=pre_start_iso,
        end_time=pre_end_iso
    )
    pre_engagement = []
    if not pre_response.data:
        pre_engagement = []
    else:
        for tweet in pre_response.data:
            metrics = tweet.public_metrics
            engagement = (
                int(metrics["like_count"]) +
                int(metrics["reply_count"]) +
                int(metrics["retweet_count"]) +
                int(metrics["quote_count"])
            )
            pre_engagement.append(engagement)

    # Scrape all tweets within the post-match time window and find tweet with the highest engagement
    post_response = client.get_users_tweets(
        id=club_id,
        max_results=100,
        tweet_fields=["created_at", "public_metrics", "text"],
        start_time=post_start_iso,
        end_time=post_end_iso
    )
    post_engagement = []
    if not post_response.data:
        post_engagement = []
    else:
        for tweet in post_response.data:
            metrics = tweet.public_metrics
            engagement = (
                    int(metrics["like_count"]) +
                    int(metrics["reply_count"]) +
                    int(metrics["retweet_count"]) +
                    int(metrics["quote_count"])
            )
            post_engagement.append(engagement)

    #Calculate the average engagement of posts for both pre and post windows
    pre_avg = sum(pre_engagement) / len(pre_engagement) if pre_engagement else 0
    post_avg = sum(post_engagement) / len(post_engagement) if post_engagement else 0
    engagement_changes = post_avg - pre_avg

    return {
        "club": club_name,
        "kickoff time": kickoff_utc,
        "pre-game average engagement": pre_avg,
        "post-game average engagement": post_avg,
        "engagement changes": engagement_changes,
    }
