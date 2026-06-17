import pandas as pd
import numpy as np
import pypdf
import io

def parse_match_data(file_path):
    """
    Loads and parses Wyscout match exports.
    Extracts the team/opponent season baseline and match-specific data.
    Handles both Excel and CSV formats.
    """
    # Determine file type and read accordingly
    if isinstance(file_path, str):
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)
    else:
        # Handle Streamlit uploaded file
        try:
            df = pd.read_excel(file_path)
        except:
            df = pd.read_csv(file_path)
    
    df.columns = [str(col).strip() for col in df.columns]
    
    # Extract season average rows (Brooklyn and Opponents rows)
    opponent_season_avg = None
    summary_data = {}
    
    for idx, row in df.iterrows():
        team_val = str(row.iloc[4]) if len(row) > 4 else ""
        if team_val.strip() == "Opponents":
            # This is the opponent season average row
            summary_data['Opponents'] = row
            break
    
    # Get actual match data (remove summary rows)
    summary_mask = df.iloc[:, 4].astype(str).isin(['Brooklyn', 'Opponents', ''])
    df_matches = df[summary_mask].copy()
    
    return df_matches, summary_data


def parse_team_stats(file_path):
    """
    Parse team statistics file and extract season averages.
    Returns DataFrame with both team and opponent season baselines.
    """
    try:
        if isinstance(file_path, str):
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
            else:
                df = pd.read_excel(file_path)
        else:
            try:
                df = pd.read_excel(file_path)
            except:
                df = pd.read_csv(file_path)
        
        df.columns = [str(col).strip() for col in df.columns]
        return df
    except Exception as e:
        print(f"Error parsing team stats: {e}")
        return pd.DataFrame()


def get_pdf_total_pages(pdf_file):
    """
    Safely reads a scouting lookup PDF stream and returns total pages.
    """
    try:
        reader = pypdf.PdfReader(pdf_file)
        return len(reader.pages)
    except Exception as e:
        print(f"Error parsing PDF metadata stream: {e}")
        return 0


def read_pdf_page(pdf_file, page_num=0):
    """
    Extracts text from a specific page of the PDF.
    """
    try:
        reader = pypdf.PdfReader(pdf_file)
        if page_num >= len(reader.pages):
            return "Page number out of range"
        page = reader.pages[page_num]
        text = page.extract_text()
        return text if text else "No text found on this page"
    except Exception as e:
        return f"Error reading page: {e}"


def query_pdf_keyword(pdf_file, keyword):
    """
    Searches for a keyword across all pages in the PDF.
    Returns list of page numbers (1-indexed) where keyword is found.
    """
    try:
        reader = pypdf.PdfReader(pdf_file)
        matched_pages = []
        
        for page_num, page in enumerate(reader.pages):
            text = page.extract_text().lower()
            if keyword.lower() in text:
                matched_pages.append(page_num + 1)  # 1-indexed for user display
        
        return matched_pages
    except Exception as e:
        print(f"Error querying PDF: {e}")
        return []
