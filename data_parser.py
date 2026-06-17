import pandas as pd
import pypdf
import io

def parse_team_stats(file_obj):
    """Dynamically detects file type and extracts raw, unaltered spreadsheet rows."""
    file_name = file_obj.name.lower()
    
    if file_name.endswith('.csv'):
        df = pd.read_csv(io.BytesIO(file_obj.getvalue()))
    else:
        df = pd.read_excel(io.BytesIO(file_obj.getvalue()), sheet_name='TeamStats')
        
    return df  # Returns completely raw dataframe to preserve summary rows

def read_pdf_page(pdf_file, page_num):
    """Extracts raw text content from a localized page number layer."""
    pdf_reader = pypdf.PdfReader(io.BytesIO(pdf_file.getvalue()))
    return pdf_reader.pages[page_num].extract_text()

def get_pdf_total_pages(pdf_file):
    """Returns total indexable pages inside the target match document."""
    pdf_reader = pypdf.PdfReader(io.BytesIO(pdf_file.getvalue()))
    return len(pdf_reader.pages)

def query_pdf_keyword(pdf_file, keyword):
    """Scans the document string fields to locate matched page references."""
    pdf_reader = pypdf.PdfReader(io.BytesIO(pdf_file.getvalue()))
    matched_pages = []
    for idx in range(len(pdf_reader.pages)):
        text = pdf_reader.pages[idx].extract_text().lower()
        if keyword.lower() in text:
            matched_pages.append(idx + 1)
    return matched_pages
