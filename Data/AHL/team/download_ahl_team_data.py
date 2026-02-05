import os
from pathlib import Path
from io import StringIO

import pandas as pd
import requests

SEASON_LABEL = "2025-2026"  # Default focus season for league snapshot
TEAM_URL = "https://www.quanthockey.com/ahl/en/seasons/2025-26/"
OUTPUT_DIR = Path(__file__).resolve().parent
ARCHIVE_DIR = OUTPUT_DIR / "season_cache"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
MOOSE_NAME = "Manitoba Moose"
START_YEAR = int(os.getenv("AHL_START_YEAR", "2000"))
END_YEAR = int(os.getenv("AHL_END_YEAR", "2026"))


def fetch_table(url: str, timeout: int = 12) -> pd.DataFrame:
    """Download the HTML page and return the first table."""
    resp = requests.get(url, headers={"User-Agent": UA}, timeout=timeout)
    resp.raise_for_status()
    html = resp.text
    return pd.read_html(StringIO(html))[0]


def flatten_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Flatten multi-level columns into single strings."""
    df = df.copy()
    df.columns = [
        "_".join([str(part) for part in col if str(part) != "nan"]).strip("_")
        if isinstance(col, tuple)
        else str(col)
        for col in df.columns
    ]
    return df


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)

    team_df = fetch_table(TEAM_URL)
    team_df = flatten_columns(team_df)
    # Normalize rank/team column names for easier filtering
    col0, col1 = team_df.columns[:2]
    team_df = team_df.rename(columns={col0: "Rk", col1: "Team"})

    league_path = OUTPUT_DIR / f"ahl_team_stats_{SEASON_LABEL}.csv"
    team_df.to_csv(league_path, index=False)

    # Build an all-seasons Moose file by walking known season URLs, with per-season caching
    moose_rows = []
    consecutive_misses = 0
    for start in range(START_YEAR, END_YEAR + 1):
        end = str((start + 1) % 100).zfill(2)
        season_label = f"{start}-{end}"
        url = f"https://www.quanthockey.com/ahl/en/seasons/{season_label}/"
        cache_file = ARCHIVE_DIR / f"MB_Moose_team_{season_label}.csv"

        df_season = None
        if cache_file.exists():
            df_season = pd.read_csv(cache_file)
            consecutive_misses = 0
        else:
            try:
                df_raw = fetch_table(url, timeout=8)
                df_raw = flatten_columns(df_raw)
                c0, c1 = df_raw.columns[:2]
                df_raw = df_raw.rename(columns={c0: "Rk", c1: "Team"})
                moose = df_raw[df_raw["Team"] == MOOSE_NAME].copy()
                if not moose.empty:
                    moose.insert(1, "Season", season_label)
                    moose.to_csv(cache_file, index=False)
                    df_season = moose
                    consecutive_misses = 0
                else:
                    consecutive_misses += 1
            except Exception:
                consecutive_misses += 1

        if df_season is not None:
            moose_rows.append(df_season)

        # If we miss a bunch in a row, assume we've gone past available seasons
        if consecutive_misses >= 6:
            break

    if moose_rows:
        moose_all = pd.concat(moose_rows, ignore_index=True)
        moose_all_path = OUTPUT_DIR / "MB_Moose_team_all_seasons.csv"
        moose_all.to_csv(moose_all_path, index=False)
        print(f"Saved Manitoba Moose all seasons to {moose_all_path}")

    print(f"Saved league teams to {league_path}")


if __name__ == "__main__":
    main()
