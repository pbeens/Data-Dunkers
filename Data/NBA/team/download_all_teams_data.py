import time
from pathlib import Path
import csv
from io import StringIO

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ----------------------
# Configuration
# ----------------------
season_year = 2026        # Example: for 2025–26 season
season_type = 2           # 2 = Regular Season on ESPN

espn_team_slugs = [
    "atl", "bos", "bkn", "cha", "chi", "cle", "dal", "den", "det", "gs",
    "hou", "ind", "lac", "lal", "mem", "mia", "mil", "min", "no", "ny",
    "okc", "orl", "phi", "phx", "por", "sac", "sa", "tor", "utah", "wsh"
]

# Folder where this script lives (so CSVs and log go beside the .py file)
SCRIPT_DIR = Path(__file__).resolve().parent
LOG_PATH = SCRIPT_DIR / "scrape_log.csv"


# ----------------------
# Logging helpers
# ----------------------
def init_log(log_path: Path) -> None:
    """Create log file with header if it does not exist."""
    if not log_path.exists():
        with log_path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "team_slug", "season_year", "season_type",
                "url", "status", "rows", "message"
            ])


def log_result(team_slug: str, year: int, season_type: int,
               url: str, status: str, rows: int = 0, message: str = "") -> None:
    """Append a single log row."""
    with LOG_PATH.open("a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([team_slug, year, season_type, url, status, rows, message])


# ----------------------
# Scrape + merge logic
# ----------------------
def scrape_and_merge_team_stats(team_slug: str, driver,
                                year: int, season_type: int,
                                out_dir: Path) -> None:
    url = f"https://www.espn.com/nba/team/stats/_/name/{team_slug}/season/{year}/seasontype/{season_type}"

    try:
        driver.get(url)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table"))
        )

        time.sleep(2)

        # Future-proof version
        tables = pd.read_html(StringIO(driver.page_source))

        if not tables:
            log_result(team_slug, year, season_type, url, "no_tables", 0, "No tables found")
            return

        name_tables = [t for t in tables if list(t.columns) == ["Name"]]
        stat_tables = [t for t in tables if list(t.columns) != ["Name"]]

        if not name_tables:
            log_result(team_slug, year, season_type, url, "no_name_table", 0, "No Name table")
            return

        names_df = name_tables[0].copy()

        if not stat_tables:
            log_result(team_slug, year, season_type, url, "no_stat_tables", 0, "No stats tables")
            return

        min_len = min([len(names_df)] + [len(t) for t in stat_tables])
        names_df = names_df.iloc[:min_len].reset_index(drop=True)
        trimmed_stats = [t.iloc[:min_len].reset_index(drop=True) for t in stat_tables]

        stats_merged = pd.concat(trimmed_stats, axis=1)
        full_df = pd.concat([names_df, stats_merged], axis=1)
        full_df = full_df.loc[:, ~full_df.columns.duplicated()]

        # Correct season label
        season_label = f"{year-1}-{year}"

        filename = f"{team_slug.upper()}_{season_label}_players.csv"
        out_path = out_dir / filename
        full_df.to_csv(out_path, index=False)

        log_result(team_slug, year, season_type, url, "success", len(full_df), f"Saved to {filename}")

    except Exception as e:
        log_result(team_slug, year, season_type, url, "error", 0, str(e))


# ----------------------
# Main run
# ----------------------
def main():
    init_log(LOG_PATH)

    options = Options()
    options.headless = True
    wd = webdriver.Firefox(options=options)

    try:
        for team in espn_team_slugs:
            scrape_and_merge_team_stats(team, wd, season_year, season_type, SCRIPT_DIR)
            # Be polite to ESPN's servers
            time.sleep(1)
    finally:
        wd.quit()


if __name__ == "__main__":
    main()
