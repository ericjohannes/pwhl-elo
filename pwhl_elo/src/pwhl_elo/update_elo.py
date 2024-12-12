import datetime
import json
import os

import pandas as pd

from pwhl_elo.utils import calculate_elo, clean_name, expected_result, time_stamp


def handle_row(row, current_elo):
    """
    Get current Elos for teams. Calculate Elo changes from one fixture. Save those results and save
    new current Elo.
    """

    # skip games that don't have scores yet
    if "final" not in row["time_r"].lower():
        return row

    home = row["home_team"]
    away = row["away_team"]

    # in case these are new teams
    if home not in current_elo["teams"]:
        current_elo[home] = 1300

    if away not in current_elo["teams"]:
        current_elo[away] = 1300

    start_elo_home = current_elo["teams"][home]
    start_elo_away = current_elo["teams"][away]

    # how many times out of 100 would each team win
    expected_win_home, expected_win_away = expected_result(start_elo_home, start_elo_away)

    elo_new_home, elo_new_away = calculate_elo(
        start_elo_home,
        start_elo_away,
        expected_win_home,
        expected_win_away,
        row["home_score_r"],
        row["away_score_r"],
    )

    current_elo["teams"][home] = elo_new_home
    current_elo["teams"][away] = elo_new_away

    row["elo_after_home"] = elo_new_home
    row["elo_after_away"] = elo_new_away

    row["elo_before_home"] = start_elo_home
    row["elo_before_away"] = start_elo_away

    row["expected_win_home"] = expected_win_home
    row["expected_win_away"] = expected_win_away

    return row


def update_elo(input: str, output_dir: str):
    """
    this process will find games taht have been played but not evaluated yet, ie have a final score
    but do not yet have resulting Elo scores assigned for them and assign Elo scores for them. It
    will also update the latest Elos file

    steps:
    1. load latest wphl_elos....csv file
    2. load wphl_result_clean file
    2.5 load latest elos file
    3. match fixtures on date and two teams, find fixtures for which the time contains "final" in
    result file but time does not contain final in the wphel_elos file. Filter those out
    4. go through them and apply elo calculations, using latest elos and updating latest elos.
    5. output new wphel_elos file and latest_elos file
    """
    TIMESTAMP = time_stamp()
    # load three files, only use input for one becuase other two are always the same
    with open("./data/output/pwhl_latest_elos.json", "r") as f:
        latest_elos = json.load(f)

    results_df = pd.read_csv(
        "./data/input/wphl_results_clean_data.csv", header=0, parse_dates=["date"]
    )

    wphl_elos_df = pd.read_csv(
        input, header=0, parse_dates=["date"]  # input here should be that latest file
    )

    results_df["home_team"] = results_df["home_team"].apply(clean_name)
    results_df["away_team"] = results_df["away_team"].apply(clean_name)

    # join fixtures on date and two teams
    merged_df = pd.merge(
        left=results_df,
        right=wphl_elos_df,
        how="outer",
        on=["date", "away_team", "home_team"],
        suffixes=["_r", "_i"],  # results and input
    )

    # find fixtures for which the time contains "final" in result file but time does not contain
    # final in the wphel_elos file.
    merged_df["time_r"] = merged_df["time_r"].str.lower()
    merged_df["time_i"] = merged_df["time_i"].str.lower()
    new_scores_df = merged_df[
        merged_df.time_r.str.contains("final") & (~merged_df.time_i.str.contains("final"))
    ]

    # sort by data just to be sure
    new_scores_df = new_scores_df.sort_values("date")
    # calculate Elo for each new fixture

    new_scores_df = new_scores_df.apply(handle_row, args=(latest_elos,), axis=1)

    # match on home_team, away_team and date and update scores and elos
    for row in new_scores_df.to_dict(orient="records"):
        wphl_elos_df.loc[
            (wphl_elos_df["home_team"] == row["home_team"])
            & (wphl_elos_df["away_team"] == row["away_team"])
            & (wphl_elos_df["date"] == row["date"]),
            [
                "elo_after_home",
                "elo_after_away",
                "elo_before_home",
                "elo_before_away",
                "expected_win_home",
                "expected_win_away",
                "away_score",
                "home_score",
                "time",
            ],
        ] = [
            row["elo_after_home"],
            row["elo_after_away"],
            row["elo_before_home"],
            row["elo_before_away"],
            row["expected_win_home"],
            row["expected_win_away"],
            row["away_score_r"],
            row["home_score_r"],
            row["time_r"],
        ]

    all_results_ts = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    wphl_elos_df.to_csv(
        os.path.join(output_dir, "all_results", f"wphl_elos_{all_results_ts}.csv"), index=False
    )

    # save latest elos
    latest_elos = {
        "date": TIMESTAMP,
        "teams": latest_elos["teams"],
    }
    with open(os.path.join(output_dir, "pwhl_latest_elos.json"), "w") as f:
        json.dump(latest_elos, f)
