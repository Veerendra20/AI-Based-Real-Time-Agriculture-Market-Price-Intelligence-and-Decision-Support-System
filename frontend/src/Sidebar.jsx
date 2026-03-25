import { useLocation, Link } from 'react-router-dom';
import { useApp } from './context/AppContext';
import { 
  LayoutDashboard, 
  BarChart2, 
  TrendingUp, 
  Leaf, 
  Calculator, 
  BookOpen 
} from 'lucide-react';

export default function Sidebar() {
  const location = useLocation();
  const { language, setLanguage, t } = useApp();

  const menuItems = [
    {
      id: 'Dashboard',
      path: '/dashboard',
      icon: LayoutDashboard,
      title: t('sidebar.dashboard'),
      subtitle: t('sidebar.dashboard_sub')
    },
    {
      id: 'Market Comparison',
      path: '/market-comparison',
      icon: BarChart2,
      title: t('sidebar.market_compare'),
      subtitle: t('sidebar.market_compare_sub')
    },
    {
      id: 'Price Prediction',
      path: '/price-prediction',
      icon: TrendingUp,
      title: t('sidebar.price_prediction'),
      subtitle: t('sidebar.price_prediction_sub')
    },
    {
      id: 'Fertilizers',
      path: '/fertilizers',
      icon: Leaf,
      title: t('sidebar.fertilizers'),
      subtitle: t('sidebar.fertilizers_sub')
    },
    {
      id: 'Loss Analysis',
      path: '/loss-analysis',
      icon: Calculator,
      title: t('sidebar.loss_analysis'),
      subtitle: t('sidebar.loss_analysis_sub')
    },
    {
      id: 'Support & Info',
      path: '/support-info',
      icon: BookOpen,
      title: t('sidebar.support_info'),
      subtitle: t('sidebar.support_info_sub')
    }
  ];

  return (
    <div className="w-80 h-screen bg-white border-r border-gray-200 flex flex-col p-4 shrink-0">
      
      {/* Top Section */}
      <div className="flex items-center gap-4 px-2 py-4 mb-2 border-b border-gray-100 pb-6">
        <div className="w-12 h-12 bg-[#2f7d4a] rounded-full flex items-center justify-center text-white shrink-0">
           <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><rect width="7" height="7" x="3" y="3" rx="1"/><rect width="7" height="7" x="14" y="3" rx="1"/><rect width="7" height="7" x="14" y="14" rx="1"/><rect width="7" height="7" x="3" y="14" rx="1"/></svg>
        </div>
        <div className="flex flex-col">
          <span className="font-bold text-xl text-gray-900 leading-tight">FarmPrice</span>
        </div>
      </div>

      {/* Language Toggle */}
      <div className="px-2 mb-6">
        <div className="bg-gray-50 rounded-2xl p-1 flex gap-1">
          <button 
            onClick={() => setLanguage('en')}
            className={`flex-1 py-2 px-1 rounded-xl text-[10px] font-extrabold transition-all ${language === 'en' ? 'bg-[#2f7d4a] text-white shadow-sm' : 'text-gray-500 hover:text-gray-700'}`}
          >
            English
          </button>
          <button 
            onClick={() => setLanguage('gu')}
            className={`flex-1 py-2 px-1 rounded-xl text-[11px] font-bold transition-all ${language === 'gu' ? 'bg-[#2f7d4a] text-white shadow-sm' : 'text-gray-500 hover:text-gray-700'}`}
          >
            ગુજરાતી
          </button>
          <button 
            onClick={() => setLanguage('hi')}
            className={`flex-1 py-2 px-1 rounded-xl text-[11px] font-bold transition-all ${language === 'hi' ? 'bg-[#2f7d4a] text-white shadow-sm' : 'text-gray-500 hover:text-gray-700'}`}
          >
            हिंदी
          </button>
        </div>
      </div>

      {/* Menu Section */}
      <nav className="flex flex-col gap-2 overflow-y-auto">
        {menuItems.map((item) => {
          const isActive = location.pathname.startsWith(item.path);
          const IconComponent = item.icon;
          
          return (
            <Link
              key={item.id}
              to={item.path}
              className={`flex items-center gap-4 w-full px-4 py-3 rounded-3xl transition-all duration-200 text-left ${
                isActive 
                  ? 'bg-[#2f7d4a] text-white shadow-sm' 
                  : 'text-gray-600 hover:bg-gray-50'
              }`}
            >
              <div className={`shrink-0 flex items-center justify-center p-1 ${isActive ? 'text-white' : 'text-gray-500'}`}>
                <IconComponent size={24} strokeWidth={isActive ? 2.5 : 2} />
              </div>
              <div className="flex flex-col">
                <p className={`font-semibold tracking-wide m-0 ${isActive ? 'text-white' : 'text-gray-800'}`}>
                  {item.title}
                </p>
                <p className={`text-xs mt-0.5 m-0 ${isActive ? 'text-green-100/90' : 'text-gray-500 font-medium'}`}>
                  {item.subtitle}
                </p>
              </div>
            </Link>
          );
        })}
      </nav>
      
      {/* Footer Removed */}

    </div>
  );
}
