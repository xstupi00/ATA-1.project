"""Data frame grouping."""

import os

# 3rd party modules
import pandas as pd

def replace_indices_with_values(df):
    def char_range(c1, c2):
        """Generates the characters from `c1` to `c2`, inclusive."""
        for c in range(ord(c1), ord(c2) + 1):
            yield chr(c)

    # Replace source and destination places with name of the stations
    for idx, value in zip(range(1, 5), char_range('A', 'E')):
        df['src'] = df['src'].astype(str).str.replace(str(idx), value)
        df['dst'] = df['dst'].astype(str).str.replace(str(idx), value)

    # Replace time intervals indices with relevant time intervals of transportation period
    time_intervals = [f"({str(i)},{str(i+10)}]" for i in range(0, 60, 10)] + ["(70, inf)"]
    for idx, time_interval in zip(range(1, 8), time_intervals):
        df['transport_time'] = df['transport_time'].astype(str).str.replace(str(idx), time_interval)

    # Return aggregated df with substituted indices by relevant values
    return df


def aggregate():
    # Get absolute path
    path = os.path.abspath(os.path.dirname(__file__))
    # Load pair-wise combination generated table from csv file
    df = pd.read_csv(os.path.join(path, './block_indices.csv'))
    # Set the aggregation function to aggregate values to the lists in individual columns
    aggregation_functions = {'transport_time': lambda x: list(x), 'dst': lambda x: list(x), 'src': lambda x: list(x)}
    # Group and sort the columns from data-set according to their values
    aggregated_df = df.groupby(
        ['slots', 'capacity', 'total_weight']
    ).aggregate(aggregation_functions).sort_values(by=['src'], key=lambda col: col.str.len(), ascending=False)
    # Replace the indices with concrete values within aggregated columns
    aggregated_df = replace_indices_with_values(aggregated_df)
    with open(os.path.join(path, "./aggregated_table.csv"), "w") as text_file:
        text_file.write(aggregated_df.to_csv())

if __name__ == '__main__':
    aggregate()