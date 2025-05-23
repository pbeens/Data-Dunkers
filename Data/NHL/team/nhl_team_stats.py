import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set the target season
end_year = 2025
start_year = end_year - 1

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct URL and filename
url = f"https://www.espn.com/nhl/stats/team/_/season/{end_year}/seasontype/2"
filename = os.path.join(script_dir, f'nhl_team_stats_{start_year}-{end_year}.csv')

print(f"🔄 Scraping season {start_year}-{end_year}...")

# Set up Selenium options to mimic a real user
options = Options()
options.set_preference(
    "general.useragent.override",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
)

# Initialize WebDriver
wd = webdriver.Firefox(options=options)
wd.get(url)

try:
    # Wait for elements to load
    WebDriverWait(wd, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//a[contains(@href, '/nhl/team/_/name/')]"))
    )

    # Extract team names
    team_elements = wd.find_elements(By.XPATH, "//a[contains(@href, '/nhl/team/_/name/')]")
    team_names = [element.text for element in team_elements if element.text]

    if not team_names:
        print(f"⚠ Warning: No team names found for {start_year}-{end_year}. Exiting...")
        wd.quit()
        exit()

    print(f"✅ Extracted {len(team_names)} teams for {start_year}-{end_year}.")

    # Read tables from the page
    tables = pd.read_html(url)

    if len(tables) < 2:
        print(f"⚠ Error: Expected tables not found for {start_year}-{end_year}. Exiting...")
        wd.quit()
        exit()

    # Process table data
    rank_team = tables[0]
    stats = tables[1]

    # Remove the 'RK' and 'Team' columns from rank_team
    rank_team = rank_team.drop(columns=['RK', 'Team'], errors='ignore')  # Ignore missing columns

    # Ensure team names list matches row count
    if len(rank_team) != len(team_names):
        print(f"⚠ Mismatch: Expected {len(rank_team)} teams, but got {len(team_names)}.")
        wd.quit()
        exit()

    # Add team names
    rank_team['Team'] = team_names

    # Merge data
    df = pd.concat([rank_team, stats], axis=1)

    # Save to CSV in the same directory as the script
    df.to_csv(filename, index=False)
    print(f"✅ Data successfully saved to {filename}")

except Exception as e:
    print(f"❌ Error processing season {start_year}-{end_year}: {e}")

finally:
    wd.quit()  # Close WebDriver

print("🎉 Scraping complete!")
