# before a new season we want to revert each team's final Elo from the season prior toward the mean. This code is to support a command that does that.

from pwhl_elo.utils import revert_elo_to_mean

revert_elo_to_mean()