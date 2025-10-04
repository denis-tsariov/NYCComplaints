import pandas as pd
from tqdm import tqdm

def check_data_structure():
    """Check the structure and years available in the 311 data"""
    
    # Read first chunk to see column names
    chunk = next(pd.read_csv('311_Service_Requests_from_2010_to_Present_20250928.csv', 
                            chunksize=1000, low_memory=False))
    
    print("Column names:")
    print(list(chunk.columns))
    print("\nFirst few rows:")
    print(chunk.head())
    
    # Check years available
    chunk['Created Date'] = pd.to_datetime(chunk['Created Date'], errors='coerce')
    print(f"\nSample years: {chunk['Created Date'].dt.year.unique()}")
    
    # Check for closed incidents
    print(f"\nClosed Date column exists: {'Closed Date' in chunk.columns}")
    if 'Closed Date' in chunk.columns:
        chunk['Closed Date'] = pd.to_datetime(chunk['Closed Date'], errors='coerce')
        closed_count = chunk['Closed Date'].notna().sum()
        print(f"Closed incidents in sample: {closed_count}/{len(chunk)}")

if __name__ == "__main__":
    check_data_structure()