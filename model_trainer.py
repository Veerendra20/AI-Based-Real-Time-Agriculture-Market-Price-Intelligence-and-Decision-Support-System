import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import joblib
from data_processor import load_and_clean_data

def train_model(data_path):
    """
    Train the price prediction model using the new Vadodara regional schema.
    """
    df = load_and_clean_data(data_path)
    
    # Feature Engineering
    le_crop = LabelEncoder()
    le_market = LabelEncoder()
    
    df['Crop_Encoded'] = le_crop.fit_transform(df['Crop Name'])
    df['Market_Encoded'] = le_market.fit_transform(df['Market Name'])
    
    # Extract date features
    df['Day'] = df['Date'].dt.day
    df['Month'] = df['Date'].dt.month
    df['Year'] = df['Date'].dt.year
    
    X = df[['Crop_Encoded', 'Market_Encoded', 'Day', 'Month', 'Year']]
    y = df['Market Price']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Random Forest Regressor for price forecasting
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Save model and encoders with new naming convention
    joblib.dump(model, 'price_model.joblib')
    joblib.dump(le_crop, 'le_crop.joblib')
    joblib.dump(le_market, 'le_market.joblib')
    
    print("Regional price model trained and saved successfully!")
    print(f"Test Accuracy Score: {model.score(X_test, y_test):.4f}")

if __name__ == "__main__":
    train_model('mandi_data.csv')
