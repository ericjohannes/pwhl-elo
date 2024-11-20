from datetime import datetime

import numpy as np


def revert_elo_to_mean(season_ending_elo: int) -> int:
    """
    To account for revversion to mean, new players, coach etc. Bring an Elo 1/3 back to 1300
    """

    difference = season_ending_elo - 1300
    new_elo = season_ending_elo - (difference / 3)
    return int(np.round(new_elo))


def time_stamp() -> str:
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")


def expected_result(elo_home: int, elo_away: int) -> [np.float64, np.float64]:
    # 538 uses 50 for nfl https://fivethirtyeight.com/methodology/how-our-nhl-predictions-work/
    HOME_ADVANTAGE = 50

    # TODO: see if playoff adjustment of 1.25 should go here per
    # https://fivethirtyeight.com/methodology/how-our-nhl-predictions-work/
    rating_home = 10 ** ((elo_home + HOME_ADVANTAGE) / 400)
    rating_away = 10 ** (elo_away / 400)
    expected_score_home = rating_home / (rating_home + rating_away)

    return [expected_score_home, 1 - expected_score_home]
