import plotly.graph_objects as go
import numpy as np
import pandas as pd

def build_grouped_bar_chart(df_metrics, opponent_name, season_baseline=None, primary_color='#000000', opponent_color='#A6A6A6'):
    df_metrics.columns = [str(c).strip() for c in df_metrics.columns]
    
    # 1. Strip rows without a Date
    match_data = df_metrics.dropna(subset=[df_metrics.columns[0]]).copy()
    
    # 2. Identify Team column (Column index 4)
    team_col = df_metrics.columns[4]
    
    # 3. Create masks
    # Use 'contains' with a fallback to ensure we find "Brooklyn"
    is_bk = match_data[team_col].astype(str).str.contains('Brooklyn', case=False, na=False)
    
    bk_data = match_data[is_bk]
    opp_data = match_data[~is_bk]
    
    # 4. DEBUG: If we can't find the data, print what we found to the console
    if bk_data.empty:
        print(f"DEBUG: No 'Brooklyn' rows found in column '{team_col}'. Values present: {match_data[team_col].unique()}")
        return go.Figure()
    if opp_data.empty:
        print(f"DEBUG: No opponent rows found. Values present: {match_data[team_col].unique()}")
        return go.Figure()

    # 5. Extract values
    metric_key = df_metrics.columns[-1]
    b_fc_val = round(float(pd.to_numeric(bk_data.iloc[0][metric_key], errors='coerce')), 0)
    opp_val = round(float(pd.to_numeric(opp_data.iloc[0][metric_key], errors='coerce')), 0)
    
    # 6. Plotting
    fig = go.Figure()
    fig.add_trace(go.Bar(x=[metric_key], y=[b_fc_val], name='Brooklyn', marker_color=primary_color))
    fig.add_trace(go.Bar(x=[metric_key], y=[opp_val], name=f"{opponent_name} (Match)", marker_color=opponent_color))
    
    if season_baseline and not np.isnan(float(season_baseline)):
        fig.add_trace(go.Bar(x=[metric_key], y=[round(float(season_baseline), 0)], 
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
