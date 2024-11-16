# before a new season we want to revert each team's final Elo from the season
# prior toward the mean. This code is to support a command that does that.
import json

from pwhl_elo.utils import revert_elo_to_mean, time_stamp

# suggested input and output
# input ../data/output/pwhl_final_elos.json
# output  ../data/output


def revert_elo_file(input: str, output_dir: str):
    TIMESTAMP = time_stamp()
    with open(input, "r") as f:
        data = json.load(f)
    print(data)

    # revert each team's Elo to the mean
    for team in data["teams"].keys():
        data["teams"][team] = revert_elo_to_mean(data["teams"][team])

    data["date"] = TIMESTAMP
    save_path = f"{output_dir}/pwhl_latest_elos.json"

    with open(save_path, "w") as f:
        json.dump(data, f)
    return save_path
