import pandas as pd

def compile_opponent_baseline(df_opp_raw, opp_team_name=None):
    """Extracts pre-calculated seasonal averages directly from Row 2 of the uploaded sheet."""
    if df_opp_raw.empty:
        return None, 0
        
    # Excel Row 2 corresponds exactly to DataFrame Index 0 (first row under headers)
    baseline_row = df_opp_raw.iloc[0]
    
    baseline = {
        'Goals': pd.to_numeric(baseline_row.get('Goals'), errors='coerce'),
        'xG': pd.to_numeric(baseline_row.get('xG'), errors='coerce'),
        'Possession, %': pd.to_numeric(baseline_row.get('Possession, %'), errors='coerce'),
        'Shots / on target': pd.to_numeric(baseline_row.get('Shots / on target'), errors='coerce'),
        'Unnamed: 9': pd.to_numeric(baseline_row.get('Unnamed: 9'), errors='coerce'),       
        'Unnamed: 13': pd.to_numeric(baseline_row.get('Unnamed: 13'), errors='coerce'),     
        'Touches in penalty area': pd.to_numeric(baseline_row.get('Touches in penalty area'), errors='coerce'),
        'PPDA': pd.to_numeric(baseline_row.get('PPDA'), errors='coerce'),
        'Unnamed: 25': pd.to_numeric(baseline_row.get('Unnamed: 25'), errors='coerce'),     
        'Unnamed: 49': pd.to_numeric(baseline_row.get('Unnamed: 49'), errors='coerce'),     
        'Unnamed: 80': pd.to_numeric(baseline_row.get('Unnamed: 80'), errors='coerce'),     
        'Unnamed: 92': pd.to_numeric(baseline_row.get('Unnamed: 92'), errors='coerce'),     
        'Unnamed: 95': pd.to_numeric(baseline_row.get('Unnamed: 95'), errors='coerce')      
    }
    return baseline, 1

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
        if opp_baseline and o_col in opp_baseline:
            row[f'{opp_name} (Season Baseline)'] = float(opp_baseline[o_col])
        bar_data.append(row)
        
    return pd.DataFrame(bar_data)
