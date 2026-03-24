import React from 'react';
import { useApp } from '../context/AppContext';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell, ReferenceLine } from 'recharts';
import { BarChart2, Star, MapPin } from 'lucide-react';

export default function MarketComparison() {
  const { selectedCrop, setSelectedCrop, selectedMarket, crops, getMarketComparison, t } = useApp();
  
  const comparisonData = getMarketComparison().sort((a, b) => b.marketPrice - a.marketPrice);
  const bestMkt = comparisonData[0];

  // Helper for mock distance/ratings for Vadodara region
  const getDist = (mkt) => {
    const dMap = { 'Vadodara': 10, 'Padra': 20, 'Savli': 35, 'Karjan': 40, 'Waghodia': 15, 'Dabhoi': 30, 'Shinor': 55 };
    return dMap[mkt] || 25;
  };
  const getRat = (mkt) => {
    const rMap = { 'Vadodara': 4.8, 'Padra': 4.2, 'Savli': 4.3, 'Karjan': 4.0, 'Waghodia': 4.5, 'Dabhoi': 4.1, 'Shinor': 3.9 };
    return rMap[mkt] || 4.0;
  };

  const chartData = comparisonData.map(d => ({
    name: d.marketName,
    price: d.marketPrice,
    msp: d.msp,
    isSelected: d.marketName === selectedMarket
  }));

  return (
    <div className="flex-1 bg-[#F8FAFC] p-8 overflow-y-auto">
      {/* Header */}
      <div className="mb-8 items-start flex flex-col">
        <h1 className="text-3xl font-extrabold text-slate-900 flex items-center gap-3">
          <BarChart2 className="text-[#2F7D4A]" /> {t('market_compare.title')}
        </h1>
        <p className="text-slate-500 mt-1">{t('market_compare.subtitle')}</p>
      </div>

      {/* Selectors Section */}
      <div className="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm mb-8 flex flex-wrap gap-6 items-end">
        <div className="flex-1 min-w-[200px]">
          <label className="block text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">🌿 {t('market_compare.select_crop')}</label>
          <select 
            value={selectedCrop}
            onChange={(e) => setSelectedCrop(e.target.value)}
            className="w-full p-3 bg-slate-50 border border-slate-200 rounded-xl focus:ring-2 focus:ring-[#2f7d4a] focus:border-transparent outline-none transition-all font-semibold text-slate-700"
          >
            {crops.map(crop => <option key={crop} value={crop}>{crop}</option>)}
          </select>
        </div>
      </div>

      {/* Best Price Card */}
      {bestMkt && (
        <div className="bg-[#DCFCE7] border border-[#BBF7D0] rounded-2xl p-6 flex items-center justify-between mb-8 shadow-sm">
          <div className="flex items-center gap-6">
            <div className="w-12 h-12 bg-[#BBF7D0] text-[#15803D] rounded-full flex items-center justify-center text-2xl">★</div>
            <div>
              <p className="text-[11px] font-bold text-[#166534] uppercase tracking-wider mb-1">{t('market_compare.best_price_at')}</p>
              <h2 className="text-xl font-black text-[#14532D]">{bestMkt.marketName} {t('market_compare.mandi')}</h2>
              <p className="text-lg font-black text-[#16A34A] mt-1">₹{bestMkt.marketPrice.toLocaleString()}/quintal</p>
            </div>
          </div>
          <div className="text-right">
             <p className="text-[11px] text-slate-500 font-bold uppercase tracking-wider">{t('market_compare.distance')}</p>
             <p className="text-lg font-bold text-slate-800">{getDist(bestMkt.marketName)} km</p>
          </div>
        </div>
      )}

      {/* Price Comparison Chart Section */}
      <div className="bg-white rounded-3xl border border-slate-100 shadow-md p-8 mb-10 overflow-hidden">
        <div className="flex items-center justify-between mb-10">
          <div className="flex items-center gap-3">
             <BarChart2 size={24} className="text-[#2F7D4A]" />
             <h3 className="font-extrabold text-slate-800 text-xl tracking-tight">{t('market_compare.distribution_title')}</h3>
          </div>
          <div className="flex items-center gap-6">
             <div className="flex items-center gap-2 small-caps font-bold text-slate-400 text-xs">
                <div className="w-3 h-3 bg-[#2F7D4A] rounded-sm"></div> {t('market_compare.legend_price')}
             </div>
             <div className="flex items-center gap-2 small-caps font-bold text-blue-500 text-xs">
                <div className="w-3 h-3 border-2 border-blue-500 border-dashed rounded-sm"></div> {t('market_compare.legend_msp')}
             </div>
          </div>
        </div>

        <div className="h-[450px] w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={chartData} margin={{ top: 20, right: 30, left: 20, bottom: 60 }}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#F1F5F9" />
                <XAxis 
                    dataKey="name" 
                    axisLine={false} 
                    tickLine={false} 
                    tick={{fill: '#475569', fontSize: 12, fontWeight: 800}}
                    angle={-25}
                    textAnchor="end"
                    dy={16}
                />
                <YAxis 
                    axisLine={false} 
                    tickLine={false} 
                    tick={{fill: '#94A3B8', fontSize: 12, fontWeight: 700}}
                    tickFormatter={(val) => `₹${val}`}
                />
                <Tooltip 
                    cursor={{fill: '#F8FAFC'}}
                    contentStyle={{ borderRadius: '16px', border: 'none', boxShadow: '0 10px 15px -3px rgb(0 0 0 / 0.1)', padding: '16px' }}
                    labelStyle={{ fontWeight: 800, color: '#1E293B', marginBottom: '8px', fontSize: '14px' }}
                />
                <Bar dataKey="price" radius={[8, 8, 0, 0]} barSize={45}>
                  {chartData.map((entry, index) => (
                    <Cell 
                        key={`cell-${index}`} 
                        fill={entry.isSelected ? '#15803D' : '#4ADE80'} 
                        stroke={entry.isSelected ? '#14532D' : 'none'}
                        strokeWidth={2}
                    />
                  ))}
                </Bar>
                {/* Horizontal reference line for MSP - typically same for all markets for a crop */}
                {chartData.length > 0 && (
                   <ReferenceLine y={chartData[0].msp} stroke="#3B82F6" strokeDasharray="5 5" strokeWidth={2} label={{ position: 'right', value: 'MSP', fill: '#3B82F6', fontSize: 10, fontWeight: 900 }} />
                )}
              </BarChart>
            </ResponsiveContainer>
        </div>
      </div>

      {/* Comparison Table */}
      <div className="bg-white rounded-2xl border border-slate-100 shadow-sm overflow-hidden mb-8">
        <div className="p-6 border-b border-slate-100 flex items-center gap-3">
           <MapPin size={18} className="text-[#2F7D4A]" />
           <span className="font-bold text-slate-800">Detailed Market Prices</span>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full border-collapse">
            <thead>
              <tr className="bg-slate-50">
                <th className="px-6 py-4 text-left text-xs font-bold text-slate-400 uppercase tracking-widest">{t('market_compare.table_market')}</th>
                <th className="px-6 py-4 text-left text-xs font-bold text-slate-400 uppercase tracking-widest">{t('market_compare.table_price')}</th>
                <th className="px-6 py-4 text-left text-xs font-bold text-slate-400 uppercase tracking-widest">{t('market_compare.table_dist')}</th>
                <th className="px-6 py-4 text-left text-xs font-bold text-slate-400 uppercase tracking-widest">{t('market_compare.table_rating')}</th>
              </tr>
            </thead>
            <tbody>
              {comparisonData.map((row, idx) => {
                const isBest = row.marketName === bestMkt.marketName;
                const isSelected = row.marketName === selectedMarket;
                
                return (
                  <tr key={idx} className={`border-b border-slate-100 hover:bg-slate-50 transition-colors ${isBest ? 'bg-green-50/30' : ''}`}>
                    <td className="px-6 py-4 font-bold text-slate-800 flex items-center gap-3">
                       {isBest && <span className="bg-[#DCFCE7] text-[#166534] px-2 py-0.5 rounded text-[10px] font-black uppercase tracking-tighter">{t('market_compare.best')}</span>}
                       {isSelected && <span className="w-2 h-2 bg-[#2f7d4a] rounded-full"></span>}
                       {row.marketName} {t('market_compare.mandi')}
                    </td>
                    <td className={`px-6 py-4 font-black ${isBest ? 'text-[#16A34A]' : 'text-slate-700'}`}>₹{row.marketPrice.toLocaleString()}</td>
                    <td className="px-6 py-4 text-sm text-slate-400 font-bold">{getDist(row.marketName)} km</td>
                    <td className="px-6 py-4 flex items-center gap-1.5 font-bold text-slate-700">
                      <Star size={14} className="text-yellow-500 fill-current" /> {getRat(row.marketName)}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
      
      {/* Footer Insight */}
      <div className="p-6 bg-white rounded-2xl border-l-4 border-yellow-500 shadow-sm flex gap-6 items-start">
        <div className="text-2xl pt-1 shrink-0">💡</div>
        <div>
          <h4 className="font-bold text-slate-900">{t('market_compare.insight_title')}</h4>
          <p className="text-sm text-slate-500 leading-relaxed">
            {t('market_compare.insight_text').replace('{market}', bestMkt?.marketName).replace('{dist}', getDist(bestMkt?.marketName))}
          </p>
        </div>
      </div>
    </div>
  );
}
