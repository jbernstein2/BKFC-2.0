import pandas as pd
import numpy as np

def compile_opponent_baseline(df_opp_raw, opp_team_name=None):
    """
    Extracts pre-calculated seasonal averages from the opponent baseline row.
    Handles both the aggregated stats and individual match data.
    """
    if df_opp_raw.empty:
        return None, 0
    
    # Look for the "Opponents" row which contains season averages
    try:
        opponents_mask = df_opp_raw.iloc[:, 4].astype(str).str.strip() == 'Opponents'
        if opponents_mask.any():
            baseline_row = df_opp_raw[opponents_mask].iloc[0]
        else:
            # Fallback to second row
            baseline_row = df_opp_raw.iloc[1] if len(df_opp_raw) > 1 else df_opp_raw.iloc[0]
        
        baseline = {
            'Goals': safe_numeric(baseline_row, 'Goals'),
            'xG': safe_numeric(baseline_row, 'xG'),
            'Possession, %': safe_numeric(baseline_row, 'Possession, %'),
            'Shots / on target': safe_numeric(baseline_row, 'Shots / on target'),
            'Passes / accurate': safe_numeric(baseline_row, 'Passes / accurate'),
            'Touches in penalty area': safe_numeric(baseline_row, 'Touches in penalty area'),
            'PPDA': safe_numeric(baseline_row, 'PPDA'),
            'Duels / won': safe_numeric(baseline_row, 'Duels / won'),
            'Aerial duels / won': safe_numeric(baseline_row, 'Aerial duels / won'),
            'Defensive duels / won': safe_numeric(baseline_row, 'Defensive duels / won'),
            'Interceptions': safe_numeric(baseline_row, 'Interceptions'),
        }
        
        match_count = len(df_opp_raw[df_opp_raw.iloc[:, 4].astype(str).str.contains('USL|Cup|Championship', case=False, na=False)])
        
        return baseline, match_count
    except Exception as e:
        print(f"Error compiling baseline: {e}")
        return None, 0


def safe_numeric(row, col_name):
    """Safely convert a value to numeric, returning NaN if not found."""
    try:
        val = row.get(col_name, np.nan)
        return float(val) if pd.notna(val) else np.nan
    except:
        return np.nan


def structure_comparison_dataframe(brooklyn_data, opponent_data, opp_baseline=None, opp_name="Opponent"):
    """
    Creates a comprehensive comparison DataFrame for the bar chart.
    Includes key tactical metrics.
    """
    bar_metrics = {
        'Possession %': 'Possession, %',
        'Goals': 'Goals',
        'xG': 'xG',
        'Total Shots': 'Shots / on target',
        'Touches in Box': 'Touches in penalty area',
        'PPDA (Defensive Press)': 'PPDA',
        'Duels Won': 'Duels / won',
        'Aerial Duels Won': 'Aerial duels / won',
        'Interceptions': 'Interceptions',
    }
    
    bar_data = []
    for label, col_name in bar_metrics.items():
        try:
            bk_val = float(brooklyn_data[col_name].values[0]) if col_name in brooklyn_data.columns else np.nan
            opp_val = float(opponent_data[col_name].values[0]) if col_name in opponent_data.columns else np.nan
            
            row = {
                'Metric': label,
                'Brooklyn FC (Match)': bk_val,
                f'{opp_name} (Match)': opp_val,
            }
            
            if opp_baseline and col_name in opp_baseline:
                baseline_val = opp_baseline.get(col_name, np.nan)
                if pd.notna(baseline_val):
                    row[f'{opp_name} (Season Avg)'] = baseline_val
            
            bar_data.append(row)
        except Exception as e:
            print(f"Error processing metric {label}: {e}")
            continue
    
    return pd.DataFrame(bar_data)


def generate_match_insights(brooklyn_data, opponent_data, opp_baseline=None, opp_name="Opponent"):
    """
    Generate actionable insights from match statistics.
    Compares Brooklyn's performance against opponent and their season baseline.
    """
    insights = {
        'offensive': [],
        'defensive': [],
        'possession': [],
        'warnings': []
    }
    
    try:
        # Goal-scoring efficiency
        bk_goals = float(brooklyn_data['Goals'].values[0]) if 'Goals' in brooklyn_data.columns else 0
        bk_xg = float(brooklyn_data['xG'].values[0]) if 'xG' in brooklyn_data.columns else 0
        opp_goals = float(opponent_data['Goals'].values[0]) if 'Goals' in opponent_data.columns else 0
        opp_xg = float(opponent_data['xG'].values[0]) if 'xG' in opponent_data.columns else 0
        
        if bk_xg > 0:
            bk_efficiency = (bk_goals / bk_xg) * 100
            if bk_efficiency > 100:
                insights['offensive'].append(f"🎯 Excellent finishing: Brooklyn converted {bk_efficiency:.0f}% of expected goals")
            elif bk_efficiency < 50:
                insights['offensive'].append(f"⚠️ Finishing concerns: Brooklyn underperformed xG by {100-bk_efficiency:.0f}%")
        
        # Shot volume
        bk_shots = float(brooklyn_data['Shots / on target'].values[0].split('/')[0]) if 'Shots / on target' in brooklyn_data.columns else 0
        opp_shots = float(opponent_data['Shots / on target'].values[0].split('/')[0]) if 'Shots / on target' in opponent_data.columns else 0
        
        if bk_shots > opp_shots * 1.5:
            insights['offensive'].append(f"📈 Dominant shot volume: Brooklyn ({bk_shots:.0f}) vs {opp_name} ({opp_shots:.0f})")
        elif bk_shots < opp_shots * 0.67:
            insights['warnings'].append(f"⚠️ Shot volume concern: Brooklyn ({bk_shots:.0f}) significantly below opponent ({opp_shots:.0f})")
        
        # Possession
        bk_poss = float(brooklyn_data['Possession, %'].values[0]) if 'Possession, %' in brooklyn_data.columns else 0
        opp_poss = float(opponent_data['Possession, %'].values[0]) if 'Possession, %' in opponent_data.columns else 0
        
        if bk_poss > 55:
            insights['possession'].append(f"🔄 Possession dominance: Brooklyn controlled {bk_poss:.1f}% of the ball")
        elif bk_poss < 45:
            insights['possession'].append(f"🔄 Low possession strategy: Brooklyn operated with {bk_poss:.1f}% possession")
        
        # Defensive pressure
        bk_ppda = float(brooklyn_data['PPDA'].values[0]) if 'PPDA' in brooklyn_data.columns else 0
        opp_ppda = float(opponent_data['PPDA'].values[0]) if 'PPDA' in opponent_data.columns else 0
        
        if bk_ppda < opp_ppda:
            insights['defensive'].append(f"🛡️ Aggressive pressing: Brooklyn applies pressure every {bk_ppda:.2f} passes ({opp_ppda:.2f} for opponent)")
        else:
            insights['defensive'].append(f"🛡️ Compact defense: Brooklyn allows pressure every {bk_ppda:.2f} passes")
        
        # Defensive duels
        bk_duels = float(brooklyn_data['Defensive duels / won'].values[0].split('/')[1]) if 'Defensive duels / won' in brooklyn_data.columns else 0
        opp_duels = float(opponent_data['Defensive duels / won'].values[0].split('/')[1]) if 'Defensive duels / won' in opponent_data.columns else 0
        
        if bk_duels > opp_duels:
            insights['defensive'].append(f"💪 Duel dominance: Brooklyn won {bk_duels:.0f}% of defensive duels vs {opp_duels:.0f}%")
        
        # Box presence
        bk_box = float(brooklyn_data['Touches in penalty area'].values[0]) if 'Touches in penalty area' in brooklyn_data.columns else 0
        opp_box = float(opponent_data['Touches in penalty area'].values[0]) if 'Touches in penalty area' in opponent_data.columns else 0
        
        if bk_box > opp_box:
            insights['offensive'].append(f"📍 Box threat: Brooklyn created {bk_box:.0f} touches in the box vs {opp_box:.0f}")
        
    except Exception as e:
        print(f"Error generating insights: {e}")
    
    return insights
