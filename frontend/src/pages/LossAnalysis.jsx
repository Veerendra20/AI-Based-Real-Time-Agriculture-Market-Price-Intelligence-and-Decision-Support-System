import React, { useState } from 'react';
import { useApp } from '../context/AppContext';
import { Calculator, AlertTriangle, CheckCircle2, IndianRupee } from 'lucide-react';

export default function LossAnalysis() {
  const { selectedCrop, setSelectedCrop, crops, selectedMarket, setSelectedMarket, markets, getStats } = useApp();
  const [userPrice, setUserPrice] = useState("");
  const [quantity, setQuantity] = useState(10);
  
  const stats = getStats();
  const mktPrice = stats.marketPrice;
  const msp = stats.msp;

  const handleCalculate = () => {
    if (!userPrice) return null;
    const price = parseFloat(userPrice);
    const lossPerQ = mktPrice - price;
    const totalLoss = lossPerQ * quantity;
    return { lossPerQ, totalLoss, isLoss: lossPerQ > 0 };
  };

  const result = handleCalculate();

  return (
    <div className="flex-1 bg-[#F8FAFC] p-8 overflow-y-auto">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-extrabold text-slate-900 flex items-center gap-3">
          <Calculator className="text-[#2F7D4A]" /> Farmer Loss Analysis
        </h1>
        <p className="text-slate-500 mt-1">Calculate potential losses and compare your selling price with market rates</p>
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
          <label className="block text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">📍 Market Benchmark</label>
          <select 
            value={selectedMarket}
            onChange={(e) => setSelectedMarket(e.target.value)}
            className="w-full p-3 bg-slate-50 border border-slate-200 rounded-xl focus:ring-2 focus:ring-[#2f7d4a] focus:border-transparent outline-none transition-all font-semibold text-slate-700"
          >
            {markets.map(mkt => <option key={mkt} value={mkt}>{mkt}</option>)}
          </select>
        </div>
      </div>

      {/* Input Section */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-10">
        <div className="bg-white p-8 rounded-3xl border border-slate-100 shadow-sm">
           <div className="flex items-center gap-3 mb-8">
              <div className="w-10 h-10 bg-green-50 text-[#2f7d4a] rounded-full flex items-center justify-center font-bold">₹</div>
              <h3 className="font-extrabold text-slate-800 text-xl tracking-tight">Your Selling Price</h3>
           </div>
           
           <div className="space-y-6">
              <div>
                 <label className="block text-[11px] font-black text-slate-400 uppercase tracking-widest mb-3">PRICE PER QUINTAL (₹)</label>
                 <div className="relative group">
                    <span className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 font-bold group-focus-within:text-[#2f7d4a]">₹</span>
                    <input 
                      type="number" 
                      placeholder="Enter price" 
                      value={userPrice}
                      onChange={(e) => setUserPrice(e.target.value)}
                      className="w-full pl-10 pr-4 py-4 bg-slate-50 border border-slate-200 rounded-2xl focus:ring-2 focus:ring-[#2f7d4a] focus:border-transparent outline-none transition-all font-extrabold text-xl text-slate-800"
                    />
                 </div>
              </div>
              
              <div>
                 <label className="block text-[11px] font-black text-slate-400 uppercase tracking-widest mb-3">TOTAL QUANTITY (QUINTALS)</label>
                 <input 
                    type="number" 
                    value={quantity}
                    onChange={(e) => setQuantity(e.target.value)}
                    className="w-full px-6 py-4 bg-slate-50 border border-slate-200 rounded-2xl focus:ring-2 focus:ring-[#2f7d4a] focus:border-transparent outline-none transition-all font-extrabold text-xl text-slate-800"
                 />
              </div>
           </div>
        </div>

        {/* Current Market Price Reference Card */}
        <div className="bg-white p-8 rounded-3xl border border-slate-100 shadow-sm flex flex-col justify-between">
           <div>
              <div className="flex items-center gap-3 mb-8">
                 <div className="w-10 h-10 bg-blue-50 text-blue-600 rounded-full flex items-center justify-center font-bold italic">M</div>
                 <h3 className="font-extrabold text-slate-800 text-xl tracking-tight">Market Benchmarks</h3>
              </div>
              <div className="space-y-6">
                 <div className="p-5 bg-green-50/50 rounded-2xl border border-green-100/50">
                    <p className="text-[10px] font-black text-green-700 uppercase tracking-widest mb-1 opacity-70">Today's Market Price</p>
                    <p className="text-3xl font-black text-green-900">₹{mktPrice.toLocaleString()}<span className="text-sm font-bold opacity-40 ml-1">/q</span></p>
                 </div>
                 <div className="p-5 bg-blue-50/50 rounded-2xl border border-blue-100/50">
                    <p className="text-[10px] font-black text-blue-700 uppercase tracking-widest mb-1 opacity-70">Government MSP</p>
                    <p className="text-3xl font-black text-blue-900">₹{msp.toLocaleString()}<span className="text-sm font-bold opacity-40 ml-1">/q</span></p>
                 </div>
              </div>
           </div>
        </div>
      </div>

      {/* Results Section */}
      {result && (
        <div className={`rounded-3xl p-10 shadow-xl border-2 mb-10 transition-all transform animate-in slide-in-from-bottom-4 duration-500 ${result.isLoss ? 'bg-red-50 border-red-200' : 'bg-green-50 border-green-200'}`}>
           <div className="flex flex-col md:flex-row items-center gap-10">
              <div className={`w-24 h-24 rounded-full flex items-center justify-center text-4xl shadow-md shrink-0 ${result.isLoss ? 'bg-red-100 text-red-600' : 'bg-green-100 text-green-600'}`}>
                 {result.isLoss ? <AlertTriangle size={48} /> : <CheckCircle2 size={48} />}
              </div>
              <div className="flex-1 text-center md:text-left">
                 <h2 className={`text-4xl font-black mb-2 ${result.isLoss ? 'text-red-900' : 'text-green-900'}`}>
                    {result.isLoss ? `You are losing ₹${Math.abs(result.lossPerQ).toLocaleString()} per quintal` : `You are earning ₹${Math.abs(result.lossPerQ).toLocaleString()} extra! ✨`}
                 </h2>
                 <p className={`text-xl font-bold ${result.isLoss ? 'text-red-700' : 'text-green-700'}`}>
                    {result.isLoss ? 'Strong Advice: Wait for prices to reach MSP or sell at government mandis.' : 'Great Job: Your selling price is excellent compared to the market average.'}
                 </p>
                 <div className="mt-8 flex flex-col md:flex-row gap-6">
                    <div className="bg-white/80 backdrop-blur-md px-8 py-5 rounded-2xl shadow-sm border border-white">
                        <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1">Total Impact</p>
                        <p className={`text-3xl font-black ${result.isLoss ? 'text-red-600' : 'text-green-600'}`}>
                          {result.isLoss ? '-' : '+'} ₹{Math.abs(result.totalLoss).toLocaleString()}
                        </p>
                    </div>
                 </div>
              </div>
           </div>
        </div>
      )}

      {/* Warning Alert */}
      {!result && (
        <div className="bg-yellow-50 border border-yellow-200 p-6 rounded-2xl flex gap-6 items-center shadow-sm">
           <div className="text-2xl bg-white w-12 h-12 shadow-sm flex items-center justify-center rounded-xl shrink-0">⚠️</div>
           <div>
             <p className="text-yellow-900 font-black">Calculation Pending</p>
             <p className="text-sm text-yellow-700 font-medium leading-relaxed">Please enter your selling price above to see how it compares with the current market benchmarks and MSP.</p>
           </div>
        </div>
      )}
    </div>
  );
}
