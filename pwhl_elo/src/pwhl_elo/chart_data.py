import json
import math
import os

import pandas as pd

from pwhl_elo.utils import structure_chartable_df


def create_chart_data(input: str, output_dir: str) -> str:
    """
    Creates a json data file of every date and elo that can be used to create a chart of Elos.
    """

    wphl_elos_df = pd.read_csv(
        input, header=0, parse_dates=["date"]  # input here should be that latest file
    )

    chartable_df = structure_chartable_df(wphl_elos_df)
    output_path = os.path.join(output_dir, "chartable", "chartable_wphl_elos.json")
    max_date = max(chartable_df.index).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    min_date = min(chartable_df.index).strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    max_elo = int(max([chartable_df[c].max() for c in chartable_df.columns]))
    min_elo = int(min([chartable_df[c].min() for c in chartable_df.columns]))

    chartable_df.index = chartable_df.index.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    chartable_dict = chartable_df.to_dict(orient="dict", index=True)

    export_data = {
        "data": [],
        "min_date": min_date,
        "max_date": max_date,
        "min_elo": min_elo,
        "max_elo": max_elo,
    }

    # structure data in easier to visualize format
    for team in chartable_dict:
        team_data = {"team": team, "games": []}
        for k, v in chartable_dict[team].items():
            if not math.isnan(v):
                team_data["games"].append({"date": k, "elo": int(v)})
        export_data["data"].append(team_data)

    with open(output_path, "w") as f:
        json.dump(export_data, f)
    return output_path
