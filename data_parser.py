import pandas as pd
import numpy as np

def parse_match_data(file_path):
    """
    Loads and parses Wyscout match exports. 
    Extracts the team/opponent season baseline before filtering out 
    the rows to isolate individual player statistics.
    """
    # 1. Load the raw spreadsheet
    df = pd.read_excel(file_path)
    
    # Clean up column spaces to prevent string matching bugs
    df.columns = [str(col).strip() for col in df.columns]
    
    # 2. Extract summary baseline row before any rows are dropped
    # Looks for 'Season Average', 'Summary', or team name rows provided by Wyscout
    summary_mask = df.iloc[:, 0].astype(str).str.contains('Season Average|Summary|Opponents|Louisville City', case=False, na=False)
    summary_rows = df[summary_mask]
    
    opponent_season_avg = None
    if not summary_rows.empty:
        # Pull the value from your target metric column (e.g., 'Goals' or 'Metric_Value')
        target_col = 'Metric_Value' if 'Metric_Value' in df.columns else df.columns[1]
        raw_avg = summary_rows[target_col].values[0]
        opponent_season_avg = pd.to_numeric(raw_avg, errors='coerce')
    
    # Fallback to 0.0 if the baseline is missing or resolves to NaN
    if pd.isna(opponent_season_avg):
        opponent_season_avg = 0.0

    # 3. Clean and isolate individual player statistics
    # Filters out the summary rows so they don't break player-specific charts
    df_players = df[~summary_mask].copy()
    
    # Drop rows where critical identifier info is missing
    if 'Player' in df_players.columns:
        df_players = df_players.dropna(subset=['Player'])
    else:
        df_players = df_players.dropna(subset=[df_players.columns[0]])
    
    return df_players, opponent_season_avg
