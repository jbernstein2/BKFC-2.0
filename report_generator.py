import plotly.graph_objects as go
import numpy as np
import pandas as pd

def build_grouped_bar_chart(df_metrics, opponent_name, season_baseline=None, primary_color='#000000', opponent_color='#A6A6A6'):
    """
    Generates a grouped bar chart for Brooklyn FC vs an Opponent.
    Fixes NaN graph voids, locks rounding precision, and ensures clean labeling.
    """
    fig = go.Figure()
    
    # Ensure values are numeric and rounded safely to 2 decimal places
    b_fc_val = round(float(pd.to_numeric(df_metrics['Brooklyn_FC'].iloc[0], errors='coerce')), 2)
    opp_val = round(float(pd.to_numeric(df_metrics['Opponent'].iloc[0], errors='coerce')), 2)
    metric_label = str(df_metrics['Metric_Name'].iloc[0])
    
    # 1. Brooklyn FC Match Performance Bar
    fig.add_trace(go.Bar(
        x=[metric_label],
        y=[b_fc_val],
        name='Brooklyn FC',
        marker_color=primary_color,
        text=[f"{b_fc_val}"],
        textposition='auto'
    ))
    
    # 2. Opponent Match Performance Bar
    fig.add_trace(go.Bar(
        x=[metric_label],
        y=[opp_val],
        name=f"{opponent_name} (Match)",
        marker_color=opponent_color,
        text=[f"{opp_val}"],
        textposition='auto'
    ))
    
    # 3. Opponent Season Baseline Bar (Only added if a valid baseline exists)
    if season_baseline is not None and not np.isnan(season_baseline):
        base_val = round(float(season_baseline), 2)
        fig.add_trace(go.Bar(
            x=[metric_label],
            y=[base_val],
            name=f"{opponent_name} (Season Avg)",
            marker_color='#4A90E2',  # Distinct baseline color
            text=[f"{base_val}"],
            textposition='auto'
        ))
        
    # Layout and styling configurations for the dashboard interface
    fig.update_layout(
        barmode='group',
        title=f"Tactical Context: Brooklyn FC vs {opponent_name}",
        xaxis_title="Performance Domain",
        yaxis_title="Value",
        template="plotly_white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    return fig
