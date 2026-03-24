import React from 'react';
import { useApp } from '../context/AppContext';
import { Leaf, FlaskConical, Droplet, Sprout } from 'lucide-react';

export default function Fertilizers() {
  const { selectedCrop, setSelectedCrop, crops } = useApp();
  
  // Deterministic fertilizer data for the 5 localized crops
  const getNPK = (crop) => {
    const map = {
        'Tomato': { n: 120, p: 60, k: 60, tips: "Use calcium-rich fertilizers to prevent blossom end rot." },
        'Onion': { n: 100, p: 50, k: 50, tips: "Apply sulfur-based fertilizers for better pungency and bulb quality." },
        'Chilli': { n: 150, p: 75, k: 75, tips: "Ensure balanced NPK and micronutrients during flowering." },
        'Cotton': { n: 240, p: 60, k: 120, tips: "Split nitrogen applications during the square and boll formation stages." },
        'Potato': { n: 180, p: 100, k: 150, tips: "High potassium requirement for better tuber quality and starch content." },
    };
    return map[crop] || { n: 0, p: 0, k: 0, tips: "Consult local agriculture officers for guidance." };
  };

  const npk = getNPK(selectedCrop);

  return (
    <div className="flex-1 bg-[#F8FAFC] p-8 overflow-y-auto">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-extrabold text-slate-900 flex items-center gap-3">
          <Leaf className="text-[#2F7D4A]" /> Fertilizer Guide
        </h1>
        <p className="text-slate-500 mt-1">Smart recommendations for optimal crop yield in the Vadodara region</p>
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
          <label className="block text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">Soil Type</label>
          <div className="w-full p-3 bg-slate-50 border border-slate-200 rounded-xl text-slate-400 font-bold opacity-70">Black Soil (Typical Vadodara)</div>
        </div>
      </div>

      {/* NPK Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">
        <div className="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm text-center">
            <div className="w-12 h-12 bg-blue-50 text-blue-600 rounded-full flex items-center justify-center mx-auto mb-4"><FlaskConical fill="currentColor" fillOpacity="0.1" /></div>
            <p className="text-xs font-bold text-slate-400 uppercase tracking-widest mb-1">Nitrogen (N)</p>
            <h2 className="text-3xl font-black text-slate-900">{npk.n} <span className="text-sm font-bold text-slate-400">kg/ha</span></h2>
        </div>
        <div className="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm text-center">
            <div className="w-12 h-12 bg-pink-50 text-pink-600 rounded-full flex items-center justify-center mx-auto mb-4"><Droplet fill="currentColor" fillOpacity="0.1" /></div>
            <p className="text-xs font-bold text-slate-400 uppercase tracking-widest mb-1">Phosphorus (P)</p>
            <h2 className="text-3xl font-black text-slate-900">{npk.p} <span className="text-sm font-bold text-slate-400">kg/ha</span></h2>
        </div>
        <div className="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm text-center">
            <div className="w-12 h-12 bg-purple-50 text-purple-600 rounded-full flex items-center justify-center mx-auto mb-4"><Sprout fill="currentColor" fillOpacity="0.1" /></div>
            <p className="text-xs font-bold text-slate-400 uppercase tracking-widest mb-1">Potassium (K)</p>
            <h2 className="text-3xl font-black text-slate-900">{npk.k} <span className="text-sm font-bold text-slate-400">kg/ha</span></h2>
        </div>
      </div>

      <div className="bg-white p-8 rounded-3xl border border-slate-100 shadow-sm mb-10">
         <div className="flex items-center gap-3 mb-4">
            <h3 className="font-extrabold text-[#2F7D4A] flex items-center gap-2"><Leaf size={20} /> Expert Tips for {selectedCrop}</h3>
         </div>
         <p className="text-lg text-slate-600 font-medium leading-relaxed italic">"{npk.tips}"</p>
      </div>

      <div className="bg-[#eff6ff] border border-blue-100 p-6 rounded-2xl flex gap-6 items-center">
         <div className="text-2xl bg-white w-12 h-12 shadow-sm flex items-center justify-center rounded-xl shrink-0">📋</div>
         <div>
           <p className="text-blue-900 font-bold">Standard Recommendation Note</p>
           <p className="text-sm text-blue-700 font-medium">These recommendations are based on typical soil profiles in the Vadodara region. We highly suggest conducting a soil health test every 2 years for precision guidance.</p>
         </div>
      </div>
    </div>
  );
}
