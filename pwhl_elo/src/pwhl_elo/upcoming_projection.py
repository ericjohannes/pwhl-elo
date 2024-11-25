import json
import os
import re
from datetime import datetime

import numpy as np
import pandas as pd

from pwhl_elo.utils import expected_result


def revert_elo_to_mean(season_ending_elo: int) -> int:
    """
    To account for revversion to mean, new players, coach etc. Bring an Elo 1/3 back to 1300
    """

    difference = season_ending_elo - 1300
    new_elo = season_ending_elo - (difference / 3)
    return int(np.round(new_elo))


def check_if_team_played(team: str, current_season: int, result_df: pd.DataFrame) -> bool:
    """
    Checks if a team has played a game this season.
    """
    played_games = result_df[
        (result_df["time"].str.contains("Final"))  # game has been played
        & ((result_df["home_team"] == team) | (result_df["away_team"] == team))  # by this team
        & (result_df["season"] == current_season)  # this season
    ]
    return len(played_games) > 0


def handle_row_wrapper(current_elo: dict):
    # check if each team has played a game yet this season. If not adjust Elo
    # 1/3rd back to 1300.

    """
    wrapper to inject latest elos into handle row function
    """

    def handle_row(row):
        """
        Calculate expected result for each row in a pandas dataframe and add to row
        """
        home = row["home_team"]
        away = row["away_team"]

        start_elo_home = current_elo[home]
        start_elo_away = current_elo[away]

        expected_win_home, expected_win_away = expected_result(start_elo_home, start_elo_away)
        row["expected_win_home"] = expected_win_home
        row["expected_win_away"] = expected_win_away
        row["elo_before_home"] = start_elo_home
        row["elo_before_away"] = start_elo_away
        return row

    return handle_row


def get_newest_file(input_dir: str):
    """
    Finds the newest file from a directory based on timestamp
    """
    pattern = r"(\d{4}-\d{2}-\d{2}_\d{2}:\d{2}:\d{2})"
    results_dir = os.path.join(input_dir, "all_results")
    files = os.listdir(results_dir)
    date_times = []
    for f in files:
        match = re.search(pattern, f)
        if match:
            date_times.append(
                # probably could just sort it as a string
                datetime.strptime(match.group(1), "%Y-%m-%d_%H:%M:%S")
            )

    date_times.sort(reverse=True)
    file_timestamp = date_times[0].strftime("%Y-%m-%d_%H:%M:%S")
    source_file = f"wphl_elos_{file_timestamp}.csv"
    return os.path.join(results_dir, source_file)


def build_upcoming_projects():
    TIMESTAMP = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    OUTPUT_DIR = os.path.join("..", "data", "output")
    INPUT_DIR = os.path.join("..", "data", "output")
    OUTPUT_FN = os.path.join(
        OUTPUT_DIR, "next_five_projections", f"game_projections_{TIMESTAMP}.json"
    )

    # get latest elos
    with open(os.path.join(INPUT_DIR, "pwhl_latest_elos.json"), "r") as f:
        latet_elos = json.load(f)

    # get first 5 unplayed games
    source_path = get_newest_file(INPUT_DIR)
    source_df = pd.read_csv(source_path)

    unplayed_df = source_df[~source_df["time"].str.contains("Final")]
    next_5_df = unplayed_df.sort_values("date").head(5)

    # calculate odds on those 5 based on latest elos
    handle_row_with_elos = handle_row_wrapper(latet_elos["teams"])
    next_5_df = next_5_df.apply(handle_row_with_elos, axis=1)
    next_5_df["date"] = pd.to_datetime(next_5_df["date"]).dt.strftime("%b. %d, %Y")
    # save results
    next_5_df[
        [
            "date",
            "away_team",
            "home_team",
            "venue",
            "type",
            "elo_before_home",
            "elo_before_away",
            "expected_win_home",
            "expected_win_away",
        ]
    ].to_json(OUTPUT_FN, orient="records")


if __name__ == "__main__":
    TIMESTAMP = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    OUTPUT_DIR = os.path.join("data", "output")
    INPUT_DIR = os.path.join("data", "output")
    OUTPUT_FN = os.path.join(
        "data", "output", "next_five_projections", f"game_projections_{TIMESTAMP}.json"
    )

    # get latest elos
    with open(os.path.join(INPUT_DIR, "pwhl_final_elos.json"), "r") as f:
        latet_elos = json.load(f)

    # get first 5 unplayed games
    source_path = get_newest_file(INPUT_DIR)
    source_df = pd.read_csv(source_path)

    # between seasons revert Elos to the means
    for team in latet_elos.keys():
        if not check_if_team_played(team, 2025, source_df):
            latet_elos[team] = revert_elo_to_mean(latet_elos[team])

    unplayed_df = source_df[~source_df["time"].str.contains("Final")]
    next_5_df = unplayed_df.sort_values("date").head(5)

    # calculate odds on those 5 based on latest elos
    handle_row_with_elos = handle_row_wrapper(latet_elos)
    next_5_df = next_5_df.apply(handle_row_with_elos, axis=1)

    # save results
    next_5_df[
        [
            "date",
            "away_team",
            "home_team",
            "venue",
            "type",
            "elo_before_home",
            "elo_before_away",
            "expected_win_home",
            "expected_win_away",
        ]
    ].to_json(OUTPUT_FN, orient="records", date_format="iso")
