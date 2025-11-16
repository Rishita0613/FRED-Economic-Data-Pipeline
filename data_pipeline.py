import requests
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# --- MANDATORY CONFIGURATION ---
# IMPORTANT: You MUST obtain a FRED API Key and replace the placeholder below.
# A FRED API key is free and required to run this script.
# Go to: https://fred.stlouisfed.org/docs/api/api_key.html
FRED_API_KEY = "171921f6636080fe089f4bb1006b2c15"
BASE_URL = "https://api.stlouisfed.org/fred/series/observations"

# --- Economic Data Series IDs ---
# UNRATE: Civilian Unemployment Rate (Percent, Monthly, Seasonally Adjusted)
# PCEPI: Personal Consumption Expenditures Price Index (Monthly, Seasonally Adjusted)
SERIES_IDS = ['UNRATE', 'PCEPI']

def fetch_series_data(series_id, api_key):
    """Fetches a single economic time series from the FRED API."""
    params = {
        'series_id': series_id,
        'api_key': api_key,
        'file_type': 'json',
        'observation_start': '2000-01-01', # Starting data from Jan 1, 2000
        'sort_order': 'asc'
    }
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
        data = response.json()
        
        # Extract observations and convert to DataFrame
        observations = data.get('observations', [])
        df = pd.DataFrame(observations)
        
        # Rename columns and ensure correct data types
        df = df[['date', 'value']]
        df.columns = ['Date', series_id]
        
        # Convert 'value' to numeric, setting 'NaN' for missing/non-numeric values (e.g., '.')
        df[series_id] = pd.to_numeric(df[series_id], errors='coerce')
        df['Date'] = pd.to_datetime(df['Date'])
        
        return df.set_index('Date')
        
    except requests.exceptions.RequestException as e:
        print(f"ERROR: Failed to fetch data for {series_id}. Ensure your FRED API Key is valid and there is internet connectivity.")
        print(f"Details: {e}")
        return pd.DataFrame()

def run_pipeline():
    """Executes the data acquisition, cleaning, and visualization pipeline."""
    if FRED_API_KEY == "YOUR_FRED_API_KEY_HERE":
        print("CRITICAL ERROR: Please obtain a FRED API Key and update the 'FRED_API_KEY' variable in data_pipeline.py.")
        return

    print("--- Starting Economic Data Pipeline ---")
    
    # 1. Acquisition and Storage
    data_frames = []
    for series_id in SERIES_IDS:
        df = fetch_series_data(series_id, FRED_API_KEY)
        if not df.empty:
            data_frames.append(df)
            print(f"Status: Fetched {series_id} successfully.")
    
    if len(data_frames) < 2:
        print("Pipeline aborted: Could not fetch all required data series.")
        return

    # 2. Cleaning and Merging (Pandas Demonstration)
    # Merge on Date index and drop any rows with missing data (ensuring time alignment)
    merged_df = pd.concat(data_frames, axis=1, join='inner').dropna()
    print(f"\nCleaning Status: Data merged and NaN values dropped. Total observations: {merged_df.shape[0]}.")
    
    # 3. Visualization (Matplotlib Demonstration: Dual-Axis Plot)
    fig, ax1 = plt.subplots(figsize=(12, 6))

    # Plot Unemployment Rate (UNRATE) on the primary axis (ax1)
    color_unemp = 'teal'
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Unemployment Rate (%)', color=color_unemp, fontweight='bold')
    ax1.plot(merged_df.index, merged_df['UNRATE'], color=color_unemp, linewidth=2, label='Unemployment Rate')
    ax1.tick_params(axis='y', labelcolor=color_unemp)
    ax1.set_ylim(bottom=0)
    ax1.grid(True, linestyle='--', alpha=0.6, which='major', axis='y')

    # Instantiate a second axis (ax2) sharing the same x-axis for Inflation
    ax2 = ax1.twinx()  
    color_pce = 'firebrick'
    ax2.set_ylabel('PCE Price Index (Index Value)', color=color_pce, fontweight='bold')
    ax2.plot(merged_df.index, merged_df['PCEPI'], color=color_pce, linestyle='--', label='PCE Price Index')
    ax2.tick_params(axis='y', labelcolor=color_pce)

    # Format the x-axis to show years nicely
    formatter = mdates.DateFormatter('%Y')
    ax1.xaxis.set_major_formatter(formatter)
    
    # Improve Title and layout
    plt.title('US Labor Market (Unemployment) vs. Inflation (PCE Index) | 2000-Present', fontsize=14, fontweight='bold')
    fig.tight_layout() 
    
    # Save the figure to the repository for documentation
    plt.savefig('economic_comparison_plot.png')
    print("\nVisualization complete. Plot saved as 'economic_comparison_plot.png'.")
    plt.show()

if __name__ == "__main__":
    run_pipeline()