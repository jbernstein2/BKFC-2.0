import pandas as pd

def compile_opponent_baseline(df_opp_raw, opp_team_name):
    """Aggregates opponent performances down into a clean baseline dict mapping."""
    df_opp_filtered = df_opp_raw[df_opp_raw['Team'].str.lower() == opp_team_name.lower()]
    if df_opp_filtered.empty:
        df_opp_filtered = df_opp_raw  # Fallback if worksheet contains dedicated filtered views
        
    baseline = {
        'Goals': pd.to_numeric(df_opp_filtered['Goals'], errors='coerce').mean(),
        'xG': pd.to_numeric(df_opp_filtered['xG'], errors='coerce').mean(),
        'Possession, %': pd.to_numeric(df_opp_filtered['Possession, %'], errors='coerce').mean(),
        'Shots / on target': pd.to_numeric(df_opp_filtered['Shots / on target'], errors='coerce').mean(),
        'Unnamed: 9': pd.to_numeric(df_opp_filtered['Unnamed: 9'], errors='coerce').mean(),       
        'Unnamed: 13': pd.to_numeric(df_opp_filtered['Unnamed: 13'], errors='coerce').mean(),     
        'Touches in penalty area': pd.to_numeric(df_opp_filtered['Touches in penalty area'], errors='coerce').mean(),
        'PPDA': pd.to_numeric(df_opp_filtered['PPDA'], errors='coerce').mean(),
        'Unnamed: 25': pd.to_numeric(df_opp_filtered['Unnamed: 25'], errors='coerce').mean(),     
        'Unnamed: 49': pd.to_numeric(df_opp_filtered['Unnamed: 49'], errors='coerce').mean(),     
        'Unnamed: 80': pd.to_numeric(df_opp_filtered['Unnamed: 80'], errors='coerce').mean(),     
        'Unnamed: 92': pd.to_numeric(df_opp_filtered['Unnamed: 92'], errors='coerce').mean(),     
        'Unnamed: 95': pd.to_numeric(df_opp_filtered['Unnamed: 95'], errors='coerce').mean()      
    }
    return baseline, len(df_opp_filtered)

def structure_comparison_dataframe(brooklyn_data, opponent_data, opp_baseline=None, opp_name="Opponent"):
    """Maps custom tracked rows to structural comparison tables."""
    bar_metrics = {
        'Possession %': ('Possession, %', 'Possession, %'),
        'Total Shots': ('Shots / on target', 'Shots / on target'),
        'Pass Accuracy %': ('Unnamed: 13', 'Unnamed: 13'),
        'Touches in Box': ('Touches in penalty area', 'Touches in penalty area'),
        'PPDA (Defensive Press)': ('PPDA', 'PPDA')
    }
    
    bar_data = []
    for label, (b_col, o_col) in bar_metrics.items():
        row = {
            'Metric': label,
            'Brooklyn FC (Match)': float(brooklyn_data[b_col].values[0]),
            f'{opp_name} (Match)': float(opponent_data[o_col].values[0]),
        }
        if opp_baseline:
            row[f'{opp_name} (Season Baseline)'] = float(opp_baseline[o_col])
        bar_data.append(row)
        
    return pd.DataFrame(bar_data)