import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
from datetime import datetime

def build_grouped_bar_chart(df_metrics, opponent_name, season_baseline=None, primary_color='#000000', opponent_color='#A6A6A6'):
    """
    Creates a grouped bar chart comparing Brooklyn vs Opponent across key metrics.
    """
    try:
        df_plot = df_metrics.dropna(subset=['Metric']).copy()
        
        fig = go.Figure()
        
        # Brooklyn bars
        fig.add_trace(go.Bar(
            x=df_plot['Metric'],
            y=df_plot['Brooklyn FC (Match)'],
            name='Brooklyn FC (Match)',
            marker_color=primary_color,
            text=df_plot['Brooklyn FC (Match)'].round(1),
            textposition='auto'
        ))
        
        # Opponent bars
        if f'{opponent_name} (Match)' in df_plot.columns:
            fig.add_trace(go.Bar(
                x=df_plot['Metric'],
                y=df_plot[f'{opponent_name} (Match)'],
                name=f'{opponent_name} (Match)',
                marker_color=opponent_color,
                text=df_plot[f'{opponent_name} (Match)'].round(1),
                textposition='auto'
            ))
        
        # Season average line
        if f'{opponent_name} (Season Avg)' in df_plot.columns:
            fig.add_trace(go.Bar(
                x=df_plot['Metric'],
                y=df_plot[f'{opponent_name} (Season Avg)'],
                name=f'{opponent_name} (Season Avg)',
                marker_color='rgba(166, 166, 166, 0.5)',
                marker_pattern_shape='x',
                text=df_plot[f'{opponent_name} (Season Avg)'].round(1),
                textposition='auto'
            ))
        
        fig.update_layout(
            title=f"Tactical Context: Brooklyn FC vs {opponent_name}",
            barmode='group',
            template="plotly_white",
            hovermode='x unified',
            height=500,
            font=dict(size=12),
            xaxis_title="Metric",
            yaxis_title="Value"
        )
        
        return fig
    except Exception as e:
        print(f"Error building bar chart: {e}")
        return go.Figure()


def build_radar_profile_web(brooklyn_data, opponent_data, opp_baseline=None, opp_team_name="Opponent"):
    """
    Constructs a radar/spider web graph comparing team tactical profiles.
    """
    try:
        # Define key tactical metrics for radar
        metrics_map = {
            'Possession %': 'Possession, %',
            'Pass Accuracy': 'Passes / accurate',
            'Shots per Game': 'Shots / on target',
            'Box Entries': 'Touches in penalty area',
            'Defensive Intensity': 'PPDA',
            'Duel Win %': 'Duels / won',
        }
        
        bk_values = []
        opp_values = []
        baseline_values = []
        metrics_labels = []
        
        for label, col_name in metrics_map.items():
            try:
                # Normalize values to 0-100 scale for radar
                if 'PPDA' in col_name:
                    # Lower PPDA is better (inverted)
                    bk_val = max(0, 100 - (float(brooklyn_data[col_name].values[0]) * 10))
                    opp_val = max(0, 100 - (float(opponent_data[col_name].values[0]) * 10))
                    base_val = max(0, 100 - (opp_baseline.get(col_name, 50) * 10)) if opp_baseline else None
                else:
                    bk_val = float(brooklyn_data[col_name].values[0]) if col_name in brooklyn_data.columns else 0
                    opp_val = float(opponent_data[col_name].values[0]) if col_name in opponent_data.columns else 0
                    base_val = opp_baseline.get(col_name) if opp_baseline else None
                
                bk_values.append(bk_val)
                opp_values.append(opp_val)
                if base_val:
                    baseline_values.append(base_val)
                metrics_labels.append(label)
            except Exception as e:
                print(f"Error processing metric {label}: {e}")
                continue
        
        # Close the radar by adding first point at end
        bk_values.append(bk_values[0])
        opp_values.append(opp_values[0])
        metrics_labels_closed = metrics_labels + [metrics_labels[0]]
        if baseline_values:
            baseline_values.append(baseline_values[0])
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=bk_values,
            theta=metrics_labels_closed,
            fill='toself',
            fillcolor='rgba(0, 0, 0, 0.1)',
            line=dict(color='#000000', width=2),
            name='Brooklyn FC',
            hovertemplate='<b>Brooklyn FC</b><br>%{theta}: %{r:.1f}<extra></extra>'
        ))
        
        fig.add_trace(go.Scatterpolar(
            r=opp_values,
            theta=metrics_labels_closed,
            fill='toself',
            fillcolor='rgba(166, 166, 166, 0.1)',
            line=dict(color='#A6A6A6', width=2),
            name=opp_team_name,
            hovertemplate=f'<b>{opp_team_name}</b><br>%{{theta}}: %{{r:.1f}}<extra></extra>'
        ))
        
        if baseline_values:
            fig.add_trace(go.Scatterpolar(
                r=baseline_values,
                theta=metrics_labels_closed,
                line=dict(color='#4A90E2', width=2, dash='dash'),
                name=f'{opp_team_name} (Season Avg)',
                hovertemplate=f'<b>{opp_team_name} Season Avg</b><br>%{{theta}}: %{{r:.1f}}<extra></extra>'
            ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )
            ),
            showlegend=True,
            template="plotly_white",
            title=f"Tactical Profile: Brooklyn FC vs {opp_team_name}",
            height=600,
            font=dict(size=12)
        )
        
        return fig
    except Exception as e:
        print(f"Error building radar chart: {e}")
        return go.Figure()


