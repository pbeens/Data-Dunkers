import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Optional: Run in headless mode
options = Options()
options.headless = True
wd = webdriver.Firefox(options=options)

# Test year and season type
season_year = 2026  # Example: for 2025–26 season
season_type = 2     # Regular Season

# List of all ESPN NBA team slugs
espn_team_slugs = [
    "atl", "bos", "bkn", "cha", "chi", "cle", "dal", "den", "det", "gs",
    "hou", "ind", "lac", "lal", "mem", "mia", "mil", "min", "no", "ny",
    "okc", "orl", "phi", "phx", "por", "sac", "sa", "tor", "utah", "wsh"
]

valid_teams = []

for team in espn_team_slugs:
    url = f"https://www.espn.com/nba/team/stats/_/name/{team}/season/{season_year}/seasontype/{season_type}"
    try:
        wd.get(url)
        WebDriverWait(wd, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table"))
        )
        print(f"✅ Found stats for: {team.upper()} ({url})")
        valid_teams.append(team)
    except (NoSuchElementException, TimeoutException):
        print(f"❌ No stats found for: {team.upper()} ({url})")
    time.sleep(1)  # be nice to the server

wd.quit()

# Optional: save to CSV
pd.DataFrame(valid_teams, columns=["valid_team_slugs"]).to_csv("valid_nba_teams.csv", index=False)
