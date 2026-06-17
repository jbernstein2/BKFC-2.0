import plotly.graph_objects as go
import numpy as np
import pandas as pd

def build_grouped_bar_chart(df_metrics, opponent_name, season_baseline=None, primary_color='#000000', opponent_color='#A6A6A6'):
    # 1. Reset columns to ensure clean names
    df_metrics.columns = [str(c).strip() for c in df_metrics.columns]
    
    # 2. Heuristic: Drop rows that aren't real match data
    # Real match rows usually have a date or a valid numeric value in the last column.
    # We drop any rows where the 'Team' or 'Date' columns are null or clearly summary metadata
    if 'Date' in df_metrics.columns:
        match_data = df_metrics.dropna(subset=['Date']).copy()
    else:
        match_data = df_metrics.copy()
        
    # 3. Filter for specific entities (Brooklyn vs. Opponent)
    # Using 'contains' is safer than exact equality due to potential whitespace
    bk_data = match_data[match_data.iloc[:, 1].astype(str).str.contains('Brooklyn', case=False, na=False)]
    opp_data = match_data[~match_data.iloc[:, 1].astype(str).str.contains('Brooklyn', case=False, na=False)]
    
    # 4. Final safety check: Do we actually have rows?
    if bk_data.empty or opp_data.empty:
        # If we reach here, it means the filter failed to isolate the rows
        # Return an empty container to keep the app running
        return go.Figure()

    # Get the last column as the metric (standard for Wyscout exports)
    metric_key = df_metrics.columns[-1]
    
    b_fc_val = round(float(pd.to_numeric(bk_data.iloc[0][metric_key], errors='coerce')), 2)
    opp_val = round(float(pd.to_numeric(opp_data.iloc[0][metric_key], errors='coerce')), 2)
    
    # Generate Figure
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
