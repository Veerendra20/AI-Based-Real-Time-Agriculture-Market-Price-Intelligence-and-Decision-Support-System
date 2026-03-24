import React, { createContext, useState, useContext } from 'react';
import { farmData, crops, markets, priceHistory } from '../data/farmData';
import { translations } from '../data/translations';

const AppContext = createContext();

export const AppProvider = ({ children }) => {
  const [language, setLanguage] = useState('en');
  const [selectedCrop, setSelectedCrop] = useState(crops[4]); // Default: Tomato
  const [selectedMarket, setSelectedMarket] = useState(markets[5]); // Default: Vadodara

  // Translation helper
  const t = (path) => {
    const keys = path.split('.');
    let result = translations[language];
    for (const key of keys) {
      if (result[key]) {
        result = result[key];
      } else {
        return path; // Fallback to path if key missing
      }
    }
    return result;
  };

  // Helper to get stats for the current selection
  const getStats = (crop = selectedCrop, market = selectedMarket) => {
    return farmData.find(d => d.cropName === crop && d.marketName === market) || { marketPrice: 0, msp: 0 };
  };

  // Helper to get all market data for a crop
  const getMarketComparison = (crop = selectedCrop) => {
    const list = farmData.filter(d => d.cropName === crop);
    // Ensure the selected market is included even if it's missing in filtered list (fallback)
    return list.length > 0 ? list : [{ cropName: crop, marketName: 'Vadodara', marketPrice: 0, msp: 0 }];
  };

  const getPriceHistory = (crop = selectedCrop) => {
    return priceHistory[crop] || [];
  };

  return (
    <AppContext.Provider value={{ 
      language,
      setLanguage,
      t,
      selectedCrop, 
      setSelectedCrop, 
      selectedMarket, 
      setSelectedMarket,
      getStats,
      getMarketComparison,
      getPriceHistory,
      crops,
      markets
    }}>
      {children}
    </AppContext.Provider>
  );
};

// eslint-disable-next-line react-refresh/only-export-components
export const useApp = () => useContext(AppContext);
