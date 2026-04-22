import pandas as pd
import numpy as np
import json
import sqlite3
from config import *


### LOAD DATA
def load_matches():
    with open(MATCHES_FILE, "r") as f1:
        matches = json.load(f1)

    rows = []
    for match in matches:
        if match["status"] == "FINISHED":#Only finished matches
            rows.append({
                "kickoff_time": pd.to_datetime(match["utcDate"], utc=True),
                "home_team" : match["homeTeam"]["shortName"],
                "away_team": match["awayTeam"]["shortName"],
                "home_goals": match["score"]["fullTime"]["home"],
                "away_goals": match["score"]["fullTime"]["away"],
                "winner": match["score"]["winner"]
            })

    return pd.DataFrame(rows)


def load_bets():
    raw_df = pd.read_csv(BETS_FILE)
    conn = sqlite3.connect(DB_FILE)
    raw_df.to_sql("raw_bets", conn, index=False, if_exists="replace")
    query = """
        SELECT
            HomeTeam AS home_team,
            AwayTeam AS away_team,
            AvgH AS avg_home_odds,
            AvgD AS avg_draw_odds,
            AvgA AS avg_away_odds
        FROM raw_bets
    """

    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


### Unify team names
def unify_team_names(df):
    standard_variant_map = {}
    for standard_name, variants in TEAM_MAPPING.items():
        for key in variants.values():
            standard_variant_map[key] = standard_name

    df["home_team"] = df["home_team"].map(standard_variant_map)
    df["away_team"] = df["away_team"].map(standard_variant_map)
    return df


### Compute probabilities and "surprisingness" of results
### The probability of a result is calculated by (1/bet_odd)
### A result is qualified as "surprising" if it's probability is < 0.35
def compute_prob(df):
    df["home_probability"] = 1 / df["avg_home_odds"]
    df["draw_probability"] = 1 / df["avg_draw_odds"]
    df["away_probability"] = 1 / df["avg_away_odds"]
    return df

def compute_surprise(df, threshold = 0.4):
    conn = sqlite3.connect(DB_FILE)
    df.to_sql("matches", conn, index=False, if_exists="replace")
    query = """
        SELECT
            *,
            CASE WHEN winner = 'HOME_TEAM' AND home_prob < ? THEN True
                WHEN winner = 'DRAW' AND draw_prob < ? THEN True
                WHEN winner = 'AWAY_TEAM' AND away_prob < ? THEN True
                ELSE False
            END AS surprising_result
        FROM matches
    """
    result_df = pd.read_sql_query(query, conn, params=([threshold, threshold, threshold]))
    conn.close()

    return result_df



df = load_matches()
#df = load_bets()
df = unify_team_names(df)
#df = compute_prob(df)
print(df.columns.tolist())
for line in df.values.tolist():
    print(line)