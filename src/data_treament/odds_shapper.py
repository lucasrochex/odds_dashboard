import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from scipy import stats

def prepare_odd_df(df):
    df_pivot = df.set_index('timestamp').pivot(columns=['home', 'away'], values=['odd_h', 'odd_a', 'odd_draw'])
    df_pivot.columns = list(map("_".join, df_pivot.columns))
    #df_pivot.ffill(inplace=True)
    #df_pivot.bfill(inplace=True)
    return df_pivot

def sort_slopes(games_48):
    slopes = {}
    for team in games_48.columns:
        df = pd.DataFrame(columns=[team], data = games_48[team], index = games_48.index)
        df['date_ordinal']=pd.to_datetime(df.index).astype(np.int64)
        df['timestamp'] = pd.to_datetime(df.index)
        # Assuming df is your DataFrame and 'timestamp' is the column with timestamps
        df.dropna(inplace=True)
        max_timestamp = df['timestamp'].max()
        current_time = pd.Timestamp.now()
        print(max_timestamp)

# Check if the time difference is less than or equal to 10 minutes
        time_difference = current_time - max_timestamp
        is_within_10_minutes = time_difference >= timedelta(minutes=10)
        if is_within_10_minutes:
            continue    
        if len(df[team]) < 100:
            continue
        slope, intercept, r_value, p_value, std_err = stats.linregress(df['date_ordinal'], df[team])
        if slope == np.nan:
            continue
        slopes[team]=slope
        
    sorted_slopes = sorted(slopes.items(), key=lambda x:x[1])
    relevant_columns = []
    for game in sorted_slopes:
        relevant_columns.append(game[0])
    return relevant_columns