import plotly.graph_objects as go
import numpy as np
import pandas as pd

def build_grouped_bar_chart(df_metrics, opponent_name, season_baseline=None, primary_color='#000000', opponent_color='#A6A6A6', has_baseline=None):
    # 1. Clean column names (strip whitespace)
    df_metrics.columns = [str(c).strip() for c in df_metrics.columns]
    
    # 2. Find which column contains the team names
    # It looks for the first column that contains 'Brooklyn' or 'Opponent'
    team_col = None
    for col in df_metrics.columns:
        if 'brooklyn' in df_metrics[col].astype(str).str.lower().values[0]:
            team_col = col
            break
    
    if not team_col:
        # Fallback: assume the second column (index 1) is the Team column based on your file
        team_col = df_metrics.columns[1]

    # 3. Dynamic lookup using the identified team column
    bk_mask = df_metrics[team_col].astype(str).str.contains('Brooklyn', case=False)
    
    # Handle cases where team names might be "Louisville City" or "Opponents"
    # We grab the first row that ISN'T Brooklyn as the opponent
    bk_row = df_metrics[bk_mask].iloc[0]
    opp_row = df_metrics[~bk_mask].iloc[0]
    
    # Get the numeric metric (assuming the last column is the one you are plotting)
    metric_key = df_metrics.columns[-1]
    
    b_fc_val = round(float(pd.to_numeric(bk_row[metric_key], errors='coerce')), 2)
    opp_val = round(float(pd.to_numeric(opp_row[metric_key], errors='coerce')), 2)
    
    # --- Now proceed with your existing bar chart code ---
    fig = go.Figure()
    fig.add_trace(go.Bar(x=[metric_key], y=[b_fc_val], name='Brooklyn', marker_color=primary_color))
    fig.add_trace(go.Bar(x=[metric_key], y=[opp_val], name=f"{opponent_name} (Match)", marker_color=opponent_color))
    
    if season_baseline is not None and not np.isnan(float(season_baseline)):
        fig.add_trace(go.Bar(x=[metric_key], y=[round(float(season_baseline), 2)], 
                             name=f"{opponent_name} (Season Avg)", marker_color='#4A90E2'))
        
    fig.update_layout(barmode='group', title=f"Tactical Context: Brooklyn vs {opponent_name}", template="plotly_white")
    return fig

def build_radar_profile_web(df_radar, title="Tactical Style Comparison"):
    """
    Constructs a closed radar web graph mapping team tactical style profiles.
    Expects df_radar to have 'Metric' and 'Value' columns.
    """
    fig = go.Figure()

    # Fallback to prevent rendering voids if empty data arrives
    if df_radar.empty:
        df_radar = pd.DataFrame({'Metric': ['No Data'], 'Value': [0]})

    # Ensure radar loop closes completely by appending the first item to the end
    metrics = df_radar['Metric'].tolist()
    values = df_radar['Value'].tolist()
    metrics.append(metrics[0])
    values.append(values[0])

    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=metrics,
        fill='toself',
        fillcolor='rgba(0, 0, 0, 0.1)',
        line=dict(color='#000000', width=2),
        name=title
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max(values) * 1.1 if max(values) > 0 else 100]
            )
        ),
        showlegend=True,
        template="plotly_white",
        title=title
    )

    return fig
