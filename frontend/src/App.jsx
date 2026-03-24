import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Sidebar from './Sidebar';

// Import Pages
import Dashboard from './pages/Dashboard';
import MarketComparison from './pages/MarketComparison';
import PricePrediction from './pages/PricePrediction';
import Fertilizers from './pages/Fertilizers';
import LossAnalysis from './pages/LossAnalysis';
import SupportInfo from './pages/SupportInfo';

export default function App() {
  return (
    <Router>
      <div className="flex w-full min-h-screen bg-gray-100 font-sans antialiased text-gray-900">
        <Sidebar />
        
        {/* Main Content Area */}
        <div className="flex-1 flex flex-col bg-white overflow-y-auto">
          <Routes>
            <Route path="/" element={<Navigate to="/dashboard" replace />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/market-comparison" element={<MarketComparison />} />
            <Route path="/price-prediction" element={<PricePrediction />} />
            <Route path="/fertilizers" element={<Fertilizers />} />
            <Route path="/loss-analysis" element={<LossAnalysis />} />
            <Route path="/support-info" element={<SupportInfo />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}
