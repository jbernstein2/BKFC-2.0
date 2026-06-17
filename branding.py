import streamlit as st

def apply_custom_theme():
    """Injects safe, isolated dark mode visual treatments for the dashboard elements."""
    st.markdown("""
        <style>
        /* Custom tactical card block containers */
        .tactical-card { 
            background-color: #161A1D; 
            padding: 20px; 
            border-radius: 8px; 
            border-left: 6px solid #D4AF37; /* Brooklyn Gold Edge */
            margin-bottom: 15px;
        }
        .tactical-card-opp { 
            background-color: #161A1D; 
            padding: 20px; 
            border-radius: 8px; 
            border-left: 6px solid #C0C0C0; /* Neutral Silver Edge for Opponents */
            margin-bottom: 15px;
        }
        .card-title { color: #A6A6A6; font-size: 14px; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px; }
        .card-value { color: #FFFFFF; font-size: 28px; font-weight: bold; margin: 0; }
        .card-baseline { color: #8A95A5; font-size: 12px; margin-top: 6px; }
        </style>
    """, unsafe_allow_html=True)

def render_metric_card(title, value, baseline_val=None, is_opponent=False):
    """Renders a robust HTML block layout card component."""
    card_style = "tactical-card-opp" if is_opponent else "tactical-card"
    
    baseline_html = ""
    if is_opponent:
        if baseline_val is not None:
            baseline_html = f"<div class='card-baseline'>Season Avg: {baseline_val:.2f}</div>"
        else:
            baseline_html = "<div class='card-baseline'>No baseline data available</div>"
            
    html_content = f"""
    <div class="{card_style}">
        <div class="card-title">{title}</div>
        <div class="card-value">{value}</div>
        {baseline_html}
    </div>
    """
    return st.markdown(html_content, unsafe_allow_html=True)
