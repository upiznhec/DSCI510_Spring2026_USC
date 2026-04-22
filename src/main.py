import pandas as pd
import numpy as np
import sqlite3
import os
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

    if not os.path.exists(CLUB_IDS_FILE):
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
                engagement_dict[(home_std, kickoff_dt)] = eng_lift_home
            if eng_lift_away:
                engagement_dict[(away_std, kickoff_dt)] = eng_lift_away

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
        USING (home_team, away_team);
    """
    merged_df = pd.read_sql_query(query, conn)
    conn.close()
    merged_df = merged_df.dropna(subset=["avg_home_odds", "avg_draw_odds", "avg_away_odds"])#drop rows where betting odds are missing

    ### Compute whether the result is surprising
    merged_df = compute_probability(merged_df)
    merged_df = compute_surprise(merged_df, threshold=threshold)

    ### Expand dataset to clubs from matches
    club_df = expand_dataset_2_club(merged_df)

    ### Attach Engagement lift and
    ### drop rows where engagement_changes is None, implying the club hasn't posted during pre- or post-match window
    ### "Didn't post" is inferred from a zero average engagement, based on the assumption that
    ### any real post from an EPL club X account generates at least 1 engagement in the window.
    engagement_changes = []
    pre_avg_col = []
    post_avg_col = []
    have_posted = []
    initial_len = len(club_df)
    for _, row in club_df.iterrows():
        key = (row["club"], row["kickoff_time"])
        entry = engagement_dict.get(key)

        pre_avg = entry["pre-game_average_engagement"]
        post_avg = entry["post-game_average_engagement"]
        pre_avg_col.append(pre_avg)
        post_avg_col.append(post_avg)

        if pre_avg == 0 or post_avg == 0:
            engagement_changes.append(None)
            have_posted.append(False)
        else:
            engagement_changes.append(entry["engagement_changes"])
            have_posted.append(True)

    club_df["engagement_changes"] = engagement_changes
    club_df["pre_game_average_engagement"] = pre_avg_col
    club_df["post_game_average_engagement"] = post_avg_col
    club_df["relative_lift"] = (club_df["engagement_changes"] / club_df["pre_game_average_engagement"])
    club_df = club_df[have_posted].reset_index(drop=True)
    print(f"Dropped {initial_len - len(club_df)} entries")

    return club_df

if __name__ == "__main__":
    main(2025,0.35)