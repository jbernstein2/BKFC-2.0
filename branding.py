import streamlit as st

def apply_custom_theme():
    """Injects high-performance dark mode sports UI theme configuration."""
    st.markdown("""
        <style>
        .main { background-color: #0f1116; color: #ffffff; }
        .stTabs [data-baseweb="tab"] { font-size: 16px; font-weight: 600; color: #a0aab2; }
        .stTabs [aria-selected="true"] { color: #00ffaa !important; border-bottom-color: #00ffaa !important; }
        h1, h2, h3, h4 { color: #ffffff; font-family: 'Helvetica Neue', Arial, sans-serif; }
        
        .metric-card { 
            background-color: #1a1f2c; 
            padding: 18px; 
            border-radius: 8px; 
            border-left: 5px solid #00ffaa; 
            margin-bottom: 12px;
        }
        .metric-card-opp { 
            background-color: #1a1f2c; 
            padding: 18px; 
            border-radius: 8px; 
            border-left: 5px solid #ff4b4b; 
            margin-bottom: 12px;
        }
        .baseline-text { color: #a0aab2; font-size: 13px; margin-top: 4px; font-weight: normal; }
        </style>
    """, unsafe_allow_html=True)

def render_metric_card(title, value, baseline_val=None, is_opponent=False):
    """Renders a beautifully formatted KPI component frame."""
    card_class = "metric-card-opp" if is_opponent else "metric-card"
    
    baseline_html = ""
    if is_opponent:
        if baseline_val is not None:
            baseline_html = f"<p class='baseline-text'>Season Avg: {baseline_val:.2f}</p>"
        else:
            baseline_html = "<p class='baseline-text'>No baseline uploaded</p>"
            
    html_content = f"""
    <div class="{card_class}">
        <h4>{title}</h4>
        <h2>{value}</h2>
        {baseline_html}
    </div>
    """
    return st.markdown(html_content, unsafe_allow_html=True)