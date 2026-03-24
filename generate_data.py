import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Markets in Vadodara region (User specified)
markets = ['Waghodia', 'Vadodara', 'Padra', 'Dabhoi', 'Karjan', 'Savli', 'Shinor']

# Crops and their associated Price/MSP ranges (Refined based on Price_Agriculture_commodities_Week.csv)
commodities = {
    'Tomato': {'msp': 1500, 'min_p': 8500, 'max_p': 11500},
    'Onion': {'msp': 1200, 'min_p': 1000, 'max_p': 2200},
    'Chilli': {'msp': 4500, 'min_p': 4000, 'max_p': 8500},
    'Cotton': {'msp': 6620, 'min_p': 5500, 'max_p': 7500},
    'Potato': {'msp': 1000, 'min_p': 800, 'max_p': 1800}
}

data = []
start_date = datetime(2025, 1, 1)

# Generate 1000 records for better ML training
for i in range(1000):
    market = np.random.choice(markets)
    crop_name = np.random.choice(list(commodities.keys()))
    date = start_date + timedelta(days=np.random.randint(0, 120))
    
    info = commodities[crop_name]
    # Randomized Market Price around the MSP with some seasonal/random variance
    market_price = np.random.randint(info['min_p'], info['max_p'])
    
    data.append({
        'Crop Name': crop_name,
        'Market Name': market,
        'Date': date.strftime('%d/%m/%Y'),
        'Market Price': market_price,
        'MSP': info['msp']
    })

df = pd.DataFrame(data)
df.to_csv('mandi_data.csv', index=False)
print(f"Localized Vadodara data generated: mandi_data.csv ({len(df)} records)")
