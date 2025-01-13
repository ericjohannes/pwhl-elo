#!/bin/bash
FN="$(pwhlelo getgames --season-id 5 --output-path ../data/input/results/wphl_results_clean_data.csv)"
echo "${FN}"

ALLRESULTSFN="$(pwhlelo update --input $FN --output-dir ../data/output/all_results/)"
PROJECTIOSNFN="$(pwhlelo projections)"
pwhlelo chartable --input $ALLRESULTSFN --output-dir ./data/output

cp ../data/output/pwhl_latest_elos.json ../pwhl-elo-frontend/src/assets/pwhl_latest_elos.json
cp $PROJECTIOSNFN ../pwhl-elo-frontend/src/assets/game_projections.json
cp ../data/output/chartable/chartable_wphl_elos.json ../pwhl-elo-frontend/src/assets/chartable_wphl_elos.json
