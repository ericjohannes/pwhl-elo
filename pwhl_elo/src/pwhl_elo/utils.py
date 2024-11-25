import math
from datetime import datetime
from typing import List

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


def expected_result(elo_home: int, elo_away: int) -> List[np.float64]:
    # 538 uses 50 for nfl https://fivethirtyeight.com/methodology/how-our-nhl-predictions-work/
    HOME_ADVANTAGE = 50

    # TODO: see if playoff adjustment of 1.25 should go here per
    # https://fivethirtyeight.com/methodology/how-our-nhl-predictions-work/
    rating_home = 10 ** ((elo_home + HOME_ADVANTAGE) / 400)
    rating_away = 10 ** (elo_away / 400)
    expected_score_home = rating_home / (rating_home + rating_away)

    return [expected_score_home, 1 - expected_score_home]


def clean_name(name: str) -> str:
    return name.strip().replace(" ", "_").lower()


def k_value() -> int:
    """
    weight matches more if stakes are higher. based on trial and error
    """
    # 6 is what 538 uses for NHL
    # https://fivethirtyeight.com/methodology/how-our-nhl-predictions-work/
    k = 6

    # TODO: explore if k should be different for playoffs
    # if fixture_type == 'playoffs':
    #     k = 15
    return k


def actual_result(goals_home: int, goals_away: int) -> List[float]:
    """
    returns points each team won as [<home team's points>, <away team's
    points>]. 1 for winning, .5 each for tying
    """
    if goals_home < goals_away:
        return [0, 1]
    if goals_home > goals_away:
        return [1, 0]
    elif goals_home == goals_away:
        return [0.5, 0.5]


def calculate_movm(goals_home: int, goals_away: int):
    """
    calculates margin of victory multiplyer. Based on 538's https://fivethirtyeight.com/methodology/
    how-our-nhl-predictions-work/
    """
    mov = abs(goals_home - goals_away)

    return 0.6686 * math.log(mov) + 0.8048


def calculate_elo(
    elo_home: int,
    elo_away: int,
    expected_win_home,
    expected_win_away,
    goals_home: int,
    goals_away: int,
) -> List[int]:
    """
    calculate the new elos from one fixture
    """
    k = k_value()
    actual_win_home, actual_win_away = actual_result(goals_home, goals_away)
    movm = calculate_movm(goals_home, goals_away)

    elo_new_home = elo_home + k * movm * (actual_win_home - expected_win_home)
    elo_new_away = elo_away + k * movm * (actual_win_away - expected_win_away)

    return [int(np.round(elo_new_home)), int(np.round(elo_new_away))]


def clean_montreal(team: str) -> str:
    """
    removes accent from montréal
    """
    return team.replace("é", "e")
