This is a Python package for calculating the Elo of the PWHL.

# Updating with new data
1. update scores in clean data file
2. Run script and update all results file and latest Elos file
3. Run script and update next 5 projections file
4. Run script to update chartable data
5. Move data into website folder
6. Build and deploy website

## detailed steps to update
1. do manually
2. update all results file and latest Elos file
```
pwhlelo update --input /Users/eric/projects/pwhl-elo/data/output/all_results/wphl_elos_2024-11-24_19:37:35.csv --output-dir /Users/eric/projects/pwhl-elo/data/output/all_results/
```
3. Run script and update next 5 projections file
```
pwhlelo projections
```
4.
```
pwhlelo chartable --input ./data/output/all_results/wphl_elos_2024-12-12_15:29:31.csv" --output-dir ./data/output
```