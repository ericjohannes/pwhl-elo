import pytest
import numpy as np

from pwhl_elo.src.pwhl_elo.calculate_elo import (
    clean_name,
    actual_result,
    expected_result,
    calculate_movm,
    calculate_elo,
)


def test_clean_name():
    name = ' New York '
    assert clean_name(name) == 'new_york'


@pytest.mark.parametrize("h_goals,a_goals,expected", [
    [3, 1, [1, 0]],  # home has more goals
    [1, 3, [0, 1]],  # away has more goals
    [1, 1, [.5, .5]],  # equal goals
])
def test_actual_result(h_goals, a_goals, expected):
    assert actual_result(h_goals, a_goals) == expected


def test_expected_result():
    expected_home, expected_away = expected_result(1290, 1310)
    assert np.round(expected_home, 3) == .543
    assert np.round(expected_away, 3) == .457


def test_calculate_movm():
    assert np.round(calculate_movm(3, 1), 3) == 1.268


def test_calculate_elo():
    input = {
        'elo_home': 1290,
        'elo_away': 1310,
        'goals_home': 3,
        'goals_away': 4,
    }
    input['expected_win_home'], input['expected_win_away'], = expected_result(
        input['elo_home'], input['elo_away']
    )
    elo_new_home, elo_new_away = calculate_elo(**input) 
    assert elo_new_home == 1287
    assert elo_new_away == 1313