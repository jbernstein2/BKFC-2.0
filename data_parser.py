import pandas as pd
import numpy as np
import pypdf
import io

def parse_match_data(file_path):
    """
    Loads and parses Wyscout match exports.
    Handles both Excel and CSV formats.
    Returns match-specific data rows.
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
    
    # Print debug info
    print(f"DEBUG: DataFrame shape: {df.shape}")
    print(f"DEBUG: Columns: {list(df.columns)}")
    print(f"DEBUG: First few rows:")
    print(df.head())
    
    # The Team column should be around index 4
    if len(df.columns) > 4:
        team_col = df.columns[4]
        print(f"DEBUG: Using team column: {team_col}")
        print(f"DEBUG: Unique team values: {df[team_col].unique()[:10]}")
    
    # Get all rows where we have actual data (not empty)
    # Filter out rows that are completely empty or contain only the season summary
    df_clean = df.dropna(subset=[df.columns[0]]).copy()  # Remove rows with no date
    
    # Remove rows where Team column contains only "Brooklyn" or "Opponents" (the summary rows)
    if len(df_clean.columns) > 4:
        team_col = df_clean.columns[4]
        # Keep rows where Team is not exactly 'Brooklyn' or 'Opponents' (these are the summary rows)
        # We want to keep rows like "Brooklyn" in match context rows
        df_clean = df_clean[~(df_clean[team_col].astype(str).str.strip().isin(['Brooklyn', 'Opponents']))].copy()
    
    print(f"DEBUG: After filtering, shape: {df_clean.shape}")
    
    # If we have data, return it
    if not df_clean.empty:
        return df_clean, {}
    
    # Fallback: return original dataframe minus truly empty rows
    df_original = df.dropna(how='all').copy()
    return df_original, {}


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
