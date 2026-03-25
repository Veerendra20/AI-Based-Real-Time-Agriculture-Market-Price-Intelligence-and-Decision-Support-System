# FarmPrice: AI-Powered Agriculture Decision Support System

FarmPrice is a comprehensive, real-time intelligence platform designed to empower farmers with actionable data. The system combines machine learning for price prediction with traditional market analysis to provide a full-spectrum decision support tool.

## 🌟 Key Features

### 📊 Real-Time Market Intelligence
- **Price Comparison:** Compare crop prices across various regional mandis (markets).
- **MSP Benchmarking:** Automatic comparison of market rates against Government Minimum Support Price (MSP).
- **Profit/Loss Analysis:** Identify the best markets to sell based on real-time price distribution.

### 📈 AI price Prediction
- **Neural Network Models:** Predict future price trends based on historical data.
- **Harvest Advisor:** Strategic guidance on the best time to sell or hold crops.
- **Risk Assessment:** Low/High risk indicators for market volatility.

### 🌿 Smart Farming Utils
- **Fertilizer Calculator:** N-P-K based recommendations for optimized crop yield.
- **Support Portal:** Direct access to Government schemes, insurance, and farming guidance.
- **Multi-Language:** Full support for **English**, **Gujarati (ગુજરાતી)**, and **Hindi (हिंदी)**.

## 🛠️ Technology Stack

- **Streamlit (Python):** Native, high-performance data dashboard.
- **React (Vite):** Modern, responsive SaaS-style frontend.
- **Scikit-Learn:** Machine learning backend for price forecasting.
- **TailwindCSS:** Sleek design system integrated into both Streamlit and React components.

## 🚀 Getting Started

### Prerequisites
- Python 3.9+ 
- Node.js (for React frontend)

### 1. Run the Streamlit Dashboard
```bash
# Install dependencies
pip install -r requirements.txt

# Launch the app
streamlit run app.py
```

### 2. Run the React Frontend
```bash
cd frontend
npm install
npm run dev
```

## 📂 Project Structure

- `app.py`: Main entry point for the Streamlit application.
- `frontend/`: Source code for the modern React dashboard.
- `data_processor.py`: Core logic for data handling and cleaning.
- `mandi_data.csv`: Real-time market data repository.
- `price_model.joblib`: Pre-trained AI model for price forecasting.
- `sync_react_data.py`: Utility to synchronize CSV data with the React frontend.

## 🌍 Localization
The application is built for accessibility. All components are dynamically translated using the centralized translation engine, ensuring that vital farming data is accessible in regional languages.

---
Built with ❤️ for Farmers Excellence | © 2026 FarmPrice