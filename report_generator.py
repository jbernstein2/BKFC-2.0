import plotly.graph_objects as go
import numpy as np
import pandas as pd

def build_grouped_bar_chart(df_metrics, opponent_name, season_baseline=None, primary_color='#000000', opponent_color='#A6A6A6'):
    # 1. Clean columns
    df_metrics.columns = [str(c).strip() for c in df_metrics.columns]
    
    # 2. Filter out top-level summary metadata (rows where Date is null/empty)
    # Your Date column is index 0
    match_data = df_metrics.dropna(subset=[df_metrics.columns[0]]).copy()
    
    # 3. Target the 5th column (Index 4) for Team names
    team_col_idx = 4
    
    # Use the 5th column to identify Brooklyn vs the specific opponent
    # We look for rows that contain 'Brooklyn' to set our primary baseline
    bk_data = match_data[match_data.iloc[:, team_col_idx].astype(str).str.contains('Brooklyn', case=False, na=False)]
    
    # We look for rows that DON'T contain 'Brooklyn' to isolate the opponent
    opp_data = match_data[~match_data.iloc[:, team_col_idx].astype(str).str.contains('Brooklyn', case=False, na=False)]
    
    # 4. Safety check
    if bk_data.empty or opp_data.empty:
        return go.Figure()

    # 5. Extract the metric value (using the last column as the target)
    metric_key = df_metrics.columns[-1]
    
    # Force float conversion for the values
    b_fc_val = round(float(pd.to_numeric(bk_data.iloc[0][metric_key], errors='coerce')), 2)
    opp_val = round(float(pd.to_numeric(opp_data.iloc[0][metric_key], errors='coerce')), 2)
    
    # 6. Generate Plotly Figure
    fig = go.Figure()
    fig.add_trace(go.Bar(x=[metric_key], y=[b_fc_val], name='Brooklyn', marker_color=primary_color))
    fig.add_trace(go.Bar(x=[metric_key], y=[opp_val], name=f"{opponent_name} (Match)", marker_color=opponent_color))
    
    if season_baseline and not np.isnan(float(season_baseline)):
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
