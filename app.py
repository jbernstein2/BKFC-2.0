import streamlit as st
import pandas as pd

# Micro-Module Custom Imports
import branding as brand
import data_parser as parser
import insights as intelligence
import report_generator as generator

# Execute Page Base Configurations
st.set_page_config(page_title="Brooklyn FC - Tactical Hub", layout="wide", initial_sidebar_state="expanded")
brand.apply_custom_theme()

st.title("⚽ Brooklyn FC Match Report Generator")
st.subheader("Contextual Performance Analytics vs. Opponent Season Baselines")

# SIDEBAR ARCHITECTURE: ACCEPT BOTH EXCEL AND CSV INTERCHANGEABLY
st.sidebar.header("📥 1. Primary Match Ingestion")
uploaded_bk_excel = st.sidebar.file_uploader("Upload Brooklyn Match Log (Excel or CSV)", type=["xlsx", "csv"])
uploaded_pdf = st.sidebar.file_uploader("Upload Wyscout Match PDF (Optional)", type=["pdf"])

st.sidebar.header("📊 2. Baseline Benchmarking")
uploaded_opp_excel = st.sidebar.file_uploader("Upload Opponent Season Data (Excel/CSV)", type=["xlsx", "csv"])

# Safe conditional interface evaluation 
if uploaded_bk_excel is not None:
    try:
        # Parse the raw sheet and safely extract both individual player metrics and the opponent season baseline
        raw_df, opponent_baseline = parser.parse_match_data(uploaded_bk_excel)
        
        # Clean up empty layout spacer rows for the match picker
        df_stats = raw_df.dropna(subset=['Match', 'Team']).copy()
        
        # Match Slicing Dropdowns
        match_options = sorted(df_stats['Match'].unique())
        selected_match = st.sidebar.selectbox("🎯 Target Match Analysis", match_options)

        match_rows = df_stats[df_stats['Match'] == selected_match]
        brooklyn_data = match_rows[match_rows['Team'] == 'Brooklyn']
        opponent_data = match_rows[match_rows['Team'] != 'Brooklyn']

        if brooklyn_data.empty or opponent_data.empty:
            st.warning("⚠️ Formatting Alert: Could not distinctively parse data rows for 'Brooklyn'. Please check sheet spelling values.")
        else:
            opp_team_name = opponent_data['Team'].values[0]

            # Opponent Baseline Data Extraction
            opp_baseline = None
            if uploaded_opp_excel is not None:
                try:
                    df_opp_raw = parser.parse_team_stats(uploaded_opp_excel)
                    opp_baseline, game_count = intelligence.compile_opponent_baseline(df_opp_raw, opp_team_name)
                    st.sidebar.success(f"✅ Loaded {game_count} baseline matches for {opp_team_name}.")
                except Exception as e:
                    st.sidebar.error(f"Could not compute opponent historical averages: {e}")

            # Sidebar Data Meta-Injections
            st.sidebar.markdown("---")
            st.sidebar.markdown(f"**Brooklyn System:** {brooklyn_data['Scheme'].values[0]}")
            st.sidebar.markdown(f"**{opp_team_name} System:** {opponent_data['Scheme'].values[0]}")

            # UI LAYOUT TABS
            tab1, tab2, tab3 = st.tabs(["📊 Performance Comparison", "🕸️ Tactical Style Identity", "📄 PDF Match Report Reader"])

            # TAB 1: CARD DASHBOARDS & CHARTS
            with tab1:
                st.markdown(f"### Performance Dashboard: Brooklyn vs {opp_team_name}")
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    brand.render_metric_card("BKLYN Goals", brooklyn_data['Goals'].values[0])
                with col2:
                    opp_g = opponent_data['Goals'].values[0]
                    base_g = opp_baseline['Goals'] if opp_baseline else None
                    brand.render_metric_card(f"{opp_team_name} Goals", opp_g, baseline_val=base_g, is_opponent=True)
                with col3:
                    brand.render_metric_card("BKLYN xG", brooklyn_data['xG'].values[0])
                with col4:
                    opp_xg = opponent_data['xG'].values[0]
                    base_xg = opp_baseline['xG'] if opp_baseline else None
                    brand.render_metric_card(f"{opp_team_name} xG", opp_xg, baseline_val=base_xg, is_opponent=True)

                st.markdown("---")
                
                try:
                    df_bar_data = intelligence.structure_comparison_dataframe(brooklyn_data, opponent_data, opp_baseline, opp_name=opp_team_name)
                    fig_bar = generator.build_grouped_bar_chart(df_bar_data, opp_team_name, has_baseline=(opp_baseline is not None))
                    st.plotly_chart(fig_bar, use_container_width=True)
                except Exception as chart_err:
                    st.error(f"Could not construct metrics graphs: {chart_err}. Verify column positioning matches standard structures.")

            # TAB 2: SPIDER VISUALIZATIONS
            with tab2:
                st.markdown("### Tactical Profile Web")
                try:
                    fig_radar = generator.build_radar_profile_web(brooklyn_data, opponent_data, opp_baseline, opp_team_name=opp_team_name)
                    st.plotly_chart(fig_radar, use_container_width=True)
                except Exception as radar_err:
                    st.error(f"Could not render radar plot mapping vectors: {radar_err}")

            # TAB 3: PDF CONSOLE READER
            with tab3:
                st.markdown("### Raw PDF Document Parser")
                if uploaded_pdf is not None:
                    try:
                        total_pages = parser.get_pdf_total_pages(uploaded_pdf)
                        st.success(f"Successfully processed match document: {uploaded_pdf.name} ({total_pages} Pages)")
                        
                        p_select = st.number_input("Jump to Page", min_value=1, max_value=total_pages, value=1)
                        extracted_text = parser.read_pdf_page(uploaded_pdf, p_select - 1)
                        st.text_area("Console Log Page Data", value=extracted_text, height=300)
                        
                        query = st.text_input("🔍 Search specific player name or metric inside PDF text nodes")
                        if query:
                            matched_pages = parser.query_pdf_keyword(uploaded_pdf, query)
                            if matched_pages:
                                st.write(f"🎯 Keyword match located on pages: **{matched_pages}**")
                            else:
                               st.write("❌ No matching text mentions located inside document.")
                    except Exception as e:
                        st.error(f"PDF engine failed to handle text streams: {e}")
                else:
                    st.info("ℹ️ Upload a standard Wyscout match report PDF via the sidebar file uploader to activate this panel.")
                    
    except Exception as startup_err:
        st.error(f"🚨 Structural processing mismatch parsing data source: {startup_err}")

else:
    # Safe default welcome screen
    st.markdown("### 📋 Welcome to the Brooklyn FC Performance Hub")
    st.info("👈 Please utilize the sidebar file controls to ingest your primary 'Brooklyn Match Log (Excel/CSV)' sheet to dynamically construct data graphs.")
