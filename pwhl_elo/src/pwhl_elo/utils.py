import numpy as np


def revert_elo_to_mean(season_ending_elo: int) -> int:
    """
    To account for revversion to mean, new players, coach etc. Bring an Elo 1/3 back to 1300
    """

    difference = season_ending_elo - 1300
    new_elo = season_ending_elo - (difference/3)
    return int(np.round(new_elo))
