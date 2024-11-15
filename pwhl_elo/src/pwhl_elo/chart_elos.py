import pandas as pd
import numpy as np


def create_charts():
    df = pd.read_csv( 
        "./pwhl/chartable_wphl_elos_2024-10-28_21:30:45.csv",
        header=0,
        usecols=['date', 'team', 'elo']
    )

    # make them all start at 1300
    start_data = []
    for x in df['team'].unique():
        start_data.append({
            'date': pd.to_datetime('12/31/2023'),
            'team': x,
            'elo': 1300
        })
    df = pd.concat([pd.DataFrame(start_data), df], ignore_index=True)
    df['date'] = pd.to_datetime(df.date)
    pivot_df = df.pivot(index='date', columns='team', values='elo')

    plot = pivot_df.interpolate(method='linear').plot()
    plot.legend(
        loc='center left',
        bbox_to_anchor=(.75, 0.5)
    )

    x_lims = [df.date.min(), pd.to_datetime('7/30/2024')]
    plot.set_xlim(x_lims)
    fig = plot.get_figure()
    fig.savefig("./pwhl/output.png")

if __name__ == "__main__":
    df = pd.read_csv( 
        "./pwhl/chartable_wphl_elos_2024-10-28_21:30:45.csv",
        header=0,
        usecols=['date', 'team', 'elo']
    )

    # make them all start at 1300
    start_data = []
    for x in df['team'].unique():
        start_data.append({
            'date': pd.to_datetime('12/31/2023'),
            'team': x,
            'elo': 1300
        })
    df = pd.concat([pd.DataFrame(start_data), df], ignore_index=True)
    df['date'] = pd.to_datetime(df.date)
    pivot_df = df.pivot(index='date', columns='team', values='elo')

    plot = pivot_df.interpolate(method='linear').plot()
    plot.legend(
        loc='center left',
        bbox_to_anchor=(.75, 0.5)
    )

    x_lims = [df.date.min(), pd.to_datetime('7/30/2024')]
    plot.set_xlim(x_lims)
    fig = plot.get_figure()
    fig.savefig("./pwhl/output.png")
