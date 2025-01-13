import json
import os

import requests

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


def handle(seasonid, pwhl):
    """
    Gets all data for a season based on its id. Gets data from url specified in config object and
    saves it to location specified by config object.
    """
    params["season_id"] = seasonid
    r = requests.get(pwhl.url, params=params)
    data = r.json()
    fn = f"season_{seasonid}.json"
    output_path = os.path.join(pwhl.output_path, fn)
    # data["SiteKit"]["Schedule"]
    with open(output_path, "w") as f:
        json.dump(data["SiteKit"]["Schedule"], f)
    return output_path
