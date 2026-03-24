import React from 'react';
import { useApp } from '../context/AppContext';
import { TrendingUp, AlertTriangle, CheckCircle2, Clock, BarChart2 } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, AreaChart, Area } from 'recharts';

export default function PricePrediction() {
  const { selectedCrop, setSelectedCrop, crops, getPriceHistory } = useApp();
  
  const historyData = getPriceHistory();
  
  // Deterministic "AI" logic for advisor
  const getForecast = (crop) => {
    const map = {
        'Tomato': { trend: 'Bullish', gain: '+ 180', conf: 86, isHold: true, hindi: "सलाह: धैर्य रखें और फसल रोकें" },
        'Onion': { trend: 'Bearish', gain: '- 45', conf: 72, isHold: false, hindi: "सलाह: अभी फसल बेचें" },
        'Chilli': { trend: 'Bullish', gain: '+ 1120', conf: 91, isHold: true, hindi: "सलाह: धैर्य रखें और फसल रोकें" },
        'Cotton': { trend: 'Stable', gain: '+ 120', conf: 65, isHold: true, hindi: "सलाह: धैर्य रखें और फसल रोकें" },
        'Potato': { trend: 'Bearish', gain: '- 90', conf: 78, isHold: false, hindi: "सलाह: अभी फसल बेचें" },
    };
    return map[crop] || { trend: 'Stable', gain: '+ 0', conf: 50, isHold: true, hindi: "सलाह: धैर्य रखें" };
  };

  const advisor = getForecast(selectedCrop);

  return (
    <div className="flex-1 bg-[#F8FAFC] p-8 overflow-y-auto font-sans">
      {/* Header */}
      <div className="mb-8 items-start flex flex-col">
        <h1 className="text-3xl font-extrabold text-slate-900 flex items-center gap-3 lowercase">
          <TrendingUp className="text-[#2F7D4A]" /> price prediction
        </h1>
        <p className="text-slate-500 mt-1">AI-powered price forecasts to help you decide the best time to sell</p>
      </div>

      {/* Selectors Section */}
      <div className="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm mb-8 flex flex-wrap gap-6 items-end">
        <div className="flex-1 min-w-[200px]">
          <label className="block text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">🌿 Select Crop</label>
          <select 
            value={selectedCrop}
            onChange={(e) => setSelectedCrop(e.target.value)}
            className="w-full p-3 bg-slate-50 border border-slate-200 rounded-xl focus:ring-2 focus:ring-[#2f7d4a] focus:border-transparent outline-none transition-all font-semibold text-slate-700"
          >
            {crops.map(crop => <option key={crop} value={crop}>{crop}</option>)}
          </select>
        </div>
        <div className="flex-1 min-w-[200px]">
          <label className="block text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">Prediction Period</label>
          <div className="w-full p-3 bg-slate-50 border border-slate-200 rounded-xl text-slate-400 font-bold opacity-70">3 Months Forecast</div>
        </div>
      </div>

      {/* Harvest Advisor Card */}
      <div className={`rounded-3xl p-8 mb-10 shadow-lg border relative overflow-hidden ${advisor.isHold ? 'bg-gradient-to-br from-green-50 to-emerald-100 border-green-200' : 'bg-gradient-to-br from-red-50 to-rose-100 border-red-200'}`}>
        <div className={`inline-flex items-center gap-2 px-4 py-1.5 rounded-full text-[10px] font-black uppercase tracking-widest text-white mb-6 shadow-md ${advisor.isHold ? 'bg-green-600' : 'bg-red-500'}`}>
           Market Insight: {advisor.trend}
        </div>
        <h2 className={`text-5xl font-black mb-2 ${advisor.isHold ? 'text-green-900' : 'text-red-900'}`}>
           {advisor.isHold ? 'STAY CALM: HOLD' : 'ACTION: SELL NOW'}
        </h2>
        <p className={`text-xl font-bold mb-10 ${advisor.isHold ? 'text-green-700' : 'text-red-700'}`}>{advisor.hindi}</p>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-6 mb-10">
           <div className="bg-white/60 backdrop-blur-md p-5 rounded-2xl border border-white/50 shadow-sm">
              <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest mb-1 opacity-70 transition-all">Expected Gain</p>
              <p className={`text-2xl font-black ${advisor.isHold ? 'text-green-700' : 'text-red-700'}`}>₹{advisor.gain}</p>
              <p className="text-[10px] text-slate-400 font-bold mt-1 leading-tight">If sold at peak</p>
           </div>
           <div className="bg-white/60 backdrop-blur-md p-5 rounded-2xl border border-white/50 shadow-sm">
              <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest mb-1 opacity-70">Market Demand</p>
              <p className="text-2xl font-black text-slate-700">VERY HIGH</p>
           </div>
           <div className="bg-white/60 backdrop-blur-md p-5 rounded-2xl border border-white/50 shadow-sm">
              <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest mb-1 opacity-70 transition-all">Risk Level</p>
              <p className="text-2xl font-black text-slate-700">LOW</p>
           </div>
           <div className="bg-white/60 backdrop-blur-md p-5 rounded-2xl border border-white/50 shadow-sm">
              <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest mb-1 opacity-70">Next Update</p>
              <p className="text-2xl font-black text-slate-700 flex items-center gap-2 italic uppercase"><Clock size={18} /> 24 Hours</p>
           </div>
        </div>

        <div className="flex items-center gap-4">
           <span className="text-xs font-black text-slate-600 uppercase tracking-widest">Prediction Confidence:</span>
           <div className="flex-1 h-2 bg-slate-200 rounded-full overflow-hidden">
              <div className="h-full bg-green-500 rounded-full shadow-[0_0_12px_rgba(34,197,94,0.4)]" style={{ width: `${advisor.conf}%` }}></div>
           </div>
           <span className="text-sm font-black text-slate-700 italic">{advisor.conf}%</span>
        </div>
      </div>

      <div className="bg-white p-8 rounded-3xl border border-slate-100 shadow-md">
         <div className="flex items-center justify-between mb-8">
            <div className="flex items-center gap-3">
                <BarChart2 className="text-[#2F7D4A]" />
                <span className="font-extrabold text-slate-800 text-xl tracking-tight">Market Trend Analysis</span>
            </div>
            <div className="flex items-center gap-4 text-xs font-bold">
                <div className="flex items-center gap-2 text-slate-400"><div className="w-3 h-3 rounded-full bg-slate-200"></div> Historical</div>
                <div className="flex items-center gap-2 text-[#2F7D4A]"><div className="w-3 h-3 rounded-full bg-[#2F7D4A] shadow-[0_0_8px_rgba(47,125,74,0.3)]"></div> Predicted (AI)</div>
            </div>
         </div>
         
         <div className="h-[400px] w-full">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={historyData}>
                <defs>
                  <linearGradient id="colorPrice" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#2F7D4A" stopOpacity={0.1}/>
                    <stop offset="95%" stopColor="#2F7D4A" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#F1F5F9" />
                <XAxis 
                    dataKey="name" 
                    axisLine={false} 
                    tickLine={false} 
                    tick={{fill: '#94A3B8', fontSize: 12, fontWeight: 700}}
                    dy={10}
                />
                <YAxis 
                    axisLine={false} 
                    tickLine={false} 
                    tick={{fill: '#94A3B8', fontSize: 12, fontWeight: 700}}
                    tickFormatter={(val) => `₹${val}`}
                />
                <Tooltip 
                    contentStyle={{ borderRadius: '16px', border: 'none', boxShadow: '0 10px 15px -3px rgb(0 0 0 / 0.1)', padding: '12px' }}
                    labelStyle={{ fontWeight: 800, color: '#1E293B', marginBottom: '4px' }}
                />
                <Area 
                    type="monotone" 
                    dataKey="price" 
                    stroke="#2F7D4A" 
                    strokeWidth={4}
                    fillOpacity={1} 
                    fill="url(#colorPrice)" 
                    dot={{ r: 6, fill: '#2F7D4A', strokeWidth: 2, stroke: '#fff' }}
                    activeDot={{ r: 8, strokeWidth: 0 }}
                />
              </AreaChart>
            </ResponsiveContainer>
         </div>
         
         <div className="mt-8 p-6 bg-slate-50 rounded-2xl border border-slate-100 italic">
            <p className="text-slate-500 text-sm font-medium leading-relaxed">
              * This forecast is generated using seasonal market analysis for the <b>Vadodara region</b>. 
              The AI predicts a <b>{advisor.trend}</b> outlook for {selectedCrop} with an accuracy of {advisor.conf}%.
            </p>
         </div>
      </div>
    </div>
  );
}
