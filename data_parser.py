import pandas as pd
import numpy as np
import pypdf

def parse_match_data(file_path):
    """
    Loads and parses Wyscout match exports. 
    Extracts the team/opponent season baseline before filtering out 
    the rows to isolate individual player statistics.
    """
    df = pd.read_excel(file_path)
    df.columns = [str(col).strip() for col in df.columns]
    
    summary_mask = df.iloc[:, 0].astype(str).str.contains('Season Average|Summary|Opponents|Louisville City', case=False, na=False)
    summary_rows = df[summary_mask]
    
    opponent_season_avg = None
    if not summary_rows.empty:
        target_col = 'Metric_Value' if 'Metric_Value' in df.columns else df.columns[1]
        raw_avg = summary_rows[target_col].values[0]
        opponent_season_avg = pd.to_numeric(raw_avg, errors='coerce')
    
    if pd.isna(opponent_season_avg):
        opponent_season_avg = 0.0

    df_players = df[~summary_mask].copy()
    if 'Player' in df_players.columns:
        df_players = df_players.dropna(subset=['Player'])
    else:
        df_players = df_players.dropna(subset=[df_players.columns[0]])
    
    return df_players, opponent_season_avg


def parse_team_stats(file_path):
    """
    Legacy backwards-compatibility wrapper. 
    Returns only the filtered DataFrame to prevent unpacking crashes in legacy app setups.
    """
    df_players, _ = parse_match_data(file_path)
    return df_players


def get_pdf_total_pages(pdf_file):
    """
    Safely reads a scouting lookup PDF stream and returns total pages.
    """
    try:
        reader = pypdf.PdfReader(pdf_file)
        return len(reader.pages)
    except Exception as e:
        print(f"Error parsing PDF metadata stream: {e}")
        return 0
