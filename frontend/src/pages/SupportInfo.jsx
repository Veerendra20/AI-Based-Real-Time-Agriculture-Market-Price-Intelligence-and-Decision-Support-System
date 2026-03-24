import React from 'react';
import { BookOpen, ExternalLink, ShieldCheck, Landmark } from 'lucide-react';
import { useApp } from '../context/AppContext';

export default function SupportInfo() {
  const { t, language } = useApp();
  
  // Map icons to the translated schemes
  const schemeIcons = [Landmark, ShieldCheck, BookOpen];
  const schemeColors = ["bg-blue-50 text-blue-600", "bg-green-50 text-green-600", "bg-orange-50 text-orange-600"];
  
  // Get schemes from translations based on current language
  // We need to fetch the raw array from the translations object
  const translatedSchemes = t('support.schemes');
  
  // Combine icons/colors with translated data
  const schemes = Array.isArray(translatedSchemes) ? translatedSchemes.map((s, i) => ({
    ...s,
    icon: schemeIcons[i] || BookOpen,
    color: schemeColors[i] || "bg-gray-50 text-gray-600"
  })) : [];

  return (
    <div className="flex-1 bg-[#F8FAFC] p-8 overflow-y-auto">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-extrabold text-slate-900 flex items-center gap-3">
          <BookOpen className="text-[#2F7D4A]" /> {t('support.title')}
        </h1>
        <p className="text-slate-500 mt-1">{t('support.subtitle')}</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
        {schemes.map((scheme, i) => (
          <div key={i} className="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm hover:shadow-md transition-shadow">
            <div className={`w-12 h-12 ${scheme.color} rounded-xl flex items-center justify-center mb-6`}>
               <scheme.icon size={24} />
            </div>
            <h3 className="font-extrabold text-slate-900 mb-2">{scheme.title}</h3>
            <p className="text-sm text-slate-500 mb-6 leading-relaxed">{scheme.desc}</p>
            <button className="flex items-center gap-2 text-[10px] font-black uppercase tracking-widest text-[#2f7d4a] hover:underline">
               {t('support.learn_more')} <ExternalLink size={12} />
            </button>
          </div>
        ))}
      </div>

      <div className="bg-white p-8 rounded-3xl border border-slate-100 shadow-sm">
         <h2 className="text-2xl font-extrabold text-slate-900 mb-4 tracking-tight">{t('support.kcc_title')}</h2>
         <p className="text-slate-500 mb-8 max-w-2xl leading-relaxed">
            {t('support.kcc_desc')}
         </p>
         <div className="bg-[#2f7d4a] text-white p-6 rounded-2xl inline-flex flex-col md:flex-row gap-8 items-center">
            <div>
               <p className="text-[10px] font-black uppercase tracking-[0.2em] opacity-80 mb-1">{t('support.toll_free')}</p>
               <h3 className="text-3xl font-black tracking-tighter">1800-180-1551</h3>
            </div>
            <div className="bg-white/20 px-4 py-2 rounded-xl text-sm font-bold backdrop-blur-sm">
               {t('support.support_247')}
            </div>
         </div>
      </div>
    </div>
  );
}
