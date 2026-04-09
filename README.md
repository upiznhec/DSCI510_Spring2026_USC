##Analyzing the Correlation Between Surprising Match Results and X Tweet Engagement Levels for English Premier League Clubs in the 2025-2026 Season
**DSCI 510 – Principles of Programming for Data Science**  
Nanpu Chen
University of Southern California – Spring 2026

## Project Overview
This project investigates whether surprising English Premier League (hereinafter referred to as “EPL”) match outcomes influence engagement levels on EPL club’s official X (formerly Twitter) account. Pre-match betting odds will be used to determine expected match results and actual match results will be compared to identify whether the result is a surprising win, an expected result, or a surprising loss. Engagement level is analyzed by collecting certain metrics (likes, retweets, and replies) from post-match posts of the clubs’ main official X account. The study aims to evaluate whether unexpected match results correlate with EPL clubs’ social media engagement.

## Files
**EPLClubsXNameList.txt** is a list of X handles (e.g. "@ManCity", "afcbournemouth", etc.) which 2025/26 season EPL clubs use on X (former twitter)
**bets_scrape.py** has a function scrape_bets that automates the process of downloading a csv file of pre-match betting odds from https://www.football-data.co.uk/
**games_scrape.py** contains 2 functions:
  1.scrape_matches(api_key,url,season) downloads all match data from https://www.football-data.org/, accessed through a specific API key. The API key oughts to be stored in position "../APIkeys/matches_key.txt"
  2.all_kickoff(api_key, url, season) invokes scrape_matches() and returns a list of the kickoff time all matches played in EPL. Matches are stored in dictionaries of keys "home_team", "away_team", and "kickoff_time"
**X_scrape.py** contains 2 functions:
  1. find_and_store_club_id(token) gets all the user_ids of EPL clubs' X accounts using the EPLClubsXNameList.txt and stores them into a "../data/EPLClubIDs.json" file. An official X API (v2) Bearer Token is required, the token oughts to be stored in position "../APIkeys/X_bearertoken.txt"
  2. scrape_club_tweet(club_name, kickoff_utc, api_key) scrapes tweets of a given club in a certain time window related to the kickoff time and returns a dictionary that contains data of X engagement changes pre- and post-match. Below is what exactly it does:
    (1). The function aims to measure match result influence using a window-based uplift approach for a specific team and a specific match
    (2). For each match, **"Pre-match window"** is defined as Kickoff time − 6 hours → Kickoff, **Post-match window:** is defined as Kickoff time + 105 minutes → Kickoff time + 465 minutes
    (3). Engagement of a tweet is calculated by adding public engagement metrics. That is, Likes + Replies + Retweets + Quotes.
    (4). The function retrieves public engagement metrics of all tweets of the club posted between these two windows and calculates the average of their tweets' engagements respectively
    (5). The function returns a dictionary that includes keys: "club", "kickoff time", "pre-game average engagement", "post-game average engagement", and "engagement changes" (post_avg-pre_avg)

## Repository Structure
│
├── src/
│ ├── games_scrape.py # Scrapes match data from football-data API
│ ├── bets_scrape.py # Retrieves betting odds data
│ ├── X_scrape.py # Scrapes engagement data from X API
│ ├── test.py # Testing and validation script
│ └── EPLClubsXNameList.txt # A list of X handles of EPL clubs
│
├── .gitignore # Excludes data, results, API keys
└── README.md

## API Requirements
This project requires:
- football-data.org API key
- X API Bearer Token
Please create a file under main called "APIkeys" and store the key and token in a one-line .txt file respectively under this file.
E.g.,
│
├── APIkeys/
│ ├── `APIkeys/matches_key.txt`
│ └──`APIkeys/X_bearertoken.txt`
├── src/
