import plotly.graph_objects as go
import numpy as np
import pandas as pd

def build_grouped_bar_chart(df_metrics, opponent_name, season_baseline=None, primary_color='#000000', opponent_color='#A6A6A6', has_baseline=None):
    """
    Generates a grouped bar chart for Brooklyn FC vs an Opponent.
    Accepts both 'season_baseline' and legacy 'has_baseline' parameters gracefully.
    """
    # Parameter normalization safety layer
    if season_baseline is None and has_baseline is not None:
        season_baseline = has_baseline

    fig = go.Figure()
    
    b_fc_val = round(float(pd.to_numeric(df_metrics['Brooklyn_FC'].iloc[0], errors='coerce')), 2)
    opp_val = round(float(pd.to_numeric(df_metrics['Opponent'].iloc[0], errors='coerce')), 2)
    metric_label = str(df_metrics['Metric_Name'].iloc[0])
    
    # 1. Brooklyn FC
    fig.add_trace(go.Bar(
        x=[metric_label],
        y=[b_fc_val],
        name='Brooklyn FC',
        marker_color=primary_color,
        text=[f"{b_fc_val}"],
        textposition='auto'
    ))
    
    # 2. Opponent Performance
    fig.add_trace(go.Bar(
        x=[metric_label],
        y=[opp_val],
        name=f"{opponent_name} (Match)",
        marker_color=opponent_color,
        text=[f"{opp_val}"],
        textposition='auto'
    ))
    
    # 3. Baseline Profile
    if season_baseline is not None and not isinstance(season_baseline, bool) and not np.isnan(float(season_baseline)):
        base_val = round(float(season_baseline), 2)
        fig.add_trace(go.Bar(
            x=[metric_label],
            y=[base_val],
            name=f"{opponent_name} (Season Avg)",
            marker_color='#4A90E2',
            text=[f"{base_val}"],
            textposition='auto'
        ))
        
    fig.update_layout(
        barmode='group',
        title=f"Tactical Context: Brooklyn FC vs {opponent_name}",
        xaxis_title="Performance Domain",
        yaxis_title="Value",
        template="plotly_white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
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
