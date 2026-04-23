## Analyzing the Correlation Between Surprising Match Results and X Tweet Engagement Levels for English Premier League Clubs in the 2025-2026 Season
**DSCI 510 – Principles of Programming for Data Science**  
Nanpu Chen
University of Southern California – Spring 2026

## Project Overview
This project investigates whether surprising English Premier League (hereinafter referred to as “EPL”) match outcomes influence engagement levels on EPL club’s official X (formerly Twitter) account. Pre-match betting odds will be used to determine expected match results and actual match results will be compared to identify whether the result is a surprising win, a surprising draw, an expected result, or a surprising loss. Engagement level is analyzed by collecting certain metrics (likes, retweets, and replies) from post-match posts of the clubs’ main official X account. The study aims to evaluate whether unexpected match results correlate with EPL clubs’ social media engagement.

### Project Precautions
This project needs an X bearer token to scrape the tweets from the EPL club's X account. You can create an X bearer token at X Development Concole (access through https://developer.x.com/). You also need to purchase enough credit to run this project or else X would return either 402 Payment Required or 403 Forbidden. For a full season, the project takes around $60-70 of credit to run. This project also auto-saves caches of engagement data so if something crashes while running results.ipynb or main.py, what is already scraped would store safely in your directory so there is no need to concern having to burn extra money to re-run and fix.

This project also uses an API key to access all the match data, that key could be found and generate by accessing https://www.football-data.org/.

## Files
**EPLClubsXNameList.txt** is a list of X handles (e.g. "@ManCity", "@afcbournemouth", etc.) which 2025/26 season EPL clubs use on X (former twitter)

**config.py** centralizes all file paths, API key file paths, data source URLs, and the TEAM_MAPPING dictionary that unifies the three different team-naming conventions used by the betting CSV, the matches API, and the X handles.

**bets_scrape.py** has a function scrape_bets that automates the process of downloading a csv file of pre-match betting odds from https://www.football-data.co.uk/

**games_scrape.py** contains a function scrape_matches(season) which downloads all EPL match data from https://www.football-data.org/, accessed through a specific API key. The API key is read from the path defined by MATCHES_KEY_FILE in config.py (by default APIkeys/matches_key.txt). The function writes the raw match list to data/All_matches.json and also returns it.

**X_scrape.py** contains 2 functions:
  1. find_and_store_club_id() gets all the user_ids of EPL clubs' X accounts using the EPLClubsXNameList.txt and stores them into a "../data/EPLClubIDs.json" file. An official X API (v2) Bearer Token is required, read from the path defined by X_TOKEN_FILE in config.py (by default APIkeys/X_bearertoken.txt).
  2. scrape_club_tweet(club_name, kickoff_utc) scrapes tweets of a given club in a certain time window related to the kickoff time and returns a dictionary that contains data of X engagement changes pre- and post-match. Below is what exactly it does:

    (1).The function aims to measure match result influence using a window-based uplift approach for a specific team and a specific match
    (2).For each match, "Pre-match window" is defined as Kickoff time − 6 hours → Kickoff, Post-match window is defined as Kickoff time + 105 minutes → Kickoff time + 465 minutes
    (3).Engagement of a tweet is calculated by adding public engagement metrics. That is, Likes + Replies + Retweets + Quotes.
    (4).The function retrieves public engagement metrics of all tweets of the club posted between these two windows and calculates the average of their tweets' engagements respectively
    (5).The function returns a dictionary that includes keys: "club", "kickoff time", "pre-game average engagement", "post-game average engagement", and "engagement changes" (post_avg-pre_avg)
    (6).Results are cached to disk under `data/engagement_cache/` as JSON files (one per club-match). On re-runs, cached results are returned instantly without hitting the X API. This makes iterating on the pipeline free once the initial scrape is complete.

