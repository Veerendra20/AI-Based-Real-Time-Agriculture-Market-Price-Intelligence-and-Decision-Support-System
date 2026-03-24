import React from 'react';

export default function Content({ activeMenu }) {
  // Map active menu state to the specific display content requested
  const contentMap = {
    'Dashboard': 'Dashboard Content',
    'Market Comparison': 'Market Comparison Content',
    'Price Prediction': 'AI Prediction Content',
    'Fertilizers': 'Fertilizer Data',
    'Loss Analysis': 'Loss Calculator',
    'Support & Info': 'Schemes & Guidance'
  };

  const displayContent = contentMap[activeMenu] || `${activeMenu} Content`;

  return (
    <div className="flex-1 bg-white flex flex-col items-center justify-center h-screen p-8 text-center border-l bg-gray-50/30">
        <div className="bg-white p-12 rounded-3xl shadow-sm border border-gray-100 max-w-2xl w-full">
            <h1 className="text-4xl font-extrabold text-[#2f7d4a] mb-4">
                {displayContent}
            </h1>
            <p className="text-gray-500 text-lg mb-8">
                This is the dynamically updated content area for <strong>{activeMenu}</strong>. 
                In the real application, the React Router or conditional rendering will mount the specific data grids and charts here.
            </p>
            <div className="h-64 rounded-2xl border-2 border-dashed border-gray-200 flex items-center justify-center bg-gray-50/50">
               <span className="text-gray-400 font-medium uppercase tracking-widest text-sm">Dashboard Widget Area</span>
            </div>
        </div>
    </div>
  );
}

