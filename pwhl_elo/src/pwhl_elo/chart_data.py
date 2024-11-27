import json
import os

import pandas as pd

from pwhl_elo.utils import drop_nans, structure_chartable_df


def create_chart_data(input: str, output_dir: str) -> str:
    """
    Creates a json data file of every date and elo that can be used to create a chart of Elos.
    """

    wphl_elos_df = pd.read_csv(
        input, header=0, parse_dates=["date"]  # input here should be that latest file
    )

    chartable_df = structure_chartable_df(wphl_elos_df)
    output_path = os.path.join(output_dir, "chartable", "chartable_wphl_elos.json")
    # save elos in easier to visualize format
    # chartable_df.to_json(
    #     output_path,
    #     orient="columns",
    #     date_format="iso",
    #     index=True
    # )
    chartable_df.index = chartable_df.index.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    chartable_dict = chartable_df.to_dict(orient="dict", index=True)

    with open(output_path, "w") as f:
        json.dump(drop_nans(chartable_dict), f)
    return output_path