**analysis.py** contains the helper functions that build and clean the analysis dataset after raw data has been scraped:
1. load_matches() reads data/All_matches.json and returns a DataFrame of finished matches with kickoff time, teams, goals, and the winner.
2. load_bets() reads the betting CSV into a SQLite staging table and returns the relevant columns (home team, away team, average home/draw/away odds) as a DataFrame.
3. unify_team_names(df) unifies all the different names that are used across the three sources in the home_team and away_team columns to a single standard name per club, using TEAM_MAPPING from config.py. (E.g., Nottingham Forest is short-named "Nottingham" in the match data json file from https://www.football-data.org/, named "Nott'm Forest" in the bets csv file from www.football-data.co.uk/, and has a handle "NUFC" on X. This function unifies all these names in a dataframe into its standard name "Nottingham Forest")
4. find_standard_name(name), looks up the standard club name from any of its variants (bet name, matches short name, or X handle). Different from unify_team_names(), it works on specific string names while the former works on whole dataframes. (E.g., find_standard_name("Nott'm Forest") returns a standard string name "Nottingham Forest")
5. compute_probability(df) adds the three implied probability columns (home/draw/away) as 1 divided by the corresponding average odd. (In soccer gambling, Betting odds can be converted into implied probabilities by taking their reciprocals, and in a fair market these probabilities would sum to 1 because they represent all possible outcomes. In real markets, the sum is slightly above 1 due to the bookmaker’s built-in margin (overround). For deeper understanding you can take a look at https://www.sportmonks.com/glossary/bookmaker-odds/)
6. compute_surprise(df, threshold=0.35) flags matches where the actual winning outcome had a pre-match implied probability below the threshold. That said, a result is qualified as "surprising" if it's possibility of happening is lower than the variable threshold (in default set to 0.35)
7. expand_dataset_2_club(df) expand the dataset from one row per match to two rows per match (since for each match we have two club accounts to analyze), and labels each club's result as expected, surprise_win, surprise_draw, or surprise_loss from that club's perspective.

**main.py** is the single entry point for the full pipeline. Calling main(season, threshold=0.35) scrapes matches, betting odds, and X engagement; unifies team names across sources; merges via SQLite; computes implied probabilities and surprise categories; expands to the club level; and attaches four engagement columns to each club-match: pre_game_average_engagement, post_game_average_engagement, engagement_changes (post minus pre), and relative_lift (engagement_changes/pre_game_average_engagement). 
Based on the assumption that any real post from an EPL club X account would generate at least 1 engagement, club-matches with 0 pre- or post-match average engagement is treated as "the club didn't post anything in the window" and that row is dropped. The function returns the final analysis DataFrame.

## Repository Structure
    │
    ├── src/
    │ ├── results.ipynb # Analysis notebook and result graphs creation
    │ ├── main.py # Runs the full pipeline
    │ ├── config.py # Store all paths, URLs, and TEAM_MAPPING in a centralized way
    │ ├── analysis.py # DataFrame building, cleaning, surprise
    │ ├── games_scrape.py # Scrapes match data from football-data API
    │ ├── bets_scrape.py # Retrieves betting odds data
    │ ├── X_scrape.py # Scrapes engagement data from X API
    │ ├── test.py # Testing and validation script
    │ └── EPLClubsXNameList.txt # A list of X handles of EPL clubs
    │
    ├── doc/
    │ ├── Nanpu_Chen_progress_report.pdf # Progress report as of April 8, 2026
    │ └── Nanpu_Chen_presentation.pdf # Final presentation slides
    │
    ├── data/ #gitignored
    │ ├── engagement_cache/ # Per-club-match JSON cache (so that you don't burn extra X token credits when something crashe)
    │ ├── All_matches.json # Raw matches from football-data API
    │ ├── bets.csv # Raw betting odds CSV
    │ ├── EPLClubIDs.json # X user IDs for each club
    │ └── project.db # database to stage the sql queries in the codes
    │
    ├── requirement.txt
    ├── .gitignore # Excludes data, results, API keys
    └── README.md

## API Requirements
This project requires:
- football-data.org API key
- X API Bearer Token

Please create a file under main called "APIkeys" and store the key and token in a one-line .txt file respectively under this file. E.g.:

    │
    ├── APIkeys/
    │ ├── `APIkeys/matches_key.txt`
    │ └──`APIkeys/X_bearertoken.txt`
    ├── src/
    ├── doc/

## AI Usage Statement
AI is used and ONLY used in small sections of X_scrape.py to generate the piece of code which is used to build a filesystem-safe cache filename from the club handle + kickoff time and to write a JSON-serializable copy (kickoff_time must be a string on disk). The parts that are AI-generated is labled as "#AI generated:" and ends with "# AI generated up until this point". The coding agent being used is Claude from Anthropic.