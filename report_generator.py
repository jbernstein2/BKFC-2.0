import plotly.graph_objects as go

def build_grouped_bar_chart(df_bar, opp_team_name, has_baseline=False):
    """Generates side-by-side contextual horizontal bar graphs in Brooklyn FC brand colors."""
    fig = go.Figure()
    
    # Brooklyn FC - Gold Accent
    fig.add_trace(go.Bar(
        y=df_bar['Metric'], x=df_bar['Brooklyn FC (Match)'], 
        name='Brooklyn FC (Match)', orientation='h', marker_color='#D4AF37'
    ))
    
    # Opponent Match - Silver / Light Grey
    fig.add_trace(go.Bar(
        y=df_bar['Metric'], x=df_bar[f'{opp_team_name} (Match)'], 
        name=f'{opp_team_name} (Match)', orientation='h', marker_color='#8A95A5'
    ))
    
    # Opponent Seasonal Baseline - Translucent White/Silver
    if has_baseline and f'{opp_team_name} (Season Baseline)' in df_bar.columns:
        fig.add_trace(go.Bar(
            y=df_bar['Metric'], x=df_bar[f'{opp_team_name} (Season Baseline)'], 
            name=f'{opp_team_name} (Season Baseline)', orientation='h', 
            marker_color='rgba(255, 255, 255, 0.25)'
        ))
        
    fig.update_layout(
        barmode='group', 
        title="Did We Disrupt Their Tactical Style?",
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)', 
        font_color='#ffffff',
        xaxis=dict(gridcolor='#22262B'), 
        yaxis=dict(gridcolor='rgba(0,0,0,0)'),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig

def build_radar_profile_web(brooklyn_data, opponent_data, opp_baseline=None, opp_team_name="Opponent"):
    """Constructs technical efficiency radar charts mapping stylistic variance."""
    radar_labels = ['Pass Accuracy %', 'Duels Won %', 'Cross Accuracy %', 'Forward Pass %', 'Final 3rd Pass Acc %', 'Progressive Pass Acc %']
    
    b_radar = [
        float(brooklyn_data['Unnamed: 13'].values[0]), float(brooklyn_data['Unnamed: 25'].values[0]),
        float(brooklyn_data['Unnamed: 49'].values[0]), float(brooklyn_data['Unnamed: 80'].values[0]),
        float(brooklyn_data['Unnamed: 92'].values[0]), float(brooklyn_data['Unnamed: 95'].values[0])
    ]
    o_radar = [
        float(opponent_data['Unnamed: 13'].values[0]), float(opponent_data['Unnamed: 25'].values[0]),
        float(opponent_data['Unnamed: 49'].values[0]), float(opponent_data['Unnamed: 80'].values[0]),
        float(opponent_data['Unnamed: 92'].values[0]), float(opponent_data['Unnamed: 95'].values[0])
    ]
    
    fig = go.Figure()
    
    # Brooklyn Profile - Gold Fill
    fig.add_trace(go.Scatterpolar(
        r=b_radar, theta=radar_labels, fill='toself', 
        name='Brooklyn FC (Match)', line=dict(color='#D4AF37', width=2), 
        fillcolor='rgba(212, 175, 55, 0.15)'
    ))
    
    # Opponent Match Profile - Silver Fill
    fig.add_trace(go.Scatterpolar(
        r=o_radar, theta=radar_labels, fill='toself', 
        name=f'{opp_team_name} (Match)', line=dict(color='#8A95A5', width=2), 
        fillcolor='rgba(138, 149, 165, 0.15)'
    ))
    
    # Opponent Base Profile - Dashed White
    if opp_baseline:
        o_base_radar = [
            opp_baseline['Unnamed: 13'], opp_baseline['Unnamed: 25'],
            opp_baseline['Unnamed: 49'], opp_baseline['Unnamed: 80'],
            opp_baseline['Unnamed: 92'], opp_baseline['Unnamed: 95']
        ]
        fig.add_trace(go.Scatterpolar(
            r=o_base_radar, theta=radar_labels, fill='none', 
            name=f'{opp_team_name} (Season Baseline)', 
            line=dict(color='#FFFFFF', width=2, dash='dash')
        ))
        
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, gridcolor='#22262B'), angularaxis=dict(gridcolor='#22262B')),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#ffffff', 
        title="Style Distortions vs Normal Norms"
    )
    return fig
