import math

import pandas as pd
import requests

# url = "https://lscluster.hockeytech.com/feed/?feed=modulekit&view=schedule&season=5&location=homeaway&key=446521baf8c38984&client_code=pwhl&site_id=0&league_id=1&lang=en&fmt=json" # noqa: E501

# notes:
# month=-1 setting month to 1 gets games from january, to 4 gets april. Can't figure out how to
# change year
# examples:
# "https://lscluster.hockeytech.com/feed/index.php?feed=statviewfeed&view=schedule&team=-1&season=5&month=-1&location=homeaway&key=446521baf8c38984&client_code=pwhl&site_id=0&league_id=1&conference_id=-1&division_id=-1&lang=en&callback=angular.callbacks._5" # noqa: E501

# "https://lscluster.hockeytech.com/feed/?feed=modulekit&view=player&key=2976319eb44abe94&fmt=json&client_code=ohl&lang=en&player_id=5328&category=seasonstats # noqa: E501


# example game
# {
#     "id": "105"
#     "game_id": "105"
#     "season_id": "5"
#     "quick_score": "0"
#     "date_played": "2024-11-30"
#     "date": "Nov. 30"
#     "date_with_day": "Sat, Nov 30"
#     "date_time_played": "2024-11-30T14:00:00Z"
#     "GameDateISO8601": "2024-11-30T14:00:00-05:00"
#     "home_team": "6"
#     "visiting_team": "1"
#     "home_goal_count": "3"
#     "visiting_goal_count": "1"
#     "period": "3"
#     "overtime": "0"
#     "schedule_time": "14:00:00"
#     "schedule_notes": ""
#     "game_clock": "00:00:00"
#     "timezone": "Canada/Eastern"
#     "game_number": "1"
#     "shootout": "0"
#     "attendance": "8089"
#     "status": "4"
#     "location": "17"
#     "game_status": "Final"
#     "intermission": "0"
#     "game_type": ""
#     "game_letter": ""
#     "if_necessary": "0"
#     "period_trans": "3"
#     "started": "1"
#     "final": "1"
#     "tickets_url": "https://www.ticketmaster.ca/event/10006158073B440D"
#     "home_audio_url": ""
#     "visiting_audio_url": ""
#     "home_team_name": "Toronto Sceptres"
#     "home_team_code": "TOR"
#     "home_team_nickname": "Sceptres"
#     "home_team_city": "Toronto"
#     "home_team_division_long": "PWHL"
#     "home_team_division_short": "PWHL"
#     "visiting_team_name": "Boston Fleet"
#     "visiting_team_code": "BOS"
#     "visiting_team_nickname": "Fleet"
#     "visiting_team_city": "Boston"
#     "visiting_team_division_long": "PWHL"
#     "visiting_team_division_short": "PWHL"
#     "notes_text": ""
#     "use_shootouts": "1"
#     "venue_name": "Coca-Cola Coliseum"
#     "venue_url": "https://www.coca-colacoliseum.com/"
#     "venue_location": "Toronto, ON"
#     "last_modified": "2024-11-30 22:06:04"
#     "flo_core_event_id": ""
#     "flo_live_event_id": ""
#     "htv_game_id": ""
#     "client_code": "pwhl"
#     "scheduled_time": "2:00 pm EST"
# }


def season_type_from_id(season_id: str) -> str:
    # determines the season type from the id
    season_types = {0: "playoffs", 1: "preseason", 2: "regular_season"}
    type_num = int(season_id) % 3
    return season_types[type_num]


def season_year_from_id(season_id: str) -> int:
    # determines year of season from the id
    # season 1 is 2024 so 0 was 2023
    return math.ceil(int(season_id) / 3) + 2023


url = "https://lscluster.hockeytech.com/feed/"
key_cols_map = {
    "game_status": "time",
    "home_team_city": "home_team",
    "visiting_team_city": "away_team",
    "home_goal_count": "home_score",
    "visiting_goal_count": "away_score",
    "venue_name": "venue",
    # "date_played": "date",
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
params = {
    "feed": "modulekit",
    "view": "schedule",
    "location": "homeaway",
    "key": "446521baf8c38984",
    "client_code": "pwhl",
    "site_id": "0",
    "league_id": "1",
    "lang": "en",
    "fmt": "json",
}


def get_games(season_id: int, output_path: str) -> str:
    # setting "season_id" parameter changes what season it gets games for.
    # 5 = 2024-2025 regular eason
    # 4 = 2024-2025 preseason.
    # guessing 6 will be 24-5 post season etc
    if season_id:
        params["season_id"] = season_id

    r = requests.get(url, params=params)
    data = r.json()
    schedule_df = pd.DataFrame(data["SiteKit"]["Schedule"])
    # drop columns that have conflicting names
    schedule_df = schedule_df.drop(drop_cols, axis=1)
    # rename cols with key cols map
    schedule_df = schedule_df.rename(columns=key_cols_map)
    # add season and type cols based on season_id
    schedule_df["type"] = season_type_from_id(season_id)
    schedule_df["season"] = season_year_from_id(season_id)
    # create date time column
    schedule_df["date"] = pd.to_datetime(schedule_df.GameDateISO8601, utc=True)
    # save csv of data with only use_cols included
    schedule_df[use_cols].to_csv(output_path, index=False, date_format="%Y/%m/%d")
    return output_path
