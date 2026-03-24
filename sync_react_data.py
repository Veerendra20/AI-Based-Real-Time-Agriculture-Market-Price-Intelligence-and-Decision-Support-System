import pandas as pd  # type: ignore
import json
import os

def sync_data():
    csv_path = 'mandi_data.csv'
    js_path = 'frontend/src/data/farmData.js'
    
    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} not found")
        return

    df = pd.read_csv(csv_path)
    # Convert Date to datetime for proper sorting
    df['Date'] = pd.to_datetime(df['Date'], dayfirst=True, errors='coerce')
    
    # Get latest entry for each (Crop, Market)
    latest_df = df.sort_values('Date').groupby(['Crop Name', 'Market Name']).tail(1)
    
    # Map to JS format
    js_data = []
    for _, row in latest_df.iterrows():
        js_data.append({
            "cropName": row['Crop Name'],
            "marketName": row['Market Name'],
            "date": row['Date'].strftime('%Y-%m-%d') if pd.notnull(row['Date']) else row['Date'],
            "marketPrice": int(row['Market Price']),
            "msp": int(row['MSP'])
        })
    
    crops = sorted(df['Crop Name'].unique().tolist())
    markets = sorted(df['Market Name'].unique().tolist())
    
    # Generate JS content
    content = f"export const farmData = {json.dumps(js_data, indent=2)};\n\n"
    content += f"export const crops = {json.dumps(crops)};\n"
    content += f"export const markets = {json.dumps(markets)};\n"
    content += "export const priceHistory = {};\n"
    
    with open(js_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Successfully synced {len(js_data)} records to {js_path}")

if __name__ == "__main__":
    sync_data()
