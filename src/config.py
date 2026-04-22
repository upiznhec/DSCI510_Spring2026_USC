import os

#Project Layout
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
APIKEYS_DIR = os.path.join(BASE_DIR, "APIkeys")
DOC_DIR = os.path.join(BASE_DIR, "doc")
CLUB_NAMES_FILE = os.path.join(SRC_DIR, "EPLClubsXNameList.txt")
#This file is stored in src due to the code's necessity to run
# it's not a data file, it's just a list of EPL club names.

#Data files
MATCHES_FILE = os.path.join(DATA_DIR, "All_matches.json")
CLUB_IDS_FILE = os.path.join(DATA_DIR, "EPLClubIDs.json")
BETS_FILE = os.path.join(DATA_DIR, "bets.csv")
DB_FILE = os.path.join(DATA_DIR, "project.db") #sql db file path.

#API keys
MATCHES_KEY_FILE = os.path.join(APIKEYS_DIR, "matches_key.txt")
X_TOKEN_FILE = os.path.join(APIKEYS_DIR, "X_bearertoken.txt")

#URLs
FOOTBALL_DATA_URL = "https://api.football-data.org/v4/competitions/PL/matches"
def get_betting_odd_csv_url(season: int):
    season_code = f"{str(season)[-2:]}{str(season+1)[-2:]}"
    return f"https://www.football-data.co.uk/mmz4281/{season_code}/E0.csv"
    # e.g., if the season is 2025/26, the csv file would be stored in https://www.[...]/mmz4281/2526/E0.csv"

#The 3 data sources use different names for each club so this is a unification dictionary for name translation
TEAM_MAPPING = {
    "Arsenal": {"bet_name": "Arsenal", "matches_shortname": "Arsenal", "x_handle": "Arsenal"},
    "Manchester City": {"bet_name": "Man City", "matches_shortname": "Man City", "x_handle": "ManCity"},
    "Manchester United": {"bet_name": "Man United", "matches_shortname": "Man United", "x_handle": "ManUtd"},
    "Aston Villa": {"bet_name": "Aston Villa", "matches_shortname": "Aston Villa", "x_handle": "AVFCOfficial"},
    "Liverpool": {"bet_name": "Liverpool", "matches_shortname": "Liverpool", "x_handle": "LFC"},
    "Chelsea": {"bet_name": "Chelsea", "matches_shortname": "Chelsea", "x_handle": "ChelseaFC"},
    "Brentford": {"bet_name": "Brentford", "matches_shortname": "Brentford", "x_handle": "BrentfordFC"},
    "Everton": {"bet_name": "Everton", "matches_shortname": "Everton", "x_handle": "Everton"},
    "Fulham": {"bet_name": "Fulham", "matches_shortname": "Fulham", "x_handle": "FulhamFC"},
    "Brighton": {"bet_name": "Brighton", "matches_shortname": "Brighton Hove", "x_handle": "OfficialBHAFC"},
    "Sunderland": {"bet_name": "Sunderland", "matches_shortname": "Sunderland", "x_handle": "SunderlandAFC"},
    "Newcastle": {"bet_name": "Newcastle", "matches_shortname": "Newcastle", "x_handle": "NUFC"},
    "Bournemouth": {"bet_name": "Bournemouth", "matches_shortname": "Bournemouth", "x_handle": "afcbournemouth"},
    "Crystal Palace": {"bet_name": "Crystal Palace", "matches_shortname": "Crystal Palace", "x_handle": "CPFC"},
    "Leeds United": {"bet_name": "Leeds", "matches_shortname": "Leeds United", "x_handle": "LUFC"},
    "Nottingham Forest": {"bet_name": "Nott'm Forest", "matches_shortname": "Nottingham", "x_handle": "NFFC"},
    "Tottenham": {"bet_name": "Tottenham", "matches_shortname": "Tottenham", "x_handle": "SpursOfficial"},
    "West Ham United": {"bet_name": "West Ham", "matches_shortname": "West Ham", "x_handle": "WestHam"},
    "Burnley": {"bet_name": "Burnley", "matches_shortname": "Burnley", "x_handle": "BurnleyOfficial"},
    "Wolverhampton": {"bet_name": "Wolves", "matches_shortname": "Wolverhampton", "x_handle": "Wolves"},
}