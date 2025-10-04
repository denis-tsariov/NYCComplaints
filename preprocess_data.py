import pandas as pd
import numpy as np
from datetime import datetime
import warnings
from tqdm import tqdm
warnings.filterwarnings('ignore')

def preprocess_311_data():
    """
    Preprocesses the 311 service requests data to create dashboard_data.csv
    with monthly average response times by zipcode for 2024 data only.
    """
    # Load the data in chunks to handle large file size
    chunk_size = 50000
    chunks = []
    
    # Read the CSV file in chunks with progress bar
    csv_reader = pd.read_csv('311_Service_Requests_from_2010_to_Present_20250928.csv', 
                             chunksize=chunk_size, low_memory=False)
    
    print("Processing 311 service requests data...")
    for chunk in tqdm(csv_reader, desc="Processing chunks"):
        
        # Filter for 2024 data only and closed incidents
        chunk['Created Date'] = pd.to_datetime(chunk['Created Date'], errors='coerce')
        chunk['Closed Date'] = pd.to_datetime(chunk['Closed Date'], errors='coerce')
        
        # Filter for 2024 data
        chunk_2024 = chunk[chunk['Created Date'].dt.year == 2024]
        
        # Only include closed incidents (non-null Closed Date)
        chunk_2024_closed = chunk_2024.dropna(subset=['Closed Date'])
        
        # Filter out rows with invalid or missing zip codes
        chunk_2024_closed = chunk_2024_closed.dropna(subset=['Incident Zip'])
        chunk_2024_closed = chunk_2024_closed[chunk_2024_closed['Incident Zip'].astype(str).str.len() == 5]
        
        if len(chunk_2024_closed) > 0:
            chunks.append(chunk_2024_closed[['Created Date', 'Closed Date', 'Incident Zip']])
    
    if not chunks:
        print("No relevant data found for 2024!")
        return
    
    # Combine all chunks
    print("\nCombining chunks...")
    df_2024 = pd.concat(chunks, ignore_index=True)
    
    print(f"Total 2024 closed incidents: {len(df_2024):,}")
    
    # Calculate response time in hours
    df_2024['response_time_hours'] = (df_2024['Closed Date'] - df_2024['Created Date']).dt.total_seconds() / 3600
    
    # Remove negative response times (data quality issues)
    df_2024 = df_2024[df_2024['response_time_hours'] >= 0]
    
    # Create month column
    df_2024['month'] = df_2024['Created Date'].dt.to_period('M')
    
    # Clean zipcode column
    df_2024['zipcode'] = df_2024['Incident Zip'].astype(str).str.zfill(5)
    
    print("Calculating monthly averages by zipcode...")
    
    # Calculate monthly average response time by zipcode
    tqdm.pandas(desc="Calculating averages")
    monthly_avg = df_2024.groupby(['month', 'zipcode'])['response_time_hours'].agg([
        'mean', 'count'
    ]).reset_index()
    
    # Rename columns
    monthly_avg.columns = ['month', 'zipcode', 'avg_response_time_hours', 'incident_count']
    
    # Convert month back to datetime for easier plotting
    monthly_avg['month'] = monthly_avg['month'].dt.to_timestamp()
    
    # Filter out zipcodes with very few incidents (less than 5 per month on average)
    zipcode_counts = monthly_avg.groupby('zipcode')['incident_count'].sum()
    valid_zipcodes = zipcode_counts[zipcode_counts >= 60].index  # At least 60 incidents total in 2024
    monthly_avg = monthly_avg[monthly_avg['zipcode'].isin(valid_zipcodes)]
    
    # Also calculate overall monthly averages (for the "All 2024" line)
    overall_monthly = df_2024.groupby('month')['response_time_hours'].mean().reset_index()
    overall_monthly['zipcode'] = 'ALL'
    overall_monthly.columns = ['month', 'avg_response_time_hours', 'zipcode']
    overall_monthly['month'] = overall_monthly['month'].dt.to_timestamp()
    overall_monthly = overall_monthly[['month', 'zipcode', 'avg_response_time_hours']]
    
    # Combine zipcode-specific and overall data
    final_data = pd.concat([
        monthly_avg[['month', 'zipcode', 'avg_response_time_hours']], 
        overall_monthly
    ], ignore_index=True)
    
    # Save to CSV
    print("Saving dashboard_data.csv...")
    final_data.to_csv('dashboard_data.csv', index=False)
    
    print(f"Dashboard data saved with {len(final_data):,} records")
    print(f"Number of valid zipcodes: {len(valid_zipcodes)}")
    print(f"Date range: {final_data['month'].min().strftime('%Y-%m')} to {final_data['month'].max().strftime('%Y-%m')}")
    
    # Print some sample data
    print("\nSample data:")
    print(final_data.head(10))
    
    print("\nZipcodes available:")
    zipcodes = sorted(final_data[final_data['zipcode'] != 'ALL']['zipcode'].unique())
    print(f"First 10 zipcodes: {zipcodes[:10]}")

if __name__ == "__main__":
    preprocess_311_data()