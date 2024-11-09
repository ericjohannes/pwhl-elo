a project to create and track Elo of the Professional Women's Hockey League


# Data Lineage
1. `data/input/wphl_results_clean_data.csv` has fixtures data. It is created manually from Google sheets, downloaded and placed here. It is the input for the other data sets.
2. `calculate_elo.py` takes `wphl_results_clean_data.csv` and outputs 3 files
    a. `wphl_elos_<date time>.csv` - a table of all fixtures with Elos calculated for games played. Projections calculated for games played.
    b. `pwhl_final_elos.json` - the latest ELo scores for all teams
    c. `chartable_wphl_elos.json` - Elos scores for each date and for each team. Designed to be used for a chart on the front end.
3. `upcoming_projection.py` takes the latest `wphl_elos_<date time>.csv`  file and creates `game_projections_<date time>.json`, which contains projections for the next five games played (from time the script was run). This accounts for if a new season is starting.





