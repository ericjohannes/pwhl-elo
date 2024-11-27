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
    # save elos in easier to visualize format
    chartable_df.to_json(
        output_path,
        orient="records",
        date_format="iso",
    )
    return output_path
