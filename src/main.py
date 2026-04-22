import pandas as pd
import numpy as np
import sqlite3
from config import *
from analysis import *
from games_scrape import scrape_matches
from bets_scrape import scrape_bets
from X_scrape import find_and_store_club_id , scrape_club_tweet


def main(season, threshold=0.35):

    ### Scrape and write matches and bets data
    try:
        scrape_matches(season)
        scrape_bets(season)
    except ValueError:
        raise ValueError("Please check whether the season you are analyzing is valid")

    find_and_store_club_id()

    engagement_dict = {}

    with open(MATCHES_FILE, "r") as f1:
        matches = json.load(f1)

    for match in matches:
        if match['status'] == 'FINISHED':
            home_short = match['homeTeam']['shortName']
            away_short = match['awayTeam']['shortName']

            #translate to standard name
            home_std = find_standard_name(home_short)
            away_std = find_standard_name(away_short)

            #get kickoff time for each match
            kickoff_dt = pd.to_datetime(match['utcDate'], utc=True)

            #Scrape engagement data from both clubs and store them
            home_x_handle = TEAM_MAPPING[home_std]["x_handle"]
            away_x_handle = TEAM_MAPPING[away_std]["x_handle"]
            eng_lift_home = scrape_club_tweet(home_x_handle, kickoff_dt)
            eng_lift_away = scrape_club_tweet(away_x_handle, kickoff_dt)
            if eng_lift_home:
                engagement_dict[(home_std, kickoff_dt)] = eng_lift_home["engagement_changes"]
            if eng_lift_away:
                engagement_dict[(away_std, kickoff_dt)] = eng_lift_away["engagement_changes"]

    ### Build the dataset
    matches_df = load_matches()
    bets_df = load_bets()
    matches_df = unify_team_names(matches_df)
    bets_df = unify_team_names(bets_df)

    conn = sqlite3.connect(DB_FILE)
    matches_df.to_sql("matches", conn, index=False, if_exists="replace")
    bets_df.to_sql("bets", conn, index=False, if_exists="replace")
    query = """
        SELECT *
        FROM matches
        LEFT JOIN bets
        ON matches.home_team = bets.home_team AND matches.away_team = bets.away_team;
    """
    merged_df = pd.read_sql_query(query, conn)
    conn.close()
    merged_df = merged_df.dropna(subset=["avg_home_odds", "avg_draw_odds", "avg_away_odds"])#drop rows where betting odds are missing

    ### Compute whether the result is surprising
    merged_df = compute_probability(merged_df)
    merged_df = compute_surprise(merged_df, threshold=threshold)

    ### Expand dataset to clubs from matches
    club_df = expand_dataset_2_club(merged_df)

    ### Attach Engagement lift
    lifts = []
    for _, row in club_df.iterrows():
        key = (row["club"], row["kickoff_time"])
        lifts.append(engagement_dict.get(key, None))

    club_df["engagement_changes"] = lifts

    return club_df

if __name__ == "__main__":
    main(2025,0.35)