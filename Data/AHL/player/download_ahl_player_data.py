import os
from pathlib import Path
from io import StringIO

import pandas as pd
import requests

SEASON_LABEL = "2025-2026"  # Default focus season for league snapshot
LEAGUE_URL = "https://www.quanthockey.com/ahl/en/seasons/2025-26-ahl-players-stats.html"
MOOSE_URL = "https://www.quanthockey.com/ahl/en/teams/manitoba-moose-players-2025-26-ahl-stats.html"
OUTPUT_DIR = Path(__file__).resolve().parent
ARCHIVE_DIR = OUTPUT_DIR / "season_cache"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
START_YEAR = int(os.getenv("AHL_START_YEAR", "2000"))
END_YEAR = int(os.getenv("AHL_END_YEAR", "2026"))


def fetch_table(url: str, timeout: int = 12) -> pd.DataFrame:
    """Download the HTML page and return the first table."""
    resp = requests.get(url, headers={"User-Agent": UA}, timeout=timeout)
    resp.raise_for_status()
    html = resp.text
    return pd.read_html(StringIO(html))[0]


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)

    league_df = fetch_table(LEAGUE_URL)
    league_path = OUTPUT_DIR / f"ahl_player_stats_{SEASON_LABEL}.csv"
    league_df.to_csv(league_path, index=False)

    moose_df = fetch_table(MOOSE_URL)
    moose_path = OUTPUT_DIR / f"MB_Moose_player_stats_{SEASON_LABEL}.csv"
    moose_df.to_csv(moose_path, index=False)

    # Also include a filtered view from the league table (team code 'MTB')
    filtered = league_df[league_df["Team"].isin(["MTB", "MB", "MOO", "MAN", "MBM"])]
    if not filtered.empty:
        filtered_path = OUTPUT_DIR / f"MB_Moose_player_stats_from_league_{SEASON_LABEL}.csv"
        filtered.to_csv(filtered_path, index=False)
        print(f"Saved Moose players (filtered league) to {filtered_path}")

    # Build all-seasons Moose player stats from team pages, cached per season
    moose_rows = []
    consecutive_misses = 0
    for start in range(START_YEAR, END_YEAR + 1):
        end = str((start + 1) % 100).zfill(2)
        season_label = f"{start}-{end}"
        url = f"https://www.quanthockey.com/ahl/en/teams/manitoba-moose-players-{season_label}-ahl-stats.html"
        cache_file = ARCHIVE_DIR / f"MB_Moose_player_stats_{season_label}.csv"

        df = None
        if cache_file.exists():
            df = pd.read_csv(cache_file)
            consecutive_misses = 0
        else:
            try:
                df = fetch_table(url, timeout=8)
                df.insert(0, "Season", season_label)
                df.to_csv(cache_file, index=False)
                consecutive_misses = 0
            except Exception:
                consecutive_misses += 1

        if df is not None:
            moose_rows.append(df)

        if consecutive_misses >= 6:
            break

    if moose_rows:
        moose_all = pd.concat(moose_rows, ignore_index=True)
        moose_all_path = OUTPUT_DIR / "MB_Moose_player_stats_all_seasons.csv"
        moose_all.to_csv(moose_all_path, index=False)
        print(f"Saved Moose players (all seasons) to {moose_all_path}")

    print(f"Saved league players to {league_path}")
    print(f"Saved Moose players (team page) to {moose_path}")


if __name__ == "__main__":
    main()
