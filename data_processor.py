import pandas as pd
import numpy as np

def load_and_clean_data(file_path):
    """
    Step 1: Data Cleaning (Updated for Vadodara Regional Schema)
    """
    df = pd.read_csv(file_path)
    
    # Handle missing values
    df.dropna(inplace=True)
    
    # Convert Date to datetime
    df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)
    
    # Convert price columns to numeric
    for col in ['Market Price', 'MSP']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Drop rows with NaN prices
    df.dropna(subset=['Market Price', 'MSP'], inplace=True)
    
    return df

def get_market_analysis(df):
    """
    Step 2: Data Analysis - Market Comparison (Historical Average)
    """
    analysis = df.groupby(['Market Name', 'Crop Name'])['Market Price'].mean().reset_index()
    analysis = analysis.rename(columns={'Market Price': 'Avg Market Price'})
    return analysis

def get_latest_market_comparison(df, crop):
    """
    Extracts the latest market price for every market for a specific crop.
    This ensures the Comparison Chart matches the Dashboard's 'Latest Price'.
    """
    # Filter for crop
    crop_df = df[df['Crop Name'] == crop].copy()
    if crop_df.empty:
        return pd.DataFrame(columns=['Market Name', 'Latest Price'])
    
    # Get latest entry per market
    latest = crop_df.sort_values('Date', ascending=False).groupby('Market Name').head(1).reset_index()
    latest = latest.rename(columns={'Market Price': 'Latest Price'})
    return latest[['Market Name', 'Latest Price']]

def get_price_trends(df, crop):
    """
    Step 2: Data Analysis - Price Trends
    """
    trend_df = df[df['Crop Name'] == crop].sort_values('Date')
    return trend_df

def get_current_stats(df, crop, market=None):
    """
    Unified source of truth for the 'Current' price and MSP of a crop.
    If market is provided, filters for that market's latest entry.
    Otherwise, returns the latest crop entry across all markets.
    """
    if market:
        filtered = df[(df['Crop Name'] == crop) & (df['Market Name'] == market)]
    else:
        filtered = df[df['Crop Name'] == crop]
        
    if filtered.empty:
        # Final fallback to general crop data if market-specific is missing
        filtered = df[df['Crop Name'] == crop]
        
    if filtered.empty:
        return {'price': 0, 'msp': 0}
        
    # Always take the latest available date
    latest = filtered.sort_values('Date', ascending=False).iloc[0]
    return {
        'price': float(latest['Market Price']),
        'msp': float(latest['MSP'])
    }

if __name__ == "__main__":
    # Test cleaning
    try:
        df = load_and_clean_data('mandi_data.csv')
        print("Cleaned Data Shape:", df.shape)
        # Test unified stats
        crop = df['Crop Name'].unique()[0]
        stats = get_current_stats(df, crop)
        print(f"Stats for {crop}: {stats}")
    except Exception as e:
        print(f"Error: {e}")
