import React from 'react';
import { useApp } from '../context/AppContext';
import { LayoutDashboard, TrendingUp, ShieldCheck, AlertCircle } from 'lucide-react';

export default function Dashboard() {
  const { selectedCrop, setSelectedCrop, selectedMarket, setSelectedMarket, crops, markets, getStats, t } = useApp();
  
  const stats = getStats();
  const priceDiff = stats.marketPrice - stats.msp;
  const isAboveMSP = priceDiff >= 0;

  return (
    <div className="flex-1 bg-[#F8FAFC] p-8 overflow-y-auto">
      {/* Header Section */}
      <div className="mb-8">
        <h1 className="text-3xl font-extrabold text-slate-900 flex items-center gap-3">
          {t('dashboard.greeting')} <span className="text-2xl">🌾</span>
        </h1>
        <p className="text-slate-500 mt-1">{t('dashboard.subtitle')}</p>
      </div>

      {/* Selectors Section */}
      <div className="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm mb-8 flex flex-wrap gap-6 items-end">
        <div className="flex-1 min-w-[200px]">
          <label className="block text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">🌿 {t('dashboard.select_crop')}</label>
          <select 
            value={selectedCrop}
            onChange={(e) => setSelectedCrop(e.target.value)}
            className="w-full p-3 bg-slate-50 border border-slate-200 rounded-xl focus:ring-2 focus:ring-[#2f7d4a] focus:border-transparent outline-none transition-all font-semibold text-slate-700"
          >
            {crops.map(crop => <option key={crop} value={crop}>{crop}</option>)}
          </select>
        </div>
        <div className="flex-1 min-w-[200px]">
          <label className="block text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">📍 {t('dashboard.select_market')}</label>
          <select 
            value={selectedMarket}
            onChange={(e) => setSelectedMarket(e.target.value)}
            className="w-full p-3 bg-slate-50 border border-slate-200 rounded-xl focus:ring-2 focus:ring-[#2f7d4a] focus:border-transparent outline-none transition-all font-semibold text-slate-700"
          >
            {markets.map(mkt => <option key={mkt} value={mkt}>{mkt}</option>)}
          </select>
        </div>
      </div>

      {/* KPI Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">
        {/* Market Price Card */}
        <div className="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm relative overflow-hidden group">
          <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
            <LayoutDashboard size={48} />
          </div>
          <div className="w-10 h-10 bg-green-50 text-[#2f7d4a] rounded-full flex items-center justify-center mb-4">
            <TrendingUp size={20} />
          </div>
          <p className="text-xs font-bold text-slate-400 uppercase tracking-widest mb-1">{t('dashboard.market_price')}</p>
          <h2 className="text-3xl font-black text-slate-900">₹{stats.marketPrice.toLocaleString()}<span className="text-sm font-bold text-slate-400 ml-1">/q</span></h2>
          <p className="text-xs text-slate-500 mt-2 font-medium">{selectedMarket} {t('dashboard.mandi')}</p>
          {isAboveMSP && <div className="absolute top-6 right-6 px-2 py-1 bg-green-100 text-green-700 rounded-lg text-[10px] font-black uppercase tracking-tighter">{t('dashboard.profit')}</div>}
        </div>

        {/* MSP Card */}
        <div className="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm relative overflow-hidden group">
          <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
            <ShieldCheck size={48} />
          </div>
          <div className="w-10 h-10 bg-blue-50 text-blue-600 rounded-full flex items-center justify-center mb-4 text-xl font-bold">₹</div>
          <p className="text-xs font-bold text-slate-400 uppercase tracking-widest mb-1">{t('dashboard.msp')}</p>
          <h2 className="text-3xl font-black text-slate-900">₹{stats.msp.toLocaleString()}<span className="text-sm font-bold text-slate-400 ml-1">/q</span></h2>
          <p className="text-xs text-slate-500 mt-2 font-medium">{t('dashboard.support')}</p>
        </div>

        {/* Price Diff Card */}
        <div className={`p-6 rounded-2xl border shadow-sm relative overflow-hidden group ${isAboveMSP ? 'bg-white border-slate-100' : 'bg-red-50/50 border-red-100'}`}>
          <div className="w-10 h-10 bg-slate-50 rounded-full flex items-center justify-center mb-4">
             {isAboveMSP ? <ShieldCheck size={20} className="text-green-600" /> : <AlertCircle size={20} className="text-red-500" />}
          </div>
          <p className="text-xs font-bold text-slate-400 uppercase tracking-widest mb-1">{t('dashboard.price_diff')}</p>
          <h2 className={`text-3xl font-black ${isAboveMSP ? 'text-green-600' : 'text-red-500'}`}>
            {isAboveMSP ? '+' : ''}₹{priceDiff.toLocaleString()}<span className="text-sm font-bold opacity-60 ml-1">/q</span>
          </h2>
          <p className={`text-xs mt-2 font-bold ${isAboveMSP ? 'text-green-600' : 'text-red-500'}`}>
            {isAboveMSP ? t('dashboard.above_msp') : t('dashboard.below_msp')}
          </p>
        </div>
      </div>

      {/* Farming Tip Footer */}
      <div className="bg-white p-6 rounded-2xl border-l-4 border-green-600 shadow-sm flex gap-6 items-center">
        <div className="text-2xl bg-green-50 w-12 h-12 flex items-center justify-center rounded-xl shrink-0">💡</div>
        <div>
          <h4 className="font-bold text-slate-900">{t('dashboard.tip_title')}</h4>
          <p className="text-sm text-slate-500 leading-relaxed">
            {t('dashboard.tip_text').replace('{crop}', selectedCrop).replace('{market}', selectedMarket)}
          </p>
        </div>
      </div>
    </div>
  );
}
