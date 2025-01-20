import json
import os

import pandas as pd

key_cols_map = {
    "game_status": "time",
    "home_team_city": "home_team",
    "visiting_team_city": "away_team",
    "home_goal_count": "home_score",
    "visiting_goal_count": "away_score",
    "venue_name": "venue",
    "date_played": "date",
}
drop_cols = ["home_team", "date"]
use_cols = [
    "date",
    "time",
    "away_team",
    "away_score",
    "home_team",
    "home_score",
    "venue",
    "season",
    "type",
]


def clean_season(file_data, seasonid, pwhl):
    """
    Takes json of one seaso and returns clean df of season.
    """
    schedule_df = pd.DataFrame(file_data)
    # drop columns that have conflicting names
    schedule_df = schedule_df.drop(drop_cols, axis=1)
    # rename cols with key cols map
    schedule_df = schedule_df.rename(columns=key_cols_map)
    # add season and type cols based on season_id
    schedule_df["type"] = pwhl.seasons[seasonid]["type"]
    schedule_df["season"] = pwhl.seasons[seasonid]["year"]
    return schedule_df


def season_id_from_filename(filename: str) -> str:
    """
    Extracts the season id from a filename of a season's data.
    """
    season_id = filename.split("_")[1]
    season_id = season_id.split(".")[0]
    return season_id


def handle(pwhl) -> str:
    """
    Combine all seasons from seasons data folder into one clean csv.
    """
    output_path = os.path.join(pwhl.clean_output_path, "pwhl_all_results.csv")
    all_seasons_df = pd.DataFrame()
    for filename in os.listdir(pwhl.output_path):
        inputpath = os.path.join(pwhl.output_path, filename)
        seasonid = season_id_from_filename(filename)
        with open(inputpath, "r") as f:
            file_data = json.load(f)
        season_df = clean_season(file_data, seasonid, pwhl)
        all_seasons_df = pd.concat([all_seasons_df, season_df])

    all_seasons_df[use_cols].to_csv(output_path, index=False, date_format="%Y/%m/%d")
    return output_path
