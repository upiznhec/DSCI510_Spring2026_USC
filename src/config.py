import os

#Project Layout
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
APIKEYS_DIR = os.path.join(BASE_DIR, "APIkeys")
DOC_DIR = os.path.join(BASE_DIR, "doc")

#Data files
MATCHES_FILE = os.path.join(DATA_DIR, "All_matches.json")
CLUB_IDS_FILE = os.path.join(DATA_DIR, "EPLClubIDs.json")
CLUB_NAMES_FILE = os.path.join(SRC_DIR, "EPLClubsXNameList.txt")
BETS_FILE = os.path.join(DATA_DIR, "bets.csv")
#This file is stored in src due to the code's unability to run
# if it's stored in the .gitignore directory "/data"

#API keys
MATCHES_KEY_FILE = os.path.join(APIKEYS_DIR, "matches_key.txt")
X_TOKEN_FILE = os.path.join(APIKEYS_DIR, "X_bearertoken.txt")