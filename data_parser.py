import pandas as pd
import numpy as np
import pypdf
import io

def parse_match_data(file_path):
    """
    Loads and parses Wyscout match exports.
    Handles both Excel and CSV formats.
    The CSV structure has:
    - Row 1: Brooklyn (season aggregate - no Date, no Match)
    - Row 2: Opponents (season aggregate - no Date, no Match)
    - Rows 3+: Individual matches with Date, Match, Team, and stats
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
    
    # Normalize column names
    df.columns = [str(col).strip() for col in df.columns]
    
    print(f"DEBUG: Loaded {len(df)} rows, {len(df.columns)} columns")
    print(f"DEBUG: Columns: {list(df.columns[:10])}")  # First 10 columns
    
    # The key is to filter by rows that have BOTH Date and Match populated
    # because the summary rows (Brooklyn, Opponents) have NO Date and NO Match
    
    # Find Date and Match columns
    date_col = None
    match_col = None
    team_col = None
    
    for col in df.columns:
        if 'Date' in col:
            date_col = col
        elif 'Match' in col:
            match_col = col
        elif 'Team' in col or col == df.columns[4]:
            team_col = col
    
    if team_col is None and len(df.columns) > 4:
        team_col = df.columns[4]
    
    print(f"DEBUG: Date column: {date_col}")
    print(f"DEBUG: Match column: {match_col}")
    print(f"DEBUG: Team column: {team_col}")
    
    # Filter: keep only rows where BOTH Date and Match have values
    # This automatically excludes the summary rows
    df_matches = df.copy()
    
    if date_col:
        df_matches = df_matches[df_matches[date_col].notna()]
        print(f"DEBUG: After filtering for Date values: {len(df_matches)} rows")
    
    if match_col:
        df_matches = df_matches[df_matches[match_col].notna()]
        print(f"DEBUG: After filtering for Match values: {len(df_matches)} rows")
    
    # Remove rows where both values are essentially empty/NaN
    df_matches = df_matches.dropna(how='all').copy()
    
    if team_col:
        print(f"DEBUG: Unique teams found: {df_matches[team_col].unique()}")
    
    print(f"DEBUG: Final match data shape: {df_matches.shape}")
    
    return df_matches, {}


def parse_team_stats(file_path):
    """
    Parse team statistics file and extract season averages.
    Returns DataFrame with all data.
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