def generate_pdf_report(brooklyn_data, opponent_data, opp_baseline, opp_name, insights, match_details):
    """
    Generates a comprehensive text-based match report with analysis.
    """
    report = []
    report.append("=" * 80)
    report.append("BROOKLYN FC COMPREHENSIVE MATCH REPORT".center(80))
    report.append("=" * 80)
    report.append("")
    
    # Match Header
    try:
        match_str = match_details.get('Match', 'Match Details Unavailable')
        competition = match_details.get('Competition', 'Unknown')
        date = match_details.get('Date', 'Unknown Date')
        duration = match_details.get('Duration', 'Unknown')
        
        report.append(f"MATCH: {match_str}")
        report.append(f"COMPETITION: {competition}")
        report.append(f"DATE: {date} | DURATION: {duration} min")
        report.append(f"BROOKLYN FORMATION: {brooklyn_data.get('Scheme', 'Unknown')}")
        report.append(f"{opp_name.upper()} FORMATION: {opponent_data.get('Scheme', 'Unknown')}")
        report.append("")
    except:
        pass
    
    # Score Summary
    report.append("FINAL SCORE".ljust(40) + "MATCH STATISTICS")
    report.append("-" * 80)
    try:
        bk_goals = int(brooklyn_data.get('Goals', 0))
        opp_goals = int(opponent_data.get('Goals', 0))
        report.append(f"Brooklyn FC {bk_goals}:{opp_goals} {opp_name}".ljust(40), end="")
    except:
        pass
    
    try:
        bk_xg = float(brooklyn_data.get('xG', 0))
        opp_xg = float(opponent_data.get('xG', 0))
        report.append(f"Expected Goals: BK {bk_xg:.2f} - {opp_xg:.2f} {opp_name}")
    except:
        report.append("")
    
    report.append("")
    
    # Key Metrics Section
    report.append("KEY PERFORMANCE METRICS".center(80))
    report.append("-" * 80)
    
    metrics_to_report = [
        ('Possession %', 'Possession, %', '%'),
        ('Shots / on Target', 'Shots / on target', ''),
        ('Pass Accuracy', 'Passes / accurate', ''),
        ('Touches in Penalty Area', 'Touches in penalty area', ''),
        ('PPDA (Defensive Press)', 'PPDA', ''),
        ('Duels Won', 'Duels / won', ''),
    ]
    
    try:
        report.append(f"{'Metric':<30} {'Brooklyn':<20} {opp_name:<20}")
        report.append("-" * 80)
        
        for display_name, col_name, unit in metrics_to_report:
            try:
                bk_val = brooklyn_data.get(col_name, 'N/A')
                opp_val = opponent_data.get(col_name, 'N/A')
                report.append(f"{display_name:<30} {str(bk_val):<20} {str(opp_val):<20}")
            except:
                continue
    except:
        pass
    
    report.append("")
    
    # Insights Section
    report.append("TACTICAL ANALYSIS".center(80))
    report.append("-" * 80)
    
    if insights:
        if insights.get('offensive'):
            report.append("\n🎯 OFFENSIVE INSIGHTS:")
            for insight in insights['offensive']:
                report.append(f"  • {insight}")
        
        if insights.get('defensive'):
            report.append("\n🛡️ DEFENSIVE INSIGHTS:")
            for insight in insights['defensive']:
                report.append(f"  • {insight}")
        
        if insights.get('possession'):
            report.append("\n🔄 POSSESSION INSIGHTS:")
            for insight in insights['possession']:
                report.append(f"  • {insight}")
        
        if insights.get('warnings'):
            report.append("\n⚠️ PERFORMANCE WARNINGS:")
            for warning in insights['warnings']:
                report.append(f"  • {warning}")
    
    report.append("")
    report.append("=" * 80)
    report.append(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("=" * 80)
    
    return "\n".join(report)
