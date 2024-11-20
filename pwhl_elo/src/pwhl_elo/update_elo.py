import json

import pandas as pd

from pwhl_elo.utils import time_stamp


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
    merged_df = pd.merge(
        left=results_df,
        right=wphl_elos_df,
        how="outer",
    )
    # join fixtures on date and two teams
    print(merged_df, latest_elos, TIMESTAMP)
