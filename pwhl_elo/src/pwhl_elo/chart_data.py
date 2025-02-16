import json
import math
import os

import pandas as pd

from pwhl_elo.utils import CHART_DATA_FN, RESULTS_ELOS_FN, structure_chartable_df


def handle(pwhl) -> str:
    """
    Creates a json data file of every date and elo that can be used to create a chart of Elos.
    """

    wphl_elos_df = pd.read_csv(
        os.path.join(pwhl.elos_output_path, RESULTS_ELOS_FN),
        header=0,
        parse_dates=["date"],  # input here should be that latest file
    )
    output_path = os.path.join(pwhl.chart_data_output_path, CHART_DATA_FN)

    # get max dates and elos from games played
    games_played = wphl_elos_df[wphl_elos_df["time"].str.lower().str.contains("final")]
    max_date = max(games_played.date).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    min_date = min(games_played.date).strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    min_elo = int(min(pd.concat([games_played.elo_after_home, games_played.elo_after_away])))
    max_elo = int(max(pd.concat([games_played.elo_after_home, games_played.elo_after_away])))

    export_data = {
        "data": [],
        "min_date": min_date,
        "max_date": max_date,
        "min_elo": min_elo,
        "max_elo": max_elo,
    }
    for season in wphl_elos_df.season.unique():
        season_data = wphl_elos_df[wphl_elos_df["season"] == season]
        chartable_df = structure_chartable_df(season_data)
        chartable_df.index = chartable_df.index.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        chartable_dict = chartable_df.to_dict(orient="dict", index=True)

        # structure data in easier to visualize format
        for team in chartable_dict:
            team_data = {"team": team, "games": [], "season": str(season)}
            for k, v in chartable_dict[team].items():
                if not math.isnan(v):
                    team_data["games"].append({"date": k, "elo": int(v)})
            export_data["data"].append(team_data)

    with open(output_path, "w") as f:
        json.dump(export_data, f)
    return output_path
