import pandas as pd
import numpy as np
from datetime import datetime
import os
import re


def get_newest_file(input_dir: str):
    """
    Finds the newest file from a directory based on timestamp
    """
    pattern = r"(\d{4}-\d{2}-\d{2}_\d{2}:\d{2}:\d{2})"
    files = os.listdir(input_dir)
    date_times = []
    for f in files:
        match = re.search(pattern, f)
        if match:
            date_times.append(
                # probably could just sort it as a string
                datetime.strptime(match.group(1), "%Y-%m-%d_%H:%M:%S")
            )

    date_times.sort(reverse=True)
    source_file = date_times[0].strftime("%Y-%m-%d_%H:%M:%S")
    return os.path.join(input_dir, source_file)
          

if __name__ == "__main__":
    TIMESTAMP = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    OUTPUT_DIR = os.path.join('data', 'output')
    INPUT_DIR = os.path.join('data', 'output', 'all_results')

    source_path = get_newest_file(INPUT_DIR)
    print(source_path)


