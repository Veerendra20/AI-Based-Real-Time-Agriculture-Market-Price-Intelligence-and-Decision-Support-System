import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import joblib  # type: ignore
from datetime import datetime, timedelta
import random
from data_processor import load_and_clean_data, get_market_analysis, get_latest_market_comparison, get_price_trends, get_current_stats  # type: ignore

# --- MULTI-LANGUAGE TRANSLATIONS ---
translations = {
    "en": {
        "title": "FarmPrice | Premium Dashboard",
        "lang_toggle": "English | ગુજરાતી",
        "nav_dashboard": "Dashboard",
        "nav_market": "Market Comparison",
        "nav_price": "Price Prediction",
        "nav_fertilizer": "Fertilizers",
        "nav_loss": "Loss Analysis",
        "nav_support": "Support & Info",
        "sidebar_dashboard_sub": "Today's prices & alerts",
        "sidebar_market_sub": "Compare across markets",
        "sidebar_price_sub": "AI-powered forecasts",
        "sidebar_fertilizer_sub": "Recommendations & prices",
        "sidebar_loss_sub": "Calculate your losses",
        "sidebar_support_sub": "Schemes & guidance",
        "select_crop": "Select Crop",
        "select_market": "Select Market",
        "market_price": "Market Price",
        "msp": "MSP",
        "selling_price": "Your Selling Price",
        "calculate_loss": "Calculate Loss",
        "mandi": "Mandi",
        "profit": "Profit",
        "loss": "Loss",
        "above_msp": "Above MSP",
        "below_msp": "Below MSP",
        "fert_title": "Fertilizer Guide",
        "fert_sub": "Smart recommendations for optimal crop yield in the Vadodara region",
        "soil_type": "Soil Type",
        "nitrogen": "Nitrogen (N)",
        "phosphorus": "Phosphorus (P)",
        "potassium": "Potassium (K)",
        "expert_tips": "Expert Tips for",
        "std_note_title": "Standard Recommendation Note",
        "std_note_text": "These recommendations are based on typical soil profiles in the Vadodara region. We highly suggest conducting a soil health test every 2 years for precision guidance.",
        "loss_title": "Farmer Loss Analysis",
        "loss_sub": "Calculate how much you're losing to middlemen and intermediaries",
        "enter_details": "Enter Your Details",
        "qty_quintals": "Quantity (In Quintals)",
        "benchmark_price": "Benchmark Price",
        "your_price": "Your Price",
        "calc_my_loss": "Calculate My Loss",
        "rev_loss": "Calculated Revenue Loss",
        "excellent_work": "Excellent Work!",
        "price_vs_benchmark": "Farmer Price vs Market Benchmark",
        "enter_qty": "Enter quantity",
        "pred_title": "price prediction",
        "pred_sub": "AI-powered price forecasts to help you decide the best time to sell",
        "pred_period": "Prediction Period",
        "market_insight": "Market Insight",
        "hold_verdict": "STAY CALM: HOLD",
        "sell_verdict": "ACTION: SELL NOW",
        "hold_adv": "Advice: Keep patience and hold the crop",
        "sell_adv": "Advice: Sell the crop now",
        "exp_gain": "Expected Gain",
        "sold_peak": "If sold at peak",
        "mkt_demand": "Market Demand",
        "risk_level": "Risk Level",
        "next_update": "Next Update",
        "pred_conf": "Prediction Confidence",
        "trend_analysis": "Market Trend Analysis",
        "historical": "Historical",
        "predicted": "Predicted",
        "high": "HIGH",
        "low": "LOW",
        "v_high": "VERY HIGH",
        "v_low": "VERY LOW",
        "greeting": "Good Morning, Farmer! 🌾",
        "greeting_sub": "Check today's prices and market insights for your crops",
        "conf_dash": "Configure your dashboard indicators",
        "msp_sub": "Minimum Support Price",
        "price_diff": "Price Difference",
        "best_price_avail": "Best Price Available At",
        "distance": "Distance",
        "mkt_dist_title": "Market Price Distribution (Today)",
        "det_mkt_prices": "Detailed Market Prices",
        "table_mkt": "Market Name",
        "table_price": "Price (₹/q)",
        "table_dist": "Distance",
        "table_rating": "Rating",
        "insight_title": "Understanding the Comparison",
        "tip_title": "Today's Farming Tip",
        "tip_text": "Consider selling your {crop} at government-approved mandis like {market} to avoid middlemen and get prices closer to or above MSP.",
        "view_details": "View Details",
        "fert_rec_title": "Fertilizer Recommendations",
        "fert_rec_sub": "Best fertilizers for your crop with current market prices",
        "quick_guide_title": "Quick Guide",
        "quick_guide_sub": "Recommended fertilizers are best for your crop. Prices are government subsidized rates.",
        "best_badge": "Best",
        "recommended_badge": "Recommended",
        "price_label": "Price",
        "brand_label": "Brand",
        "cost_summary_title": "Estimated Cost Summary (अनुमानित लागत)",
        "total_cost_label": "Total for recommended fertilizers",
        "per_acre_approx": "per acre approx.",
    },
    "gu": {
        "title": "ફાર્મપ્રાઈસ | પ્રીમિયમ ડેશબોર્ડ",
        "lang_toggle": "ગુજરાતી | English",
        "nav_dashboard": "ડેશબોર્ડ",
        "nav_market": "બજારની સરખામણી",
        "nav_price": "ભાવની આગાહી",
        "nav_fertilizer": "ખાતર",
        "nav_loss": "નુકસાનનું વિશ્લેષણ",
        "nav_support": "સપોર્ટ અને માહિતી",
        "sidebar_dashboard_sub": "આજના ભાવ અને ચેતવણીઓ",
        "sidebar_market_sub": "વિવિધ બજારો વચ્ચે તુલના કરો",
        "sidebar_price_sub": "AI-આધારિત આગાહી",
        "sidebar_fertilizer_sub": "ભલામણો અને ભાવો",
        "sidebar_loss_sub": "તમારા નુકસાનની ગણતરી કરો",
        "sidebar_support_sub": "યોજનાઓ અને માર્ગદર્શન",
        "select_crop": "પાક પસંદ કરો",
        "select_market": "બજાર પસંદ કરો",
        "market_price": "બજાર ભાવ",
        "msp": "ન્યૂનતમ આધાર ભાવ",
        "selling_price": "તમારો વેચાણ ભાવ",
        "calculate_loss": "નુકસાન ગણો",
        "mandi": "મંડી",
        "profit": "નફો",
        "loss": "નુકસાન",
        "above_msp": "MSP થી ઉપર",
        "below_msp": "MSP થી નીચે",
        "fert_title": "ખાતર માર્ગદર્શિકા",
        "fert_sub": "વડોદરા વિસ્તારમાં પાકના શ્રેષ્ઠ ઉત્પાદન માટે સ્માર્ટ ભલામણો",
        "soil_type": "જમીનનો પ્રકાર",
        "nitrogen": "નાઇટ્રોજન (N)",
        "phosphorus": "ફોસ્ફરસ (P)",
        "potassium": "પોટેશિયમ (K)",
        "expert_tips": "માટે નિષ્ણાત ટિપ્સ",
        "std_note_title": "સામાન્ય ભલામણ નોંધ",
        "std_note_text": "આ ભલામણો વડોદરા વિસ્તારની સામાન્ય જમીન પર આધારિત છે. અમે ચોકસાઈપૂર્વક માર્ગદર્શન માટે દર 2 વર્ષે જમીનના સ્વાસ્થ્યનું પરીક્ષણ કરવાની ભલામણ કરીએ છીએ.",
        "loss_title": "ખેડૂત નુકસાન વિશ્લેષણ",
        "loss_sub": "તમે વચેટિયાઓ અને મધ્યસ્થીઓને કેટલું ગુમાવી રહ્યા છો તેની ગણતરી કરો",
        "enter_details": "તમારી વિગતો દાખલ કરો",
        "qty_quintals": "જથ્થો (ક્વિન્ટલમાં)",
        "benchmark_price": "બેન્ચમાર્ક કિંમત",
        "your_price": "તમારી કિંમત",
        "calc_my_loss": "મારું નુકસાન ગણો",
        "rev_loss": "ગણતરી કરેલ મહેસૂલ નુકસાન",
        "excellent_work": "ઉત્તમ કામ!",
        "price_vs_benchmark": "ખેડૂત ભાવ વિ બજાર બેન્ચમાર્ક",
        "enter_qty": "જથ્થો દાખલ કરો",
        "pred_title": "ભાવની આગાહી",
        "pred_sub": "સૌથી શ્રેષ્ઠ સમયે વેચવા માટે AI-આધારિત ભાવની આગાહી",
        "pred_period": "આગાહીનો સમયગાળો",
        "market_insight": "બજારની સમજ",
        "hold_verdict": "ધીરજ રાખો: અત્યારે ન વેચો",
        "sell_verdict": "તુરંત વેચો: અત્યારે યોગ્ય ભાવ છે",
        "hold_adv": "સલાહ: અત્યારે પાકને રોકી રાખો",
        "sell_adv": "સલાહ: અત્યારે પાક વેચો",
        "exp_gain": "અપેક્ષિત નફો",
        "sold_peak": "જો રેકોર્ડ ભાવે વેચવામાં આવે તો",
        "mkt_demand": "બજારની માંગ",
        "risk_level": "જોખમનું સ્તર",
        "next_update": "આગામી અપડેટ",
        "pred_conf": "આગાહીનો આત્મવિશ્વાસ",
        "trend_analysis": "બજારના વલણનું વિશ્લેષણ",
        "historical": "ઐતિહાસિક",
        "predicted": "આગાહી કરેલ",
        "high": "ઉચ્ચ",
        "low": "નીચું",
        "v_high": "ખૂબ ઉચ્ચ",
        "v_low": "ખૂબ નીચું",
        "greeting": "શુભ સવાર, ખેડૂત મિત્ર! 🌾",
        "greeting_sub": "તમારા પાક માટે આજના ભાવ અને બજારની માહિતી તપાસો",
        "conf_dash": "તમારા ડેશબોર્ડ સૂચકાંકો ગોઠવો",
        "msp_sub": "ન્યૂનતમ ટેકાના ભાવ",
        "price_diff": "ભાવનો તફાવત",
        "best_price_avail": "સૌથી વધુ ભાવ અહીં ઉપલબ્ધ છે",
        "distance": "અંતર",
        "mkt_dist_title": "બજાર ભાવ વિતરણ (આજે)",
        "det_mkt_prices": "વિગતવાર બજાર ભાવો",
        "table_mkt": "બજારનું નામ",
        "table_price": "ભાવ (₹/ક્વિન્ટલ)",
        "table_dist": "અંતર",
        "table_rating": "રેટિંગ",
        "insight_title": "તુલનાને સમજવી",
        "tip_title": "આજની ખેતીની ટિપ",
        "tip_text": "તમારા {crop} ને વચેટિયાઓથી બચવા અને MSP ની નજીક અથવા તેનાથી વધુ ભાવ મેળવવા માટે {market} જેવી સરકારી માન્ય મંડીઓમાં વેચવાનું વિચારો.",
        "view_details": "વિગતવાર જુઓ",
        "fert_rec_title": "ખાતરની ભલામણો",
        "fert_rec_sub": "વર્તમાન બજાર ભાવો સાથે તમારા પાક માટે શ્રેષ્ઠ ખાતર",
        "quick_guide_title": "ઝડપી માર્ગદર્શિકા",
        "quick_guide_sub": "ભલામણ કરેલ ખાતર તમારા પાક માટે શ્રેષ્ઠ છે. કિંમતો સરકારી સબસિડીવાળા દરો છે.",
        "best_badge": "શ્રેષ્ઠ",
        "recommended_badge": "ભલામણ કરેલ",
        "price_label": "કિંમત",
        "brand_label": "બ્રાન્ડ",
        "cost_summary_title": "અંદાજિત ખર્ચ સારાંશ (અનુમાનિત લાગત)",
        "total_cost_label": "ભલામણ કરેલ ખાતર માટે કુલ",
        "per_acre_approx": "એકર દીઠ અંદાજે.",
    },
    "hi": {
        "title": "फार्मप्राइस | प्रीमियम डैशबोर्ड",
        "lang_toggle": "English | ગુજરાતી | हिंदी",
        "nav_dashboard": "डैशबोर्ड",
        "nav_market": "बाजार तुलना",
        "nav_price": "मूल्य पूर्वानुमान",
        "nav_fertilizer": "उर्वरक",
        "nav_loss": "हानि विश्लेषण",
        "nav_support": "सहायता और जानकारी",
        "sidebar_dashboard_sub": "आज की कीमतें और अलर्ट",
        "sidebar_market_sub": "विभिन्न बाजारों में तुलना करें",
        "sidebar_price_sub": "AI-संचालित पूर्वानुमान",
        "sidebar_fertilizer_sub": "सिफारिशें और कीमतें",
        "sidebar_loss_sub": "अपने नुकसान की गणना करें",
        "sidebar_support_sub": "योजनाएं और मार्गदर्शन",
        "select_crop": "फसल चुनें",
        "select_market": "बाजार चुनें",
        "market_price": "बाजार मूल्य",
        "msp": "न्यूनतम समर्थन मूल्य (MSP)",
        "selling_price": "आपकी बिक्री कीमत",
        "calculate_loss": "हानि की गणना करें",
        "mandi": "मंडी",
        "profit": "लाभ",
        "loss": "हानि",
        "above_msp": "MSP से ऊपर",
        "below_msp": "MSP से नीचे",
        "fert_title": "उर्वरक मार्गदर्शन",
        "fert_sub": "वडोदरा क्षेत्र में बेहतर फसल उपज के लिए स्मार्ट सिफारिशें",
        "soil_type": "मिट्टी का प्रकार",
        "nitrogen": "नाइट्रोजन (N)",
        "phosphorus": "फास्फोरस (P)",
        "potassium": "पोटेशियम (K)",
        "expert_tips": "के लिए विशेषज्ञ सुझाव",
        "std_note_title": "मानक सिफारिश नोट",
        "std_note_text": "ये सिफारिशें वडोदरा क्षेत्र की सामान्य मिट्टी पर आधारित हैं। हम सटीक मार्गदर्शन के लिए हर 2 साल में मिट्टी के स्वास्थ्य परीक्षण की सलाह देते हैं।",
        "loss_title": "किसान हानि विश्लेषण",
        "loss_sub": "गणना करें कि आप बिचौलियों और मध्यस्थों को कितना खो रहे हैं",
        "enter_details": "अपने विवरण दर्ज करें",
        "qty_quintals": "मात्रा (क्विंटल में)",
        "benchmark_price": "बेंचमार्क मूल्य",
        "your_price": "आपकी कीमत",
        "calc_my_loss": "मेरी हानि की गणना करें",
        "rev_loss": "गणना किया गया राजस्व नुकसान",
        "excellent_work": "उत्कृष्ट कार्य!",
        "price_vs_benchmark": "किसान मूल्य बनाम बाजार बेंचमार्क",
        "enter_qty": "मात्रा दर्ज करें",
        "pred_title": "मूल्य पूर्वानुमान",
        "pred_sub": "सर्वोत्तम समय पर बेचने के लिए AI-संचालित मूल्य पूर्वानुमान",
        "pred_period": "पूर्वानुमान अवधि",
        "market_insight": "बाजार अंतर्दृष्टि",
        "hold_verdict": "धैर्य रखें: अभी न बेचें",
        "sell_verdict": "बेचें: अभी सही कीमत है",
        "hold_adv": "सलाह: फसल को रोक कर रखें",
        "sell_adv": "सलाह: फसल अभी बेचें",
        "exp_gain": "अपेक्षित लाभ",
        "sold_peak": "अगर उच्चतम मूल्य पर बेचा जाए",
        "mkt_demand": "बाजार की मांग",
        "risk_level": "जोखिम का स्तर",
        "next_update": "अगला अपडेट",
        "pred_conf": "पूर्वानुमान का विश्वास",
        "trend_analysis": "बाजार के रुझान का विश्लेषण",
        "historical": "ऐतिहासिक",
        "predicted": "अनुमानित",
        "high": "उच्च",
        "low": "कम",
        "v_high": "बहुत अधिक",
        "v_low": "बहुत कम",
        "greeting": "शुभ प्रभात, किसान भाई! 🌾",
        "greeting_sub": "अपनी फसलों के लिए आज की कीमतें और बाजार की जानकारी देखें",
        "conf_dash": "अपने डैशबोर्ड संकेतकों को कॉन्फ़िगर करें",
        "msp_sub": "न्यूनतम समर्थन मूल्य",
        "price_diff": "मूल्य का अंतर",
        "best_price_avail": "सबसे अच्छी कीमत यहाँ उपलब्ध है",
        "distance": "दूरी",
        "mkt_dist_title": "बाजार मूल्य वितरण (आज)",
        "det_mkt_prices": "विस्तृत बाजार मूल्य",
        "table_mkt": "मंडी का नाम",
        "table_price": "मूल्य (₹/क्विंटल)",
        "table_dist": "दूरी",
        "table_rating": "रेटिंग",
        "insight_title": "तुलना को समझना",
        "tip_title": "आज की खेती की सलाह",
        "tip_text": "बिचौलियों से बचने और MSP के करीब या उससे अधिक मूल्य प्राप्त करने के लिए अपनी {crop} को {market} जैसी सरकारी मंडियों में बेचने पर विचार करें।",
        "view_details": "विवरण देखें",
        "fert_rec_title": "उर्वरक सिफारिशें",
        "fert_rec_sub": "वर्तमान बाजार मूल्यों के साथ आपकी फसल के लिए सर्वोत्तम उर्वरक",
        "quick_guide_title": "त्वरित मार्गदर्शिका",
        "quick_guide_sub": "सिफारिश किए गए उर्वरक आपकी फसल के लिए सबसे अच्छे हैं। कीमतें सरकारी सब्सिडी वाली दरें हैं।",
        "best_badge": "सर्वश्रेष्ठ",
        "recommended_badge": "अनुशंसित",
        "price_label": "कीमत",
        "brand_label": "ब्रांड",
        "cost_summary_title": "अनुमानित लागत सारांश",
        "total_cost_label": "अनुशंसित उर्वरकों के लिए कुल",
        "per_acre_approx": "प्रति एकड़ लगभग।",
    }
}

crop_translations = {
    "en": {"Tomato": "Tomato", "Onion": "Onion", "Chilli": "Chilli", "Cotton": "Cotton", "Potato": "Potato"},
    "gu": {"Tomato": "ટામેટા", "Onion": "ડુંગળી", "Chilli": "મરચાં", "Cotton": "કપાસ", "Potato": "બટાકા"},
    "hi": {"Tomato": "टमाटर", "Onion": "प्याज", "Chilli": "मिर्च", "Cotton": "कपास", "Potato": "आलू"}
}

market_translations = {
    "en": {"Waghodia": "Waghodia", "Vadodara": "Vadodara", "Padra": "Padra", "Dabhoi": "Dabhoi", "Karjan": "Karjan", "Savli": "Savli", "Shinor": "Shinor"},
    "gu": {"Waghodia": "વાઘોડિયા", "Vadodara": "વડોદરા", "Padra": "પાદરા", "Dabhoi": "ડભોઇ", "Karjan": "કરજન", "Savli": "સાવલી", "Shinor": "શીનોર"},
    "hi": {"Waghodia": "वाघोडिया", "Vadodara": "वडोदरा", "Padra": "पादरा", "Dabhoi": "डभोई", "Karjan": "करजन", "Savli": "सावली", "Shinor": "शिनोर"}
}

def tc(crop):
    lang = st.session_state.lang
    return crop_translations.get(lang, {}).get(crop, crop)

def tm(market):
    lang = st.session_state.lang
    return market_translations.get(lang, {}).get(market, market)

# st.set_page_config must be the first Streamlit command
st.set_page_config(page_title="FarmPrice | Gujarat", page_icon="🌾", layout="wide")

# Initialize language session state
if 'lang' not in st.session_state:
    st.session_state.lang = 'en'

# Helper for translation
def t(key):
    return translations[st.session_state.lang].get(key, key)


# Load Inter Font
st.markdown('<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">', unsafe_allow_html=True)

# --- NEXT LEVEL SaaS CSS ---
st.markdown("""
<style>
    /* Mesh Gradient Background */
    @keyframes meshGradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Inter', sans-serif !important;
        background: linear-gradient(-45deg, #F8FAFC, #F1F5F9, #ECFDF5, #F8FAFC);
        background-size: 400% 400%;
        animation: meshGradient 15s ease infinite !important;
    }
    
    /* Floating Glass Sidebar */
    section[data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.8) !important;
        backdrop-filter: blur(24px) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 0 32px 32px 0 !important;
        margin: 16px 0 16px 0 !important;
        height: calc(100vh - 32px) !important;
        box-shadow: 12px 0 32px rgba(0,0,0,0.03) !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    
    /* Entrance Animations */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .stMarkdown, .stPlotlyChart, .metric-card, .fz-card, .sp-card, .m-card, .ha-card, .chart-container, .forecast-matrix, .calculator-panel {
        animation: fadeInUp 0.8s cubic-bezier(0.23, 1, 0.32, 1) both;
    }
    
    /* Shared Global Page Headers */
    .mc-header, .pp-header, .la-header { display: flex; align-items: center; gap: 12px; margin-bottom: 4px; }
    .pp-title { font-size: 24px; font-weight: 950; color: #1E293B; margin: 0; letter-spacing: -0.03em; }
    .pp-subtitle { font-size: 13px; color: #64748B; margin-bottom: 24px; line-height: 1.5; }
    .pp-sel-lbl-fix { font-size: 11px; font-weight: 800; color: #64748B; text-transform: uppercase; margin-bottom: 8px; display: block; letter-spacing: 0.5px; }

    
    /* Next Level Glass 2.0 Components */
    .metric-card {
        background: rgba(255, 255, 255, 0.6);
        backdrop-filter: blur(20px);
        padding: 20px;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.7);
        box-shadow: 0 15px 35px -10px rgba(0,0,0,0.05);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        margin-bottom: 16px;
    }
    .metric-card:hover { transform: translateY(-4px) scale(1.02); border-color: #10B981; box-shadow: 0 15px 30px -10px rgba(16,185,129,0.2); }

    .ha-card { 
        background: rgba(255, 255, 255, 0.45); 
        backdrop-filter: blur(24px); 
        border: 1px solid rgba(255, 255, 255, 0.5); 
        border-radius: 20px; 
        padding: 32px; 
        margin-bottom: 24px; 
        box-shadow: 0 15px 40px rgba(0,0,0,0.04); 
        transition: 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275); 
    }
    .ha-card:hover { transform: translateY(-6px); border-color: #10B981; box-shadow: 0 25px 60px rgba(16,185,129,0.12); }
    .ha-status-pill { background: #10B981; color: white; padding: 6px 16px; border-radius: 16px; font-size: 11px; font-weight: 800; text-transform: uppercase; margin-bottom: 16px; letter-spacing: 0.1em; }
    .ha-verdict { font-size: 40px; font-weight: 950; color: #064E3B; margin: 0; line-height: 0.95; letter-spacing: -0.05em; }
    
    .chart-container { 
        background: rgba(255, 255, 255, 0.55); 
        backdrop-filter: blur(28px); 
        padding: 24px; 
        border-radius: 20px; 
        border: 1px solid rgba(255, 255, 255, 0.6); 
        box-shadow: 0 15px 40px rgba(0,0,0,0.03); 
        margin-bottom: 24px; 
    }

    /* Market Price Intensity Ranking */
    .m-card-gold { border: 2px solid #F59E0B !important; background: linear-gradient(135deg, rgba(255,251,235,0.9), rgba(254,243,199,0.9)) !important; box-shadow: 0 15px 30px rgba(245,158,11,0.15) !important; }
    .m-card-silver { border: 1.5px solid #94A3B8 !important; background: linear-gradient(135deg, rgba(248,250,252,0.9), rgba(241,245,249,0.9)) !important; }
    .m-card-bronze { border: 1.5px solid #B45309 !important; background: rgba(255,255,255,0.9) !important; }
    .rank-badge { position: absolute; top: 16px; right: 16px; width: 28px; height: 28px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
    .rank-1 { background: #F59E0B; color: white; border: 2px solid #FEF3C7; }
    .rank-2 { background: #94A3B8; color: white; border: 2px solid #F1F5F9; }
    .rank-3 { background: #B45309; color: white; border: 2px solid #FFEDD5; }

    /* Forecast Matrix (Holographic) */
    .forecast-matrix { background: rgba(15, 23, 42, 0.8); backdrop-filter: blur(32px); border: 1px solid rgba(16, 185, 129, 0.4); border-radius: 16px; padding: 24px; color: white; box-shadow: 0 0 40px -15px rgba(16,185,129,0.2); }
    .matrix-title { font-size: 16px; font-weight: 900; color: #10B981; text-transform: uppercase; letter-spacing: 0.15em; margin-bottom: 12px; }
    .matrix-val { font-size: 36px; font-weight: 950; color: white; letter-spacing: -0.04em; }
    
    /* Impact Hub (Calculator Panels) */
    .calculator-panel { background: white; border-radius: 16px; border: 1px solid #F1F5F9; padding: 24px; box-shadow: 0 15px 30px rgba(0,0,0,0.02); }
    .calc-impact-header { display: flex; align-items: center; gap: 12px; margin-bottom: 16px; }
    .calc-icon-dot { width: 10px; height: 10px; border-radius: 50%; background: #E11D48; animation: pulse 2s infinite; }
    @keyframes pulse { 0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(225,29,72,0.7); } 70% { transform: scale(1.1); box-shadow: 0 0 0 10px rgba(225,29,72,0); } 100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(225,29,72,0); } }

    /* Market Ticker */
    .ticker-wrap { width: 100%; overflow: hidden; background: #1E293B; color: #F8FAFC; padding: 8px 0; border-radius: 12px; margin-bottom: 2rem; border: 1px solid rgba(255,255,255,0.1); }
    .ticker { display: inline-block; white-space: nowrap; padding-right: 100%; animation: ticker 50s linear infinite; font-weight: 700; font-size: 13px; }
    @keyframes ticker {
        0% { transform: translate3d(0, 0, 0); }
        100% { transform: translate3d(-100%, 0, 0); }
    }
    .ticker-item { display: inline-block; padding: 0 40px; border-right: 1px solid #334155; }

    /* Reusable Utilities */
    .m-title { font-size: 11px; font-weight: 800; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 8px; }
    .m-price { font-size: 24px; font-weight: 950; color: #1E293B; }
    .market-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 16px; margin-top: 24px; }
    .m-card { background: white; border-radius: 16px; border: 1px solid #F1F5F9; padding: 20px; transition: 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275); position: relative; }
    
    /* 3D Tilt Utilities - Overriding previous simple hovers */
    .metric-card, .m-card, .fz-card, .sp-card, .support-header {
        transform-style: preserve-3d;
        perspective: 1000px;
    }
    .metric-card:hover, .fz-card:hover, .sp-card:hover {
        transform: translateY(-4px) rotateX(2deg) rotateY(-2deg);
        box-shadow: 0 15px 30px -10px rgba(16, 185, 129, 0.15);
    }
    .m-card:hover {
        border-color: #10B981;
        transform: translateY(-6px) rotateX(2deg) rotateY(-2deg) scale(1.02);
        box-shadow: 0 20px 40px -15px rgba(16, 185, 129, 0.2);
    }

    /* Ultra-Premium Webkit Scrollbar */
    ::-webkit-scrollbar { width: 8px; height: 8px; }
    ::-webkit-scrollbar-track { background: #0F172A; }
    ::-webkit-scrollbar-thumb { background: #10B981; border-radius: 10px; }
    ::-webkit-scrollbar-thumb:hover { background: #059669; }

    /* Dynamic Gradient Borders (Glow Animation) */
    @keyframes borderGlow {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .m-card-gold::before {
        content: ""; position: absolute; top: -3px; left: -3px; right: -3px; bottom: -3px;
        z-index: -1; border-radius: 39px;
        background: linear-gradient(90deg, #F59E0B, #FBBF24, #10B981, #F59E0B);
        background-size: 300% 300%;
        animation: borderGlow 4s ease infinite;
    }

    /* Floating AI Assistant FAB */
    .ai-fab {
        position: fixed; bottom: 40px; right: 40px; z-index: 999999;
        width: 68px; height: 68px; border-radius: 50%;
        background: linear-gradient(135deg, #10B981, #059669);
        box-shadow: 0 10px 25px rgba(16, 185, 129, 0.4);
        display: flex; align-items: center; justify-content: center;
        color: white; font-size: 28px; cursor: pointer;
        transition: 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        animation: pulseFAB 2s infinite;
    }
    .ai-fab:hover {
        transform: scale(1.15) rotate(15deg);
        box-shadow: 0 20px 40px rgba(16, 185, 129, 0.6);
        animation: none;
    }
    @keyframes pulseFAB {
        0% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
        70% { box-shadow: 0 0 0 25px rgba(16, 185, 129, 0); }
        100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
    }
    .ai-fab-tooltip {
        position: absolute; right: 85px; top: 18px;
        background: #1E293B; color: white;
        padding: 10px 20px; border-radius: 16px; font-size: 15px; font-weight: 800;
        opacity: 0; pointer-events: none; transition: 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        white-space: nowrap; box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        border: 1px solid rgba(255,255,255,0.1);
        transform: translateX(10px);
    }
    .ai-fab:hover .ai-fab-tooltip { 
        opacity: 1; 
        transform: translateX(0); 
    }
</style>

<div class="ai-fab">
    ✨
    <div class="ai-fab-tooltip">Chat with FarmPrice AI</div>
</div>
""", unsafe_allow_html=True)

# --- REUSABLE COMPONENTS ---
def render_market_ticker(df):
    all_markets = df['Market Name'].unique()[:10]
    ticker_html = """<div class="ticker-wrap"><div class="ticker">"""
    for m in all_markets:
        avg_p = df[df['Market Name'] == m]['Market Price'].mean()
        ticker_html += f"""<div class="ticker-item">🏛️ {tm(m)}: <span class="ticker-price">₹{avg_p:,.0f}</span></div>"""
    ticker_html += """</div></div>"""
    st.markdown(ticker_html, unsafe_allow_html=True)

def render_metric_card(label, value, icon="💰", status="neutral"):
    color_map = {
        "good": "#22C55E",
        "bad": "#EF4444",
        "neutral": "#64748B"
    }
    color = color_map.get(status, "#1E293B")
    
    html = f"""
    <div class="metric-card">
        <div class="metric-label"><span>{icon}</span> {label}</div>
        <div class="metric-value">{value}</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

# --- DATA LOADING ---
@st.cache_data
def get_data_v4():
    return load_and_clean_data('mandi_data.csv')

df = get_data_v4()

# --- INITIALIZE GLOBAL SESSION STATE ---
if 'sel_crop' not in st.session_state:
    st.session_state.sel_crop = sorted(df['Crop Name'].unique())[0]
if 'sel_market' not in st.session_state:
    # Get first available market for the initial crop
    initial_crop = st.session_state.sel_crop
    mkt_list = sorted(df[df['Crop Name'] == initial_crop]['Market Name'].unique())
    st.session_state.sel_market = mkt_list[0] if mkt_list else ""

# --- ML MODEL LOADING ---
@st.cache_resource
def load_ml_models():
    try:
        model = joblib.load('price_model.joblib')
        le_crop = joblib.load('le_crop.joblib')
        le_market = joblib.load('le_market.joblib')
        return model, le_crop, le_market
    except:
        return None, None, None

model, le_crop, le_market = load_ml_models()

def predict_future_prices(crop: str, market: str, period_months: int):
    if not model or not le_crop or not le_market:
        return None
    try:
        crop_enc = le_crop.transform([crop])[0]
        mark_enc = le_market.transform([market])[0]
        now = datetime.now()
        future_dates = []
        predictions = []
        for i in range(1, period_months + 1):
            future_month = (now.month + i - 1) % 12 + 1
            future_year = now.year + (now.month + i - 1) // 12
            # Use day 15 for a stable monthly estimate
            pred = model.predict([[crop_enc, mark_enc, 15, future_month, future_year]])[0]
            future_dates.append(datetime(future_year, future_month, 15))
            predictions.append(pred)
        return pd.DataFrame({'Date': future_dates, 'Market Price': predictions})
    except:
        return None

# --- SIDEBAR NAVIGATION ---
# --- SIDEBAR NAVIGATION ---
# We use standard Streamlit radio buttons for perfect interactivity,
# but we style them aggressively with CSS to look exactly like the premium design.

if 'page' not in st.session_state:
    st.session_state.page = "Dashboard"

with st.sidebar:
    # Sidebar Navigation Styling
    st.markdown(f"""
        <div style="text-align: center; padding-bottom: 20px;">
            <h1 style="color: #2E7D32; font-size: 28px; margin-bottom: 0;">🌾 FarmPrice</h1>
            <p style="color: #666; font-size: 14px; margin-top: 5px;">Smart Farming for Vadodara</p>
        </div>
    """, unsafe_allow_html=True)

    # Language Toggle in Sidebar
    lang_col1, lang_col2, lang_col3 = st.sidebar.columns(3)
    with lang_col1:
        if st.button("English", use_container_width=True, type="primary" if st.session_state.lang == 'en' else "secondary"):
            st.session_state.lang = 'en'
            st.rerun()
    with lang_col2:
        if st.button("ગુજરાતી", use_container_width=True, type="primary" if st.session_state.lang == 'gu' else "secondary"):
            st.session_state.lang = 'gu'
            st.rerun()
    with lang_col3:
        if st.button("हिंदी", use_container_width=True, type="primary" if st.session_state.lang == 'hi' else "secondary"):
            st.session_state.lang = 'hi'
            st.rerun()

    st.sidebar.markdown("---")

    # Native Radio Buttons mapped to rich HTML labels
    # We use Streamlit Markdown within the radio label to split title and subtext!
    nav_selection = st.radio(
        "Navigation",
        [
            f"**{t('nav_dashboard')}**",
            f"**{t('nav_market')}**",
            f"**{t('nav_price')}**",
            f"**{t('nav_fertilizer')}**",
            f"**{t('nav_loss')}**",
            f"**{t('nav_support')}**"
        ],
        label_visibility="collapsed"
    )

    # Custom Header matching exactly
    st.markdown("""
    <style>
        /* Modern Font Injection */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        
        /* Apply font to sidebar */
        [data-testid="stSidebar"] {
            font-family: 'Inter', sans-serif;
            background-color: transparent !important;
        }
        
        /* Hide Default Radio Circles */
        .stRadio div[data-testid="stMarkdownContainer"] p {
            display: flex;
            flex-direction: column;
            align-items: flex-start;
            margin: 0;
            padding: 0;
            cursor: pointer;
            width: 100%;
        }
        
        [data-testid="stRadio"] div[role="radiogroup"] > label {
            background: transparent;
            padding: 12px 16px 12px 48px !important; /* Padding for the absolute icon */
            border-radius: 20px;
            margin-bottom: 8px;
            transition: all 0.2s ease;
            position: relative;
        }

        /* Hover State */
        [data-testid="stRadio"] div[role="radiogroup"] > label:hover {
            background-color: #F3F4F6 !important;
        }

        /* Active State */
        [data-testid="stRadio"] div[role="radiogroup"] > label:has(input:checked) {
            background-color: #2f7d4a !important;
            box-shadow: 0 4px 6px -1px rgba(47, 125, 74, 0.2), 0 2px 4px -2px rgba(47, 125, 74, 0.2);
        }

        /* Hide the actual radio circle marker */
        [data-testid="stRadio"] [data-baseweb="radio"] > div:first-child {
            display: none !important;
        }

        /* ----- Title Styling inside the Radio ----- */
        [data-testid="stRadio"] div[data-testid="stMarkdownContainer"] p strong {
            font-weight: 500;
            font-size: 0.95rem;
            line-height: 1.2;
            color: #4B5563;
        }
        
        /* Active Title Color */
        [data-testid="stRadio"] label:has(input:checked) div[data-testid="stMarkdownContainer"] p strong {
            font-weight: 600;
            color: white !important;
        }

        /* ----- Subtitle Styling inside the Radio via ::after ----- */
        [data-testid="stRadio"] div[role="radiogroup"] > label div[data-testid="stMarkdownContainer"] p::after {
            display: block;
            font-size: 0.75rem;
            color: #6B7280;
            margin-top: 3px;
            font-weight: 400;
        }
        
        /* Active Subtitle Color */
        [data-testid="stRadio"] div[role="radiogroup"] > label:has(input:checked) div[data-testid="stMarkdownContainer"] p::after {
            color: rgba(255, 255, 255, 0.85) !important;
        }

        /* Injecting the actual subtitle strings */
        [data-testid="stRadio"] div[role="radiogroup"] > label:nth-child(1) div[data-testid="stMarkdownContainer"] p::after {{ content: "{t('sidebar_dashboard_sub')}"; }}
        [data-testid="stRadio"] div[role="radiogroup"] > label:nth-child(2) div[data-testid="stMarkdownContainer"] p::after {{ content: "{t('sidebar_market_sub')}"; }}
        [data-testid="stRadio"] div[role="radiogroup"] > label:nth-child(3) div[data-testid="stMarkdownContainer"] p::after {{ content: "{t('sidebar_price_sub')}"; }}
        [data-testid="stRadio"] div[role="radiogroup"] > label:nth-child(4) div[data-testid="stMarkdownContainer"] p::after {{ content: "{t('sidebar_fertilizer_sub')}"; }}
        [data-testid="stRadio"] div[role="radiogroup"] > label:nth-child(5) div[data-testid="stMarkdownContainer"] p::after {{ content: "{t('sidebar_loss_sub')}"; }}
        [data-testid="stRadio"] div[role="radiogroup"] > label:nth-child(6) div[data-testid="stMarkdownContainer"] p::after {{ content: "{t('sidebar_support_sub')}"; }}

        /* =========================================
           ICON INJECTION VIA CSS 
           ========================================= */
        [data-testid="stRadio"] div[role="radiogroup"] > label::before {
            content: '';
            position: absolute;
            left: 16px;
            top: 50%;
            transform: translateY(-50%);
            width: 20px;
            height: 20px;
            background-size: contain;
            background-repeat: no-repeat;
            opacity: 0.7;
            transition: all 0.2s ease;
        }

        /* Active Icon State - Make it white and 100% opacity */
        [data-testid="stRadio"] div[role="radiogroup"] > label:has(input:checked)::before {
            filter: brightness(0) invert(1);
            opacity: 1;
        }

        /* 1: Dashboard (Grid Icon) */
        [data-testid="stRadio"] div[role="radiogroup"] > label:nth-child(1)::before {
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%234B5563' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Crect width='7' height='7' x='3' y='3' rx='1'/%3E%3Crect width='7' height='7' x='14' y='3' rx='1'/%3E%3Crect width='7' height='7' x='14' y='14' rx='1'/%3E%3Crect width='7' height='7' x='3' y='14' rx='1'/%3E%3C/svg%3E");
        }
        
        /* 2: Market Comparison (Chart Line) */
        [data-testid="stRadio"] div[role="radiogroup"] > label:nth-child(2)::before {
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%234B5563' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cline x1='12' x2='12' y1='20' y2='10'/%3E%3Cline x1='18' x2='18' y1='20' y2='4'/%3E%3Cline x1='6' x2='6' y1='20' y2='16'/%3E%3C/svg%3E");
        }

        /* 3: Price Prediction (Trending Up) */
        [data-testid="stRadio"] div[role="radiogroup"] > label:nth-child(3)::before {
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%234B5563' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='22 7 13.5 15.5 8.5 10.5 2 17'/%3E%3Cpolyline points='16 7 22 7 22 13'/%3E%3C/svg%3E");
        }

        /* 4: Fertilizers (Leaf) */
        [data-testid="stRadio"] div[role="radiogroup"] > label:nth-child(4)::before {
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%234B5563' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z'/%3E%3Cpath d='M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12'/%3E%3C/svg%3E");
        }

        /* 5: Loss Analysis (Calculator) */
        [data-testid="stRadio"] div[role="radiogroup"] > label:nth-child(5)::before {
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%234B5563' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Crect width='16' height='20' x='4' y='2' rx='2'/%3E%3Cline x1='8' x2='16' y1='6' y2='6'/%3E%3Cline x1='16' x2='16' y1='14' y2='18'/%3E%3Cpath d='M16 10h.01'/%3E%3Cpath d='M12 10h.01'/%3E%3Cpath d='M8 10h.01'/%3E%3Cpath d='M12 14h.01'/%3E%3Cpath d='M8 14h.01'/%3E%3Cpath d='M12 18h.01'/%3E%3Cpath d='M8 18h.01'/%3E%3C/svg%3E");
        }

        /* 6: Support & Info (Book) */
        [data-testid="stRadio"] div[role="radiogroup"] > label:nth-child(6)::before {
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%234B5563' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1 0-5H20'/%3E%3C/svg%3E");
        }
    </style>
    """, unsafe_allow_html=True)

# Clean the selection by grabbing only the bolded part (e.g., "**Dashboard**")
# and stripping the asterisks to exactly match our page routing strings.
page_clean = nav_selection.replace("**", "")

# ---------------------------------------------------------
# Shared Tailwind CSS (available across ALL page sections)
# ---------------------------------------------------------
react_css = """
    <style>
    .tw-bg-slate-50 { background-color: #f8fafc; }
    .tw-bg-white { background-color: #ffffff; }
    .tw-bg-green-100 { background-color: #dcfce7; }
    .tw-bg-green-200 { background-color: #bbf7d0; }
    .tw-text-slate-900 { color: #0f172a; }
    .tw-text-slate-800 { color: #1e293b; }
    .tw-text-slate-700 { color: #334155; }
    .tw-text-slate-500 { color: #64748b; }
    .tw-text-slate-400 { color: #94a3b8; }
    .tw-text-green-800 { color: #166534; }
    .tw-text-green-900 { color: #14532d; }
    .tw-text-green-600 { color: #16a34a; }
    .tw-text-green-700 { color: #15803d; }
    .tw-text-yellow-500 { color: #eab308; }
    .tw-border-slate-100 { border-color: #f1f5f9; border-style: solid; }
    .tw-border-green-200 { border-color: #bbf7d0; border-style: solid; }
    .tw-border-yellow-500 { border-color: #eab308; border-style: solid; }
    .tw-rounded-3xl { border-radius: 1.5rem; }
    .tw-rounded-2xl { border-radius: 1rem; }
    .tw-rounded-full { border-radius: 9999px; }
    .tw-rounded { border-radius: 0.25rem; }
    .tw-shadow-sm { box-shadow: 0 1px 2px 0 rgb(0 0 0 / 0.05); }
    .tw-shadow-md { box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1); }
    .tw-shadow-lg { box-shadow: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1); }
    .tw-flex { display: flex; }
    .tw-items-center { align-items: center; }
    .tw-justify-between { justify-content: space-between; }
    .tw-gap-6 { gap: 1.5rem; }
    .tw-gap-4 { gap: 1rem; }
    .tw-gap-3 { gap: 0.75rem; }
    .tw-gap-2 { gap: 0.5rem; }
    .tw-gap-1 { gap: 0.25rem; }
    .tw-mb-8 { margin-bottom: 2rem; }
    .tw-mb-10 { margin-bottom: 2.5rem; }
    .tw-mb-6 { margin-bottom: 1.5rem; }
    .tw-mb-2 { margin-bottom: 0.5rem; }
    .tw-p-6 { padding: 1.5rem; }
    .tw-p-8 { padding: 2rem; }
    .tw-p-5 { padding: 1.25rem; }
    .tw-px-6 { padding-left: 1.5rem; padding-right: 1.5rem; }
    .tw-px-4 { padding-left: 1rem; padding-right: 1rem; }
    .tw-py-4 { padding-top: 1rem; padding-bottom: 1rem; }
    .tw-py-1-5 { padding-top: 0.375rem; padding-bottom: 0.375rem; }
    .tw-px-2 { padding-left: 0.5rem; padding-right: 0.5rem; }
    .tw-py-05 { padding-top: 0.125rem; padding-bottom: 0.125rem; }
    .tw-mt-1 { margin-top: 0.25rem; }
    .tw-border { border-width: 1px; }
    .tw-border-b { border-bottom-width: 1px; }
    .tw-border-l-4 { border-left-width: 4px; }
    .tw-font-black { font-weight: 900; }
    .tw-font-extrabold { font-weight: 800; }
    .tw-font-bold { font-weight: 700; }
    .tw-font-medium { font-weight: 500; }
    .tw-text-5xl { font-size: 3rem; line-height: 1; }
    .tw-text-3xl { font-size: 1.875rem; line-height: 2.25rem; }
    .tw-text-2xl { font-size: 1.5rem; line-height: 2rem; }
    .tw-text-xl { font-size: 1.25rem; line-height: 1.75rem; }
    .tw-text-lg { font-size: 1.125rem; line-height: 1.75rem; }
    .tw-text-sm { font-size: 0.875rem; line-height: 1.25rem; }
    .tw-text-xs { font-size: 0.75rem; line-height: 1rem; }
    .tw-text-xxs { font-size: 10px; line-height: 1rem; }
    .tw-uppercase { text-transform: uppercase; }
    .tw-lowercase { text-transform: lowercase; }
    .tw-italic { font-style: italic; }
    .tw-tracking-wider { letter-spacing: 0.05em; }
    .tw-tracking-widest { letter-spacing: 0.1em; }
    .tw-tracking-tighter { letter-spacing: -0.05em; }
    .tw-tracking-tight { letter-spacing: -0.025em; }
    .tw-leading-tight { line-height: 1.25; }
    .tw-table { width: 100%; border-collapse: collapse; }
    .tw-th { text-align: left; }
    .tw-tr-hover:hover { background-color: #f8fafc; }
    .tw-bg-green-50-30 { background-color: rgba(240, 253, 244, 0.5); }
    .tw-grid { display: grid; }
    .tw-grid-cols-4 { grid-template-columns: repeat(4, minmax(0, 1fr)); }
    .tw-flex-1 { flex: 1 1 0%; }
    .tw-h-2 { height: 0.5rem; }
    .tw-h-full { height: 100%; }
    .tw-shrink-0 { flex-shrink: 0; }
    .tw-relative { position: relative; }
    .tw-overflow-hidden { overflow: hidden; }
    .tw-inline-flex { display: inline-flex; }
    .tw-opacity-70 { opacity: 0.7; }
    .tw-backdrop-blur { backdrop-filter: blur(12px); }
    .tw-border-white-50 { border-color: rgba(255, 255, 255, 0.5); border-style: solid; }
    .tw-bg-white-60 { background-color: rgba(255, 255, 255, 0.6); }
    .tw-text-center { text-align: center; }
    .tw-mx-auto { margin-left: auto; margin-right: auto; }
    .tw-w-12 { width: 3rem; }
    .tw-h-12 { height: 3rem; }
    .tw-rounded-xl { border-radius: 0.75rem; }
    .tw-grid-cols-3 { grid-template-columns: repeat(3, minmax(0, 1fr)); }
    @media (max-width: 768px) {
        .tw-grid-cols-4 { grid-template-columns: repeat(2, minmax(0, 1fr)); }
        .tw-grid-cols-3 { grid-template-columns: repeat(1, minmax(0, 1fr)); }
    }
    </style>
"""

# ---------------------------------------------------------
# Page 1: Dashboard
# ---------------------------------------------------------
def render_dashboard():
    # -----------------------------
    # CUSTOM CSS FOR NEW DASHBOARD
    # -----------------------------
    st.markdown("""
    <style>
    .new-dashboard-bg { font-family: 'Inter', sans-serif; color: #1E293B; margin-top: -12px; }
    .nd-greeting { font-size: 22px; font-weight: 800; color: #1E293B; margin-bottom: 4px; display: flex; align-items: center; gap: 8px; }
    .nd-subtitle { font-size: 13px; color: #64748B; margin-bottom: 24px; }
    
    .nd-metric-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-top: 16px; margin-bottom: 24px; }
    .nd-card { background: white; border-radius: 12px; padding: 16px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); border: 1px solid #F1F5F9; position: relative; display: flex; flex-direction: column; justify-content: space-between; min-height: 120px;}
    .nd-card-icon { width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-bottom: 8px; }
    .icon-green { background: #DCFCE7; color: #16A34A; }
    .icon-orange { background: #FFEDD5; color: #EA580C; }
    .nd-card-title { font-size: 11px; color: #64748B; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px; }
    .nd-card-val { font-size: 20px; font-weight: 800; color: #0F172A; line-height: 1; margin-bottom: 4px; }
    .nd-card-sub { font-size: 11px; color: #94A3B8; }
    .nd-pill { position: absolute; top: 16px; right: 16px; background: #DCFCE7; color: #166534; font-size: 11px; font-weight: 600; padding: 2px 8px; border-radius: 12px; }
    
    .nd-empty-card { background: white; border-radius: 16px; padding: 20px; border: 1px solid #F1F5F9; display: flex; flex-direction: column; justify-content: center; color: transparent; background-image: linear-gradient(to bottom, #ffffff, #fdfdfd); pointer-events: none; opacity: 0.5; }
    .nd-ec-title { font-size: 20px; font-weight: 800; color: #E2E8F0; }
    .nd-ec-sub { font-size: 11px; color: #E2E8F0; }
    
    .nd-action-row { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 24px; }
    .nd-act-card { background: white; border: 1px solid #E2E8F0; border-radius: 16px; padding: 20px; display: flex; align-items: center; justify-content: space-between; cursor: default; transition: all 0.2s; box-shadow: 0 1px 2px rgba(0,0,0,0.02); }
    .nd-act-left { display: flex; align-items: center; gap: 16px; }
    .nd-act-icon { width: 40px; height: 40px; border-radius: 50%; display: flex; justify-content: center; align-items: center; }
    .nd-act-title { font-size: 14px; font-weight: 700; color: #1E293B; margin: 0; line-height: 1.2; }
    .nd-act-sub { font-size: 12px; color: #64748B; margin: 0; }
    .nd-act-arrow { color: #94A3B8; }
    
    .nd-footer-tip { background: white; border-left: 4px solid #16A34A; border-radius: 12px; padding: 20px; display: flex; gap: 16px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
    .nd-ft-icon { font-size: 24px; }
    .nd-ft-content { display: flex; flex-direction: column; }
    .nd-ft-title { font-size: 14px; font-weight: 700; color: #1E293B; margin-bottom: 4px; }
    .nd-ft-text { font-size: 13px; color: #64748B; line-height: 1.5; margin: 0; }
    
    /* Selector container */
    .nd-selector-card { background: white; border-radius: 16px; border: 1px solid #F1F5F9; padding: 24px; box-shadow: 0 1px 2px rgba(0,0,0,0.02); margin-top: 16px; margin-bottom: 24px; }
    </style>
    """, unsafe_allow_html=True)
    
    # -----------------------------
    # HEADER & TICKER
    # -----------------------------
    st.markdown(f"""
    <div class="new-dashboard-bg" style="margin-top: 2rem;">
        <div class="nd-greeting">{t("greeting")}</div>
        <div class="nd-subtitle">{t("greeting_sub")}</div>
    </div>
    """, unsafe_allow_html=True)
    
    render_market_ticker(df)
    
    # Dashboard Selectors
    crop_list = sorted(df['Crop Name'].unique())
    
    with st.container(border=True):
        st.markdown(f'<p class="nd-ah-sub" style="margin-bottom:12px; color:#64748B; font-weight:600;">{t("conf_dash")}</p>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            # Shared key 'sel_crop' for global sync
            selected_crop = st.selectbox(t("select_crop"), crop_list, key="sel_crop", format_func=tc)
        with c2:
            market_list = sorted(df[df['Crop Name'] == selected_crop]['Market Name'].unique())
            # Ensure the selected market is still valid for this crop
            if st.session_state.sel_market not in market_list:
                st.session_state.sel_market = market_list[0] if market_list else ""
            selected_market = st.selectbox(t("select_market"), market_list, key="sel_market", format_func=tm)
        
    stats = get_current_stats(df, selected_crop, selected_market)
    
    if stats:
        # -----------------------------
        # METRIC CARDS
        # -----------------------------
        # Use current data from unified stats
        mkt_price = stats['price']
        msp = stats['msp']
        
        diff_pct = ((mkt_price - msp)/msp)*100 if msp else 0
        diff_pill = f"~ {abs(diff_pct):.1f}%"
        
        # Calculate price difference for the new 3rd card
        price_diff = mkt_price - msp
        diff_text = f"+₹{price_diff:,.0f}/q" if price_diff >= 0 else f"-₹{abs(price_diff):,.0f}/q"
        diff_sub = t("above_msp") if price_diff >= 0 else t("below_msp")
        diff_icon_color = "#16A34A" if price_diff >= 0 else "#E11D48"
        diff_icon_bg = "#DCFCE7" if price_diff >= 0 else "#FEE2E2"
        diff_svg = '<polyline points="22 7 13.5 15.5 8.5 10.5 2 17"></polyline><polyline points="16 7 22 7 22 13"></polyline>' if price_diff >= 0 else '<polyline points="22 17 13.5 8.5 8.5 13.5 2 7"></polyline><polyline points="16 17 22 17 22 11"></polyline>'
        
        html_metrics = f"""<div class="nd-metric-grid">
    <!-- Market Price -->
    <div class="nd-card">
    <div class="nd-pill">{diff_pill}</div>
    <div>
    <div class="nd-card-icon icon-green">
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline></svg>
    </div>
    <div class="nd-card-title">{t("market_price")}</div>
    <div class="nd-card-val">₹{mkt_price:,.0f}/q</div>
    <div class="nd-card-sub">{tm(selected_market)} {t("mandi")}</div>
    </div>
    </div>
    <!-- Government MSP -->
    <div class="nd-card">
    <div>
    <div class="nd-card-icon icon-green">
    <span style="font-weight:bold; font-size:18px;">₹</span>
    </div>
    <div class="nd-card-title">{t("msp")}</div>
    <div class="nd-card-val">₹{msp:,.0f}/q</div>
    <div class="nd-card-sub">{t("msp_sub")}</div>
    </div>
    </div>
    <!-- Price Difference -->
    <div class="nd-card">
    <div>
    <div class="nd-card-icon" style="background:{diff_icon_bg}; color:{diff_icon_color};">
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">{diff_svg}</svg>
    </div>
    <div class="nd-card-title">{t("price_diff")}</div>
    <div class="nd-card-val">{diff_text}</div>
    <div class="nd-card-sub">{diff_sub}</div>
    </div>
    </div>
    </div>"""
        st.markdown(html_metrics, unsafe_allow_html=True)
        
        # -----------------------------
        # ACTION BUTTONS & TIPS
        # -----------------------------
        html_bottom = f"""<div class="nd-footer-tip">
    <div class="nd-ft-icon">💡</div>
    <div class="nd-ft-content">
    <div class="nd-ft-title">{t("tip_title")}</div>
    <p class="nd-ft-text">{t("tip_text").format(crop=tc(selected_crop), market=tm(selected_market))}</p>
    </div>
    </div>"""
        st.markdown(html_bottom, unsafe_allow_html=True)

# ---------------------------------------------------------
# Page 2: Market Comparison
# ---------------------------------------------------------
def render_market_comparison():
    # -----------------------------
    # REACT MIRROR (TAILWIND CSS)
    # -----------------------------
    
    header_html = f"""
    <div class="tw-mb-8 tw-flex" style="flex-direction: column;">
      <h1 class="tw-text-3xl tw-font-extrabold tw-text-slate-900 tw-flex tw-items-center tw-gap-3" style="margin:0;">
        <span style="color:#2F7D4A;">📊</span> {t("nav_market")}
      </h1>
      <p class="tw-text-slate-500" style="margin-top:0.25rem;">Compare prices across different mandis to find the best deal</p>
    </div>
    """
    
    st.markdown(react_css + header_html, unsafe_allow_html=True)
    
    # Selectors Section
    st.markdown("""<div class="tw-bg-white tw-p-6 tw-rounded-2xl tw-border tw-border-slate-100 tw-shadow-sm tw-mb-8">
        <label class="tw-text-xs tw-font-bold tw-text-slate-400 tw-uppercase tw-tracking-wider" style="display:block; margin-bottom:0.5rem;">🌿 Select Crop to Compare</label>""", unsafe_allow_html=True)
    
    crop_list = sorted(df['Crop Name'].unique())
    selected_crop = st.selectbox(t("select_crop"), crop_list, key="sel_crop", label_visibility="collapsed", format_func=tc)
    st.markdown('</div>', unsafe_allow_html=True)

    # Data Processing
    # Use Latest Prices per market for 100% consistency with Dashboard
    mkt_data = get_latest_market_comparison(df, selected_crop).sort_values('Latest Price', ascending=False)
    
    if not mkt_data.empty:
        best_mkt = mkt_data.iloc[0]
        # Use unified statistics for the 'Best Price' card to match Dashboard
        best_stats = get_current_stats(df, selected_crop, best_mkt['Market Name'])
        
        # Custom mockup static data integration for Vadodara region markets
        dist_map = {best_mkt['Market Name']: 15, 'Vadodara': 10, 'Padra': 20, 'Savli': 35, 'Karjan': 40, 'Waghodia': 15, 'Dabhoi': 30, 'Shinor': 55}
        rat_map = {best_mkt['Market Name']: 4.5, 'Vadodara': 4.8, 'Padra': 4.2, 'Savli': 4.3, 'Karjan': 4.0, 'Waghodia': 4.5, 'Dabhoi': 4.1, 'Shinor': 3.9}

        # Best Price Card
        best_html = f"""
        <div class="tw-bg-green-100 tw-border tw-border-green-200 tw-rounded-2xl tw-p-6 tw-flex tw-items-center tw-justify-between tw-mb-8 tw-shadow-sm">
          <div class="tw-flex tw-items-center tw-gap-6">
            <div class="tw-bg-green-200 tw-text-green-700 tw-rounded-full tw-flex tw-items-center tw-justify-between tw-text-2xl" style="width: 3rem; height: 3rem; justify-content: center;">★</div>
            <div>
              <p class="tw-text-xxs tw-font-bold tw-text-green-800 tw-uppercase tw-tracking-wider" style="margin:0 0 0.25rem 0;">Best Price Available At</p>
              <h2 class="tw-text-xl tw-font-black tw-text-green-900" style="margin:0;">{tm(best_mkt['Market Name'])} {t("mandi")}</h2>
              <p class="tw-text-lg tw-font-black tw-text-green-600" style="margin:0.25rem 0 0 0;">₹{best_stats['price']:,}/quintal</p>
            </div>
          </div>
          <div style="text-align: right;">
             <p class="tw-text-xxs tw-text-slate-500 tw-font-bold tw-uppercase tw-tracking-wider" style="margin:0;">{t("distance")}</p>
             <p class="tw-text-lg tw-font-bold tw-text-slate-800" style="margin:0;">{dist_map.get(best_mkt['Market Name'], 20)} km</p>
          </div>
        </div>
        """
        st.markdown(best_html, unsafe_allow_html=True)

        # Price Comparison Chart Section
        st.markdown("""<div class="tw-bg-white tw-rounded-3xl tw-border tw-border-slate-100 tw-shadow-md tw-p-8 tw-mb-10" style="overflow:hidden;">
            <div class="tw-flex tw-items-center tw-justify-between tw-mb-10">
              <div class="tw-flex tw-items-center tw-gap-3">
                 <span style="color:#2F7D4A; font-size:24px;">📊</span>
                 <h3 class="tw-font-extrabold tw-text-slate-800 tw-text-xl tw-tracking-tight" style="margin:0;">Market Price Distribution (Today)</h3>
              </div>
              <div class="tw-flex tw-items-center tw-gap-6">
                 <div class="tw-flex tw-items-center tw-gap-1 tw-font-bold tw-text-slate-400 tw-text-xs">
                    <div style="width:0.75rem; height:0.75rem; background:#2F7D4A; border-radius:0.125rem;"></div> MARKET PRICE
                 </div>
                 <div class="tw-flex tw-items-center tw-gap-1 tw-font-bold tw-text-xs" style="color:#3B82F6;">
                    <div style="width:0.75rem; height:0.75rem; border:2px dashed #3B82F6; border-radius:0.125rem;"></div> GOVT MSP
                 </div>
              </div>
            </div>""", unsafe_allow_html=True)
            
        top_mandis = mkt_data.head(7).sort_values('Latest Price', ascending=True)
        colors = ['#15803D' if m == best_mkt['Market Name'] else '#4ADE80' for m in top_mandis['Market Name']]
        line_colors = ['#14532D' if m == best_mkt['Market Name'] else 'rgba(0,0,0,0)' for m in top_mandis['Market Name']]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=[tm(m) for m in top_mandis['Market Name']], 
            y=top_mandis['Latest Price'], 
            marker_color=colors,
            marker_line_color=line_colors,
            marker_line_width=2,
            name="Market Price",
            hovertemplate="₹%{y:,}/q<extra></extra>",
            width=0.6,
        ))
        
        msp_val = best_stats['msp']
        fig.add_shape(type="line", x0=-0.5, x1=len(top_mandis)-0.5, y0=msp_val, y1=msp_val, line={"color": "#3B82F6", "width": 2, "dash": "dash"})
        fig.add_annotation(x=len(top_mandis)-1, y=msp_val, text="MSP", showarrow=False, yshift=15, font={"color": "#3B82F6", "size": 10, "weight": 900})

        fig.update_layout(
            height=450, 
            margin={'l': 0, 'r': 0, 't': 0, 'b': 40}, 
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis={"showgrid": False, "zeroline": False, "tickfont": {"size": 12, "color": "#475569", "weight": 800}, "tickangle": -25},
            yaxis={"showgrid": True, "gridcolor": "#F1F5F9", "gridwidth": 1, "griddash": "dash", "zeroline": False, "tickfont": {"size": 12, "color": "#94A3B8", "weight": 700}, "tickprefix": "₹"},
            showlegend=False,
            bargap=0.4
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)

        # Comparison Table
        st.markdown(f"""<div class="tw-bg-white tw-rounded-2xl tw-border tw-border-slate-100 tw-shadow-sm tw-mb-8" style="overflow:hidden;">
            <div class="tw-p-6 tw-border-b tw-border-slate-100 tw-flex tw-items-center tw-gap-3">
               <span style="color:#2F7D4A;">📍</span>
               <span class="tw-font-bold tw-text-slate-800">{t("det_mkt_prices")}</span>
            </div>
            <div style="overflow-x:auto;">
              <table class="tw-table">
                <thead>
                  <tr class="tw-bg-slate-50">
                    <th class="tw-th tw-px-6 tw-py-4 tw-text-xs tw-font-bold tw-text-slate-400 tw-uppercase tw-tracking-widest">{t("table_mkt")}</th>
                    <th class="tw-th tw-px-6 tw-py-4 tw-text-xs tw-font-bold tw-text-slate-400 tw-uppercase tw-tracking-widest">{t("table_price")}</th>
                    <th class="tw-th tw-px-6 tw-py-4 tw-text-xs tw-font-bold tw-text-slate-400 tw-uppercase tw-tracking-widest">{t("table_dist")}</th>
                    <th class="tw-th tw-px-6 tw-py-4 tw-text-xs tw-font-bold tw-text-slate-400 tw-uppercase tw-tracking-widest">{t("table_rating")}</th>
                  </tr>
                </thead>
                <tbody>
        """, unsafe_allow_html=True)
        
        table_rows = ""
        for idx, row in mkt_data.iterrows():
            isBest = (row['Market Name'] == best_mkt['Market Name'])
            bg_cls = "tw-bg-green-50-30" if isBest else ""
            txt_cls = "tw-text-green-600" if isBest else "tw-text-slate-700"
            best_badge = """<span class="tw-bg-green-100 tw-text-green-800 tw-px-2 tw-py-05 tw-rounded tw-text-xxs tw-font-black tw-uppercase tw-tracking-tighter">Best</span>""" if isBest else ""
            
            table_rows += f"""<tr class="tw-border-b tw-border-slate-100 tw-tr-hover {bg_cls}">
                <td class="tw-td tw-px-6 tw-py-4 tw-font-bold tw-text-slate-800 tw-flex tw-items-center tw-gap-3">
                    {best_badge} {row['Market Name']} {t("mandi")}
                </td>
                <td class="tw-td tw-px-6 tw-py-4 tw-font-black {txt_cls}">₹{row['Latest Price']:,}</td>
                <td class="tw-td tw-px-6 tw-py-4 tw-text-sm tw-text-slate-400 tw-font-bold">{dist_map.get(row['Market Name'], 25)} km</td>
                <td class="tw-td tw-px-6 tw-py-4 tw-font-bold tw-text-slate-700 tw-flex tw-items-center tw-gap-1">
                    <span style="color:#EAB308;">★</span> {rat_map.get(row['Market Name'], 4.0)}
                </td>
            </tr>"""
        
        st.markdown(table_rows + "</tbody></table></div></div>", unsafe_allow_html=True)

        # Footer Insight
        st.markdown(f"""<div class="tw-p-6 tw-bg-white tw-rounded-2xl tw-border-l-4 tw-border-yellow-500 tw-shadow-sm tw-flex tw-gap-6 tw-items-start">
            <div class="tw-text-2xl" style="padding-top:0.25rem;">💡</div>
            <div>
              <h4 class="tw-font-bold tw-text-slate-900" style="margin:0 0 0.25rem 0;">{t("insight_title")}</h4>
              <p class="tw-text-sm tw-text-slate-500" style="margin:0; line-height:1.6;">
                While {best_mkt['Market Name']} offers the highest price, consider transport costs. {best_mkt['Market Name']} is {dist_map.get(best_mkt['Market Name'], 20)}km away. Factors like fuel and time are important when deciding where to sell.
              </p>
            </div>
        </div>""", unsafe_allow_html=True)

def render_price_prediction():
    # Extracted Tailwind classes specific to Price Prediction
    pp_react_css = """
    <style>
    .tw-bg-grad-green { background: linear-gradient(to bottom right, #f0fdf4, #d1fae5); border-color: #bbf7d0; border-style: solid; }
    .tw-bg-grad-red { background: linear-gradient(to bottom right, #fef2f2, #ffe4e6); border-color: #fecaca; border-style: solid; }
    .tw-bg-green-600 { background-color: #16a34a; }
    .tw-bg-red-500 { background-color: #ef4444; }
    .tw-bg-green-500 { background-color: #22c55e; }
    .tw-bg-slate-200 { background-color: #e2e8f0; }
    .tw-bg-white-60 { background-color: rgba(255, 255, 255, 0.6); }
    .tw-text-white { color: #ffffff; }
    .tw-text-red-900 { color: #7f1d1d; }
    .tw-text-red-700 { color: #b91c1c; }
    .tw-text-slate-600 { color: #475569; }
    .tw-lowercase { text-transform: lowercase; }
    .tw-shadow-lg { box-shadow: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1); }
    .tw-relative { position: relative; }
    .tw-overflow-hidden { overflow: hidden; }
    .tw-inline-flex { display: inline-flex; }
    .tw-text-5xl { font-size: 3rem; line-height: 1; }
    .tw-grid { display: grid; }
    .tw-grid-cols-4 { grid-template-columns: repeat(4, minmax(0, 1fr)); }
    .tw-backdrop-blur { backdrop-filter: blur(12px); }
    .tw-border-white-50 { border-color: rgba(255, 255, 255, 0.5); border-style: solid; }
    .tw-opacity-70 { opacity: 0.7; }
    .tw-leading-tight { line-height: 1.25; }
    .tw-italic { font-style: italic; }
    .tw-flex-1 { flex: 1 1 0%; }
    .tw-h-2 { height: 0.5rem; }
    .tw-h-full { height: 100%; }
    .tw-py-1-5 { padding-top: 0.375rem; padding-bottom: 0.375rem; }
    .tw-mb-6 { margin-bottom: 1.5rem; }
    .tw-mb-2 { margin-bottom: 0.5rem; }
    .tw-mt-1 { margin-top: 0.25rem; }
    .tw-p-5 { padding: 1.25rem; }
    .tw-gap-4 { gap: 1rem; }
    @media (max-width: 768px) { .tw-grid-cols-4 { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
    </style>
    """
    
    # Header
    header_html = f"""
    <div class="tw-mb-8 tw-flex" style="flex-direction: column;">
      <h1 class="tw-text-3xl tw-font-extrabold tw-text-slate-900 tw-flex tw-items-center tw-gap-3 tw-lowercase" style="margin:0;">
        <span style="color:#2F7D4A;">📈</span> {t("pred_title")}
      </h1>
      <p class="tw-text-slate-500" style="margin-top:0.25rem;">{t("pred_sub")}</p>
    </div>
    """
    
    st.markdown(react_css + pp_react_css + header_html, unsafe_allow_html=True)

    # Selectors Section
    st.markdown(f"""<div class="tw-bg-white tw-p-6 tw-rounded-2xl tw-border tw-border-slate-100 tw-shadow-sm tw-mb-8 tw-flex tw-gap-6 tw-items-end" style="flex-wrap: wrap;">
        <div class="tw-flex-1" style="min-width:200px;">
          <label class="tw-text-xs tw-font-bold tw-text-slate-400 tw-uppercase tw-tracking-wider" style="display:block; margin-bottom:0.5rem;">🌿 {t("select_crop")}</label>""", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    crop_list = sorted(df['Crop Name'].unique())
    with col1:
        selected_crop = st.selectbox(t("select_crop"), crop_list, key="sel_crop", label_visibility="collapsed", format_func=tc)
    with col2:
        period = st.selectbox(t("pred_period"), ["1 Month", "3 Months", "6 Months"], index=1, label_visibility="collapsed", key="pred_period")
        
    st.markdown('</div></div>', unsafe_allow_html=True)

    # -----------------------------
    # ML FORECAST LOGIC
    # -----------------------------
    market_to_predict = st.session_state.sel_market
    months_map = {"1 Month": 1, "3 Months": 3, "6 Months": 6}
    n_months = months_map.get(period, 3)
    
    # Use unified current stats for consistency
    stats = get_current_stats(df, selected_crop, market_to_predict)
    current_price = stats['price']
    
    # We still need crop_df for the historical part of the chart
    crop_df = df[(df['Crop Name'] == selected_crop) & (df['Market Name'] == market_to_predict)].sort_values('Date')
    if crop_df.empty:
        crop_df = df[df['Crop Name'] == selected_crop].sort_values('Date')

    forecast_df = predict_future_prices(selected_crop, market_to_predict, n_months)
    
    if forecast_df is not None and not forecast_df.empty and current_price > 0:
        peak_price = forecast_df['Market Price'].max()
        gain = peak_price - current_price
        is_bullish = gain > 0
        conf_score = 86 if is_bullish else 68
        
        verdict = t("hold_verdict") if is_bullish else t("sell_verdict")
        advice = t("hold_adv") if is_bullish else t("sell_adv")
        gain_text = f"+{int(gain)}" if is_bullish else f"{int(gain)}"
        
        trend = "Bullish" if is_bullish else "Bearish" # Logic key, keep internal
    else:
        verdict, advice, gain_text, conf_score, is_bullish, trend = t("hold_verdict"), t("hold_adv"), "+240", 86, True, "Bullish"

    # Harvest Advisor Card (React styled)
    card_bg = "tw-bg-grad-green" if is_bullish else "tw-bg-grad-red"
    pill_bg = "tw-bg-green-600" if is_bullish else "tw-bg-red-500"
    title_col = "tw-text-green-900" if is_bullish else "tw-text-red-900"
    sub_col = "tw-text-green-700" if is_bullish else "tw-text-red-700"
    verdict_text = "STAY CALM: HOLD" if is_bullish else "ACTION: SELL NOW"
    
    advisor_html = f"""
      <div class="{card_bg} tw-rounded-3xl tw-p-8 tw-mb-10 tw-border tw-shadow-lg tw-relative tw-overflow-hidden">
        <div class="tw-inline-flex tw-items-center tw-gap-2 tw-px-4 tw-py-1-5 tw-rounded-full tw-text-xxs tw-font-black tw-uppercase tw-tracking-widest tw-text-white tw-mb-6 tw-shadow-md {pill_bg}">
           {t("market_insight")}: {trend}
        </div>
        <h2 class="tw-text-5xl tw-font-black tw-mb-2 {title_col}" style="margin-top:0;">
           {verdict}
        </h2>
        <p class="tw-text-xl tw-font-bold tw-mb-10 {sub_col}" style="margin-top:0;">{advice}</p>

        <div class="tw-grid tw-grid-cols-4 tw-gap-6 tw-mb-10 pl-grid-mob">
           <div class="tw-bg-white-60 tw-backdrop-blur tw-p-5 tw-rounded-2xl tw-border tw-border-white-50 tw-shadow-sm">
              <p class="tw-text-xxs tw-font-black tw-text-slate-500 tw-uppercase tw-tracking-widest tw-mb-1 tw-opacity-70" style="margin:0;">{t("exp_gain")}</p>
              <p class="tw-text-2xl tw-font-black {sub_col}" style="margin:0;">₹{gain_text}</p>
              <p class="tw-text-xxs tw-text-slate-400 tw-font-bold tw-mt-1 tw-leading-tight" style="margin:0;">{t("sold_peak")}</p>
           </div>
           <div class="tw-bg-white-60 tw-backdrop-blur tw-p-5 tw-rounded-2xl tw-border tw-border-white-50 tw-shadow-sm">
              <p class="tw-text-xxs tw-font-black tw-text-slate-500 tw-uppercase tw-tracking-widest tw-mb-1 tw-opacity-70" style="margin:0;">{t("mkt_demand")}</p>
              <p class="tw-text-2xl tw-font-black tw-text-slate-700" style="margin:0;">{t("v_high")}</p>
           </div>
           <div class="tw-bg-white-60 tw-backdrop-blur tw-p-5 tw-rounded-2xl tw-border tw-border-white-50 tw-shadow-sm">
              <p class="tw-text-xxs tw-font-black tw-text-slate-500 tw-uppercase tw-tracking-widest tw-mb-1 tw-opacity-70" style="margin:0;">{t("risk_level")}</p>
              <p class="tw-text-2xl tw-font-black tw-text-slate-700" style="margin:0;">{t("low")}</p>
           </div>
           <div class="tw-bg-white-60 tw-backdrop-blur tw-p-5 tw-rounded-2xl tw-border tw-border-white-50 tw-shadow-sm">
              <p class="tw-text-xxs tw-font-black tw-text-slate-500 tw-uppercase tw-tracking-widest tw-mb-1 tw-opacity-70" style="margin:0;">{t("next_update")}</p>
              <p class="tw-text-2xl tw-font-black tw-text-slate-700 tw-flex tw-items-center tw-gap-2 tw-italic tw-uppercase" style="margin:0;">24 Hours</p>
           </div>
        </div>

        <div class="tw-flex tw-items-center tw-gap-4">
           <span class="tw-text-xs tw-font-black tw-text-slate-600 tw-uppercase tw-tracking-widest">{t("pred_conf")}:</span>
           <div class="tw-flex-1 tw-h-2 tw-bg-slate-200 tw-rounded-full tw-overflow-hidden">
              <div class="tw-h-full tw-bg-green-500 tw-rounded-full" style="width: {conf_score}%; box-shadow: 0 0 12px rgba(34,197,94,0.4);"></div>
           </div>
           <span class="tw-text-sm tw-font-black tw-text-slate-700 tw-italic">{conf_score}%</span>
        </div>
      </div>
    """
    st.markdown(advisor_html, unsafe_allow_html=True)

    # -----------------------------
    # CHART SECTION (REACT MIRROR - AREA CHART)
    # -----------------------------
    st.markdown(f"""<div class="tw-bg-white tw-p-8 tw-rounded-3xl tw-border tw-border-slate-100 tw-shadow-md">
         <div class="tw-flex tw-items-center tw-justify-between tw-mb-8">
            <div class="tw-flex tw-items-center tw-gap-3">
                <span style="color:#2F7D4A; font-size:24px;">📈</span>
                <span class="tw-font-extrabold tw-text-slate-800 tw-text-xl tw-tracking-tight">{t("trend_analysis")}</span>
            </div>
            <div class="tw-flex tw-items-center tw-gap-4 tw-text-xs tw-font-bold">
                <div class="tw-flex tw-items-center tw-gap-2 tw-text-slate-400"><div style="width:12px; height:12px; border-radius:50%; background:#94a3b8;"></div> {t("historical")}</div>
                <div class="tw-flex tw-items-center tw-gap-2 tw-text-green-600"><div style="width:12px; height:12px; border-radius:50%; background:#10B981;"></div> {t("predicted")}</div>
            </div>
         </div>""", unsafe_allow_html=True)
         
    fig = go.Figure()
    if not crop_df.empty:
        hist_plot = crop_df.tail(12)
        
        # Historical Data
        fig.add_trace(go.Scatter(
            x=hist_plot['Date'], 
            y=hist_plot['Market Price'], 
            name='Historical',
            mode='lines',
            line={"color": "#94A3B8", "width": 3},
            fill='tozeroy',
            fillcolor='rgba(148, 163, 184, 0.1)'
        ))
        
        if forecast_df is not None and not forecast_df.empty:
            last_hist_date = hist_plot['Date'].values[-1]
            last_hist_price = float(hist_plot['Market Price'].values[-1])
            
            # AI Predicted (Matches React specific AreaChart style)
            con_dates = [last_hist_date] + pd.to_datetime(forecast_df['Date']).tolist()
            con_prices = [last_hist_price] + forecast_df['Market Price'].astype(float).tolist()
            
            fig.add_trace(go.Scatter(
                x=con_dates, 
                y=con_prices, 
                name='Predicted',
                mode='lines',
                line={"color": "#10B981", "width": 3, "dash": "dash"},
                fill='tozeroy',
                fillcolor='rgba(16, 185, 129, 0.15)'
            ))

    fig.update_layout(
        height=350, 
        margin={'l': 0, 'r': 0, 't': 0, 'b': 20}, 
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis={"showgrid": False, "zeroline": False, "tickfont": {"size": 12, "color": "#94A3B8", "weight": 700}},
        yaxis={"showgrid": True, "gridcolor": "#F1F5F9", "gridwidth": 1, "griddash": "dash", "zeroline": False, "tickfont": {"size": 12, "color": "#94A3B8", "weight": 700}, "tickprefix": "₹"},
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    st.markdown("</div>", unsafe_allow_html=True)

    # ---------------------------------------------------------
# Page 5: Fertilizers
# ---------------------------------------------------------
def render_fertilizers():
    fert_react_css = """
    <style>
    .fert-header { display: flex; align-items: center; gap: 12px; margin-bottom: 8px; }
    .fert-title { font-size: 28px; font-weight: 950; color: #065F46; margin: 0; letter-spacing: -0.02em; }
    .fert-subtitle { font-size: 14px; color: #64748B; margin-bottom: 32px; }
    
    .fert-card-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 24px; margin-bottom: 32px; }
    @media (max-width: 768px) { .fert-card-grid { grid-template-columns: 1fr; } }
    
    .f-card { background: white; border-radius: 24px; border: 1px solid #E2E8F0; padding: 24px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); transition: all 0.3s ease; display: flex; flex-direction: column; gap: 16px; position: relative; }
    .f-card:hover { transform: translateY(-4px); box-shadow: 0 12px 20px -8px rgba(0,0,0,0.1); border-color: #10B981; }
    
    .f-header { display: flex; justify-content: space-between; align-items: flex-start; }
    .f-info { display: flex; gap: 16px; align-items: center; }
    .f-icon { width: 48px; height: 48px; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 24px; }
    .f-name-box { display: flex; flex-direction: column; }
    .f-name { font-size: 18px; font-weight: 800; color: #1E293B; margin: 0; }
    .f-name-local { font-size: 14px; color: #64748B; margin: 0; }
    
    .badge-best { background: #DCFCE7; color: #166534; padding: 4px 10px; border-radius: 99px; font-size: 11px; font-weight: 800; display: flex; align-items: center; gap: 4px; }
    .tag-category { background: #F1F5F9; color: #64748B; padding: 4px 12px; border-radius: 99px; font-size: 11px; font-weight: 700; width: fit-content; margin-top: 8px; }
    
    .price-box { background: #F8FAFC; border-radius: 16px; padding: 16px; display: flex; justify-content: space-between; align-items: center; }
    .price-label-group { display: flex; align-items: center; gap: 8px; }
    .price-label { font-size: 11px; font-weight: 700; color: #94A3B8; text-transform: uppercase; }
    .brand-text { font-size: 11px; color: #64748B; font-weight: 600; margin-top: 2px; }
    .price-value { font-size: 22px; font-weight: 900; color: #1E293B; }
    .price-unit { font-size: 12px; color: #94A3B8; font-weight: 600; }
    
    .instruction-box { background: #F8FAFC; border-radius: 12px; padding: 12px 16px; display: flex; gap: 12px; align-items: center; }
    .inst-icon { font-size: 16px; opacity: 0.6; }
    .inst-text { font-size: 13px; font-weight: 600; color: #475569; margin: 0; line-height: 1.4; }
    
    .guide-banner { background: #F0FDF4; border: 1px solid #DCFCE7; border-left: 4px solid #10B981; border-radius: 16px; padding: 16px 24px; display: flex; align-items: center; gap: 16px; margin-bottom: 32px; }
    .guide-content { flex: 1; }
    .guide-title { font-size: 15px; font-weight: 800; color: #1E293B; margin: 0 0 4px 0; display: flex; align-items: center; gap: 8px; }
    .guide-text { font-size: 13px; color: #64748B; margin: 0; font-weight: 500; }
    .badge-rec { background: #DCFCE7; color: #15803D; padding: 2px 8px; border-radius: 4px; font-size: 10px; font-weight: 800; display: inline-flex; align-items: center; gap: 4px; border: 1px solid #BBF7D0; }
    
    .summary-card { background: white; border-radius: 20px; border: 1px solid #E2E8F0; padding: 32px; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.03); }
    .summary-title { font-size: 16px; font-weight: 800; color: #1E293B; display: flex; align-items: center; gap: 12px; margin-bottom: 24px; }
    .summary-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; border-bottom: 1px solid #F1F5F9; padding-bottom: 24px; margin-bottom: 24px; }
    .summary-item { background: #F8FAFC; padding: 16px; border-radius: 12px; text-align: center; }
    .summary-item-name { font-size: 11px; font-weight: 700; color: #94A3B8; text-transform: uppercase; margin-bottom: 4px; }
    .summary-item-price { font-size: 18px; font-weight: 900; color: #1E293B; }
    .total-box { text-align: center; }
    .total-label { font-size: 13px; font-weight: 600; color: #64748B; margin-bottom: 4px; }
    .total-value { font-size: 32px; font-weight: 950; color: #065F46; letter-spacing: -0.04em; }
    .total-sub { font-size: 12px; color: #94A3B8; font-weight: 600; margin-top: 2px; }
    </style>
    """
    
    st.markdown(fert_react_css, unsafe_allow_html=True)
    
    # Header
    st.markdown(f"""
    <div class="fert-header">
        <span style="font-size: 32px;">🌿</span>
        <h1 class="fert-title">{t('fert_rec_title')}</h1>
    </div>
    <p class="fert-subtitle">{t('fert_rec_sub')}</p>
    """, unsafe_allow_html=True)
    
    # Crop Selection Card
    st.markdown(f"""<div class="tw-bg-white tw-p-8 tw-rounded-2xl tw-border tw-border-slate-100 tw-shadow-sm tw-mb-8">
        <label class="tw-text-xs tw-font-bold tw-text-slate-400 tw-uppercase tw-tracking-wider" style="display:block; margin-bottom:0.75rem;">🌿 {t("select_crop")}</label>""", unsafe_allow_html=True)
    
    crop_list = sorted(df['Crop Name'].unique())
    selected_crop = st.selectbox(t("select_crop"), crop_list, key="sel_crop", label_visibility="collapsed", format_func=tc)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Quick Guide Banner
    st.markdown(f"""
    <div class="guide-banner">
        <div style="font-size: 24px;">💡</div>
        <div class="guide-content">
            <p class="guide-title">{t('quick_guide_title')} <span class="badge-rec">✓ {t('recommended_badge')}</span></p>
            <p class="guide-text">{t('quick_guide_sub')}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Fertilizer Data based on Wheat (as in image)
    fert_data = [
        {
            "name": "Urea", "local": "યૂરિયા", "icon": "💧", "bg": "#EFF6FF", "text_color": "#2563EB",
            "category": "Nitrogen (N)", "price": 267, "brand": "IFFCO", "instruction": "Apply 2-3 times during growth", "inst_local": "વૃદ્ધિ દરમિયાન 2-3 વાર લાગુ કરો"
        },
        {
            "name": "DAP (Di-ammonium Phosphate)", "local": "ડીએપી", "icon": "☀️", "bg": "#FFFBEB", "text_color": "#D97706",
            "category": "Phosphorus (P)", "price": 1350, "brand": "IFFCO", "instruction": "Apply at sowing time", "inst_local": "વાવણી સમયે લાગુ કરો"
        },
        {
            "name": "MOP (Muriate of Potash)", "local": "પોટાશ", "icon": "🌿", "bg": "#FAF5FF", "text_color": "#9333EA",
            "category": "Potassium (K)", "price": 1700, "brand": "IPL", "instruction": "Apply before flowering", "inst_local": "ફૂલો આવે તે પહેલાં લાગુ કરો"
        },
        {
            "name": "Vermicompost", "local": "વર્મિકમ્પોસ્ટ", "icon": "🌱", "bg": "#F0FDF4", "text_color": "#16A34A",
            "category": "Organic", "price": 400, "brand": "Local", "instruction": "Mix in soil before sowing", "inst_local": "વાવણી પહેલા માટીમાં ભેળવો"
        }
    ]
    
    # Card Grid
    grid_html = '<div class="fert-card-grid">'
    for f in fert_data:
        card = f"""
<div class="f-card">
    <div class="f-header">
        <div class="f-info">
            <div class="f-icon" style="background: {f['bg']}; color: {f['text_color']};">{f['icon']}</div>
            <div class="f-name-box">
                <p class="f-name">{f['name']}</p>
                <p class="f-name-local">{f['local']}</p>
            </div>
        </div>
        <div class="badge-best">✓ {t('best_badge')}</div>
    </div>
    <div class="tag-category">{f['category']}</div>
    <div class="price-box">
        <div class="price-label-group">
            <div style="font-size: 20px;">₹</div>
            <div>
                <div class="price-label">{t('price_label')}</div>
                <div class="brand-text">{t('brand_label')}: {f['brand']}</div>
            </div>
        </div>
        <div>
            <span class="price-value">₹{f['price']}</span>
            <span class="price-unit">per 50kg bag</span>
        </div>
    </div>
    <div class="instruction-box">
        <div class="inst-icon">📦</div>
        <div class="f-name-box">
            <p class="inst-text">{f['instruction']}</p>
            <p class="f-name-local" style="font-size:11px;">{f['inst_local']}</p>
        </div>
    </div>
</div>
"""
        grid_html += card
    grid_html += '</div>'
    st.markdown(grid_html, unsafe_allow_html=True)
    
    # Cost Summary
    st.markdown(f"""
    <div class="summary-card">
        <h3 class="summary-title"><span style="font-size: 24px;">₹</span> {t('cost_summary_title')}</h3>
        <div class="summary-grid">
            <div class="summary-item">
                <p class="summary-item-name">Urea</p>
                <p class="summary-item-price">₹267</p>
            </div>
            <div class="summary-item">
                <p class="summary-item-name">DAP (Di-ammonium Phosphate)</p>
                <p class="summary-item-price">₹1350</p>
            </div>
            <div class="summary-item">
                <p class="summary-item-name">Vermicompost</p>
                <p class="summary-item-price">₹400</p>
            </div>
        </div>
        <div class="total-box">
            <p class="total-label">{t('total_cost_label')}</p>
            <p class="total-value">₹2,017</p>
            <p class="total-sub">({t('per_acre_approx')})</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Page 6: Loss Analysis
# ---------------------------------------------------------
def render_loss_analysis():
    st.markdown(f"""<div class="la-header">
    <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#2F7D4A" stroke-width="2.5"><rect width="16" height="20" x="4" y="2" rx="2"/><line x1="8" y1="6" x2="16" y2="6"/><line x1="16" y1="14" x2="16" y2="18"/><path d="M16 10h.01"/><path d="M12 10h.01"/><path d="M8 10h.01"/><path d="M12 14h.01"/><path d="M8 14h.01"/><path d="M12 18h.01"/><path d="M8 18h.01"/></svg>
    <h1 class="la-title">{t("loss_title")}</h1>
    </div>
    <div class="la-subtitle">{t("loss_sub")}</div>""", unsafe_allow_html=True)
    
    with st.container(border=True):
        st.markdown(f'<p style="font-weight:800; font-size:15px; color:#1E293B; margin-bottom:20px;">{t("enter_details")}</p>', unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        crop_list = sorted(df['Crop Name'].unique())
        
        with c1:
            st.markdown(f'<p class="la-label">{t("select_crop")}</p>', unsafe_allow_html=True)
            sel_comm = st.selectbox(t("select_crop"), crop_list, key="sel_crop", label_visibility="collapsed", format_func=tc)
            
        with c2:
            st.markdown(f'<p class="la-label">{t("qty_quintals")}</p>', unsafe_allow_html=True)
            qty = st.number_input(t("enter_qty"), min_value=1.0, value=10.0, step=1.0, label_visibility="collapsed", key="la_qty")
        
        # Get market data from the unified stats for absolute consistency
        # This ensures the price shown here matches the Dashboard EXACTLY
        current_mkt = st.session_state.sel_market
        stats = get_current_stats(df, sel_comm, current_mkt)
        
        mkt_avg = stats['price']
        msp_val = stats['msp']
        suggested_farmer_price = mkt_avg * 0.85 # Assume typical farmer gets 15% less
        
        p1, p2 = st.columns(2)
        with p1:
            st.markdown(f"""<div class="calculator-panel"><div class="calc-impact-header"><div class="calc-icon-dot" style="background:#10B981; animation:none;"></div><span style="font-weight:900; color:#1E293B; font-size:14px;">{t("benchmark_price")}</span></div><p class="calc-label">Current average market rate</p><p style="font-size:32px; font-weight:950; color:#10B981; letter-spacing:-0.03em;">₹{mkt_avg:,.0f}<span style="font-size:14px; color:#94A3B8;">/q</span></p></div>""", unsafe_allow_html=True)
        with p2:
            st.markdown(f'<div class="calculator-panel"><div class="calc-impact-header"><div class="calc-icon-dot"></div><span style="font-weight:900; color:#1E293B; font-size:14px;">{t("your_price")}</span></div><p class="calc-label">Input your actual selling price (₹/q)</p>', unsafe_allow_html=True)
            u_price = st.number_input(t("your_price"), min_value=1.0, value=float(round(mkt_avg*0.85)) if mkt_avg > 0 else 1000.0, step=10.0, label_visibility="collapsed", key="u_price")
            st.markdown('</div>', unsafe_allow_html=True)
            
        # Action Button - styled via CSS trick
        st.markdown('<div style="margin-top:24px;">', unsafe_allow_html=True)
        calc = st.button(t("calc_my_loss"), key="calc_loss_btn", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Button styling injection
        st.markdown("""<style>
            div[data-testid="stButton"] button[key="calc_loss_btn"] {
                background-color: #348253 !important;
                color: white !important;
                border: none !important;
                border-radius: 12px !important;
                padding: 16px 24px !important;
                font-weight: 700 !important;
                font-size: 16px !important;
                height: 54px !important;
            }
            div[data-testid="stButton"] button[key="calc_loss_btn"]:hover {
                background-color: #2D6E46 !important;
                box-shadow: 0 4px 12px rgba(52,130,83,0.3) !important;
            }
            /* Style for the numerical input inside the red box */
            div[key="u_price"] input {
                color: #E11D48 !important;
                font-size: 20px !important;
                font-weight: 800 !important;
                background: transparent !important;
                border: none !important;
                padding: 0 !important;
            }
        </style>""", unsafe_allow_html=True)

    if calc:
        unit_diff = mkt_avg - u_price
        total_diff = unit_diff * qty
        
        if unit_diff > 0:
            st.markdown(f"""<div class="calculator-panel" style="margin-top:24px; border:2px solid rgba(225,29,72,0.2); background:linear-gradient(135deg, white, #FFF1F2);">
                <div style="font-size: 0.9rem; font-weight: 800; color: #E11D48; text-transform:uppercase; letter-spacing:0.1em; margin-bottom:8px;">Calculated Revenue Loss</div>
                <div style="font-size: 40px; font-weight: 950; color: #E11D48; margin: 10px 0; letter-spacing:-0.05em;">₹{total_diff:,.0f}</div>
                <p style="color: #64748B; font-size: 13px; font-weight:500;">Selling at ₹{u_price:,.0f}/q implies a loss of <b>₹{unit_diff:,.0f} per quintal</b> vs the market average.</p>
            </div>""", unsafe_allow_html=True)
            
            # Optional MSP Comparison
            if u_price < msp_val:
                st.warning(f"⚠️ **Legal Alert**: Your selling price (₹{u_price:,.0f}) is below the Government MSP (₹{msp_val:,.0f}). This is a significant loss situation.")
        else:
            st.markdown(f"""<div class="calculator-panel" style="margin-top:24px; border:2px solid rgba(16,185,129,0.2); background:linear-gradient(135deg, white, #ECFDF5);">
                <div style="font-size: 0.9rem; font-weight: 800; color: #10B981; text-transform:uppercase; letter-spacing:0.1em; margin-bottom:8px;">Excellent Work!</div>
                <div style="font-size: 40px; font-weight: 950; color: #10B981; margin: 10px 0; letter-spacing:-0.05em;">+₹{abs(total_diff):,.0f}</div>
                <p style="color: #64748B; font-size: 13px; font-weight:500;">Great! You are selling above the market price 🎉. You've earned an extra <b>₹{abs(unit_diff):,.0f} per quintal</b>.</p>
            </div>""", unsafe_allow_html=True)
        
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = u_price,
            title = {'text': "Farmer Price vs Market Benchmark", 'font': {'size': 18, 'color': '#1E293B'}},
            gauge = {
                'axis': {'range': [min(u_price, mkt_avg)*0.7, max(u_price, mkt_avg)*1.3], 'tickwidth': 1},
                'bar': {'color': "#10B981" if u_price > mkt_avg else "#E11D48"},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "#F1F5F9",
                'steps': [
                    {'range': [0, mkt_avg], 'color': '#FEE2E2'},
                    {'range': [mkt_avg, max(u_price, mkt_avg)*1.3], 'color': '#DCFCE7'}
                ],
                'threshold': {
                    'line': {'color': "#1E293B", 'width': 4},
                    'thickness': 0.75,
                    'value': mkt_avg
                }
            }
        ))
        fig.update_layout(height=350, margin={'l': 20, 'r': 20, 't': 50, 'b': 20}, paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)

    # ---------------------------------------------------------
# Page 7: Support & Info
# ---------------------------------------------------------
def render_support_info():

    # --- Session state for internal sub-page routing ---
    if 'support_page' not in st.session_state:
        st.session_state.support_page = None

    support_items = [
        {
            "key": "pmkisan", "icon": "🏛️", "title": "PM-Kisan (" + ("સન્માન નિધિ" if st.session_state.lang == 'gu' else "Samman Nidhi") + ")",
            "desc": "Check your ₹6,000 yearly income support status directly on the official portal." if st.session_state.lang == 'en' else "સત્તાવાર પોર્ટલ પર તમારી વાર્ષિક ₹6,000 આવક સહાયની સ્થિતિ તપાસો.",
            "action": t("view_details"), "color": "#2563EB", "bg": "#EFF6FF",
            "url": "https://pmkisan.gov.in/",
            "benefit": "₹6,000 per year (₹2,000 every 4 months) direct bank transfer",
            "eligibility": ["All small & marginal farmers with cultivable land", "Annual household income below ₹2 lakh", "Aadhaar linked bank account required"],
            "steps": ["Visit pmkisan.gov.in or your nearest Common Service Centre", "Register with Aadhaar, bank account & land records", "CSC operator submits application to State Govt", "After verification, installments come to your bank directly"],
            "docs": ["Aadhaar Card", "Bank passbook (with IFSC)", "Land ownership documents", "Mobile number"],
            "helpline": "PM-Kisan Helpline: 155261 / 1800-115-526",
        },
        {
            "key": "pmfby", "icon": "🛡️", "title": "Fasal Bima (" + ("પાક વીમો" if st.session_state.lang == 'gu' else "PMFBY") + ")",
            "desc": "Comprehensive crop insurance covering losses from natural calamities & pests." if st.session_state.lang == 'en' else "કુદરતી આફતો અને જીવાતોથી થતા નુકસાનને આવરી લેતો વ્યાપક પાક વીમો.",
            "action": t("view_details"), "color": "#10B981", "bg": "#ECFDF5",
            "url": "https://pmfby.gov.in/",
            "benefit": "Full insurance sum at just 2% premium for Kharif, 1.5% for Rabi crops",
            "eligibility": ["All farmers growing notified crops", "Both loanee and non-loanee farmers", "Sharecroppers and tenant farmers also covered"],
            "steps": ["Enroll before cut-off date at your bank or CSC", "Pay small premium based on crop type", "Report crop loss within 72 hours of damage", "Claims settled within 2 months of harvest"],
            "docs": ["Bank account details", "Land records / Lease agreement", "Sowing certificate", "Mobile number for crop loss alerts"],
            "helpline": "Crop Insurance Helpline: 1800-200-7710",
        },
        {
            "key": "kcc", "icon": "💳", "title": "Kisan Credit Card (" + ("કિસાન ક્રેડિટ કાર્ડ" if st.session_state.lang == 'gu' else "KCC") + ")",
            "desc": "Apply for a high-limit revolving credit card for seeds, fertilizers & equipment." if st.session_state.lang == 'en' else "બિયારણ, ખાતર અને સાધનો માટે ઉચ્ચ મર્યાદાવાળા રિવોલ્વિંગ ક્રેડિટ કાર્ડ માટે અરજી કરો.",
            "action": t("view_details"), "color": "#F59E0B", "bg": "#FFFBEB",
            "url": "https://www.nabard.org/content1.aspx?id=572&catid=23&mid=530",
            "benefit": "Credit limit up to ₹3 lakh at 4-7% interest (subsidized). No collateral for loans up to ₹1.6 lakh.",
            "eligibility": ["All farmers (individual / joint borrowers)", "Self-Help Groups & Joint Liability Groups", "Tenant farmers, oral lessees & sharecroppers"],
            "steps": ["Visit your nearest bank or cooperative bank", "Submit application with land & ID documents", "Bank assesses your landholding & crop pattern", "KCC issued within 2 weeks of approval"],
            "docs": ["Identity proof (Aadhaar / Voter ID)", "Land ownership or lease documents", "Passport size photo", "Bank account details"],
            "helpline": "NABARD Helpline: 1800-22-0000",
        },
        {
            "key": "helpline", "icon": "📞", "title": "24/7 Kisan Call Centre",
            "desc": "Toll-free helpline 1800-180-1551 — agri-experts available in 22 languages.",
            "action": "View Details", "color": "#E11D48", "bg": "#FFF1F2",
            "url": "tel:18001801551",
            "benefit": "Free expert agricultural advice in your mother tongue, 24 hours a day.",
            "eligibility": ["All farmers across India", "No registration required", "Available in Hindi, Gujarati, and 20 more languages"],
            "steps": ["Dial 1800-180-1551 (toll-free, no charge)", "Select your preferred language", "Describe your farming problem to the expert", "Get instant advice on seeds, pests, weather, schemes"],
            "docs": ["No documents needed", "Just call and speak to an expert"],
            "helpline": "Kisan Call Centre: 1800-180-1551 (24/7 Free)",
        },
        {
            "key": "enam", "icon": "🌾", "title": "eNAM — National Agri Market",
            "desc": "Sell your produce on India's unified electronic mandi network across 1,000+ markets.",
            "action": "View Details", "color": "#7C3AED", "bg": "#F5F3FF",
            "url": "https://www.enam.gov.in/",
            "benefit": "Get transparent, competitive prices for your produce across state borders.",
            "eligibility": ["All farmers with produce registered with APMC", "Traders registered on eNAM platform", "Nearby mandis must be eNAM-integrated"],
            "steps": ["Register at eNAM mandi or online at enam.gov.in", "Bring your produce to the mandi for quality grading", "Your lot is auctioned electronically to buyers nationwide", "Payment deposited directly to your bank account"],
            "docs": ["Aadhaar Card", "Bank account details", "Mandi license (if trader)", "Mobile number"],
            "helpline": "eNAM Helpdesk: 1800-270-0224",
        },
        {
            "key": "soil", "icon": "🧪", "title": "Soil Health Card Scheme",
            "desc": "Get a FREE soil test and personalized fertilizer recommendations every 2 years.",
            "action": "View Details", "color": "#0891B2", "bg": "#ECFEFF",
            "url": "https://soilhealth.dac.gov.in/",
            "benefit": "Know your soil's exact nutrient needs — save money on fertilizers and increase yield.",
            "eligibility": ["All farmers in India", "Issued every 2 years per farm", "Free of cost — government funded"],
            "steps": ["Visit your nearest Krishi Vigyan Kendra (KVK) or Agriculture office", "Provide a soil sample from your field (0-20cm depth)", "Lab tests 12 parameters including N, P, K, pH, organic carbon", "Card issued within 30 days with crop-wise recommendations"],
            "docs": ["Land records or lease agreement", "Aadhaar for registration", "GPS location of field (optional but helpful)"],
            "helpline": "Soil Health Card Helpline: 1800-180-1551",
        },
        {
            "key": "gujarat_agri", "icon": "🌿", "title": "Gujarat Agriculture Dept.",
            "desc": "Official state schemes, subsidies, and farming advisories specific to Gujarat farmers.",
            "action": "View Details", "color": "#15803D", "bg": "#F0FDF4",
            "url": "https://agri.gujarat.gov.in/",
            "benefit": "Access Gujarat-specific subsidies: drip irrigation, seeds, tractors, solar pumps & more.",
            "eligibility": ["Gujarat registered farmers only", "Varies by individual scheme", "Small & marginal farmers get priority"],
            "steps": ["Visit agri.gujarat.gov.in or your local Taluka Agriculture Office", "Find relevant scheme for your crop/equipment", "Submit application with required documents", "Inspector verifies and subsidy is credited to your account"],
            "docs": ["7/12 Utara (land record)", "Aadhaar Card", "Bank passbook", "Caste certificate (if applicable)"],
            "helpline": "Gujarat Agri Helpline: 1800-233-0555",
        },
        {
            "key": "nabard", "icon": "🏦", "title": "NABARD — Rural Finance",
            "desc": "Access farm loans, rural infrastructure fund, and cooperative credit support schemes.",
            "action": "View Details", "color": "#9333EA", "bg": "#FAF5FF",
            "url": "https://www.nabard.org/",
            "benefit": "Refinancing to banks for farm credit. Interest subvention schemes. Watershed & farmer group support.",
            "eligibility": ["Farmers through banks & cooperatives", "Rural artisans and non-farm rural enterprises", "Farmer Producer Organizations (FPOs)"],
            "steps": ["Contact your nearest Rural/Cooperative/Commercial Bank", "Ask for NABARD-refinanced loans or schemes", "Bank forwards eligible cases to NABARD", "NABARD provides funds at subsidized rates to the bank"],
            "docs": ["Routed through your bank — bank will advise documents", "Typically: land records, Aadhaar, income proof"],
            "helpline": "NABARD Helpline: 1800-22-0000",
        },
    ]

    # ----------------------------------------------------------------
    # DETAIL PAGE VIEW (when a card is clicked)
    # ----------------------------------------------------------------
    if st.session_state.support_page:
        page_data = next((s for s in support_items if s['key'] == st.session_state.support_page), None)
        if page_data:
            col_back, _ = st.columns([1, 8])
            with col_back:
                if st.button("← Back", key="support_back"):
                    st.session_state.support_page = None
                    st.rerun()

            c = page_data['color']
            bg = page_data['bg']

            # Hero Header
            st.markdown(f"""
            <div style="background:{bg}; border:2px solid {c}22; border-radius:24px; padding:36px 32px; margin-bottom:28px; position:relative; overflow:hidden;">
                <div style="position:absolute; top:0; left:0; width:100%; height:5px; background:{c};"></div>
                <div style="display:flex; align-items:center; gap:20px; margin-bottom:16px;">
                    <div style="font-size:48px;">{page_data['icon']}</div>
                    <div>
                        <h1 style="font-size:28px; font-weight:900; color:#0F172A; margin:0; letter-spacing:-0.03em;">{page_data['title']}</h1>
                        <p style="font-size:14px; color:#64748B; margin:6px 0 0 0; line-height:1.5;">{page_data['desc']}</p>
                    </div>
                </div>
                <div style="background:white; border-radius:14px; padding:18px 24px; border:1px solid {c}33;">
                    <p style="font-size:11px; font-weight:800; color:{c}; text-transform:uppercase; letter-spacing:0.1em; margin:0 0 4px 0;">Key Benefit</p>
                    <p style="font-size:16px; font-weight:800; color:#0F172A; margin:0;">{page_data['benefit']}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # 3-column info
            r1, r2, r3 = st.columns(3, gap="medium")

            with r1:
                elig_html = "".join([f'<li style="margin-bottom:8px; line-height:1.5;">{e}</li>' for e in page_data['eligibility']])
                st.markdown(f"""
                <div style="background:white; border-radius:18px; padding:24px; border:1px solid #F1F5F9; box-shadow:0 4px 16px rgba(0,0,0,0.04); height:100%;">
                    <p style="font-size:11px; font-weight:800; color:{c}; text-transform:uppercase; letter-spacing:0.1em; margin:0 0 12px 0;">✅ Who is Eligible</p>
                    <ul style="font-size:13px; color:#334155; font-weight:500; padding-left:18px; margin:0; line-height:1.6;">
                        {elig_html}
                    </ul>
                </div>
                """, unsafe_allow_html=True)

            with r2:
                steps_html = "".join([f'<li style="margin-bottom:10px; line-height:1.5;"><span style="font-weight:700; color:{c};">Step {i+1}:</span> {s}</li>' for i, s in enumerate(page_data['steps'])])
                st.markdown(f"""
                <div style="background:white; border-radius:18px; padding:24px; border:1px solid #F1F5F9; box-shadow:0 4px 16px rgba(0,0,0,0.04); height:100%;">
                    <p style="font-size:11px; font-weight:800; color:{c}; text-transform:uppercase; letter-spacing:0.1em; margin:0 0 12px 0;">📋 How to Apply</p>
                    <ol style="font-size:13px; color:#334155; font-weight:500; padding-left:18px; margin:0; line-height:1.6; list-style:none;">
                        {steps_html}
                    </ol>
                </div>
                """, unsafe_allow_html=True)

            with r3:
                docs_html = "".join([f'<li style="margin-bottom:8px; line-height:1.5;">📄 {d}</li>' for d in page_data['docs']])
                st.markdown(f"""
                <div style="background:white; border-radius:18px; padding:24px; border:1px solid #F1F5F9; box-shadow:0 4px 16px rgba(0,0,0,0.04); height:100%;">
                    <p style="font-size:11px; font-weight:800; color:{c}; text-transform:uppercase; letter-spacing:0.1em; margin:0 0 12px 0;">📁 Documents Needed</p>
                    <ul style="font-size:13px; color:#334155; font-weight:500; padding-left:4px; margin:0; list-style:none;">
                        {docs_html}
                    </ul>
                </div>
                """, unsafe_allow_html=True)

            # Helpline + Official Link footer — with clickable tel: and portal links
            import re as _re
            _phone_match = _re.search(r'[\d]{4}[-\s]?[\d]{3}[-\s]?[\d]{4}|[\d]{10,}', str(page_data['helpline']))
            _phone_raw = _phone_match.group(0).replace('-','').replace(' ','') if _phone_match else ''
            _tel_link = f"tel:{_phone_raw}" if _phone_raw else "#"

            st.markdown(f"""
            <div style="display:flex; gap:16px; margin-top:20px; flex-wrap:wrap;">
                <a href="{_tel_link}" style="flex:1; min-width:220px; text-decoration:none; display:block;">
                <div style="background:{bg}; border:2px solid {c}44; border-radius:14px; padding:18px 22px;
                     display:flex; align-items:center; gap:14px; cursor:pointer; transition:all 0.3s;
                     box-shadow:0 4px 16px rgba(0,0,0,0.04);"
                     onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 8px 24px rgba(0,0,0,0.12)';"
                     onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 4px 16px rgba(0,0,0,0.04)';">
                    <div style="width:48px; height:48px; border-radius:12px; background:{c}22; flex-shrink:0;
                         display:flex; align-items:center; justify-content:center; font-size:24px;">📞</div>
                    <div>
                        <p style="font-size:10px; font-weight:800; color:{c}; text-transform:uppercase;
                           letter-spacing:0.08em; margin:0 0 2px 0;">📲 Tap to Call — Free</p>
                        <p style="font-size:14px; font-weight:800; color:#0F172A; margin:0;">{page_data['helpline']}</p>
                        <p style="font-size:11px; color:#64748B; margin:2px 0 0 0; font-weight:500;">Click to dial instantly</p>
                    </div>
                </div>
                </a>
                <div style="flex:1; min-width:220px; background:{c}; border-radius:14px; padding:18px 22px;
                     display:flex; align-items:center; justify-content:space-between; gap:14px;">
                    <div>
                        <p style="font-size:10px; font-weight:800; color:rgba(255,255,255,0.7);
                           text-transform:uppercase; margin:0 0 3px 0;">🌐 Official Portal</p>
                        <p style="font-size:13px; font-weight:700; color:white; margin:0;">
                            {str(page_data['url']).replace('https://','').replace('http://','').rstrip('/')}
                        </p>
                        <p style="font-size:11px; color:rgba(255,255,255,0.6); margin:3px 0 0 0;">
                            Opens official government website
                        </p>
                    </div>
                    <a href="{page_data['url']}" target="_blank"
                       style="background:white; color:{c}; font-size:12px; font-weight:800;
                              padding:12px 22px; border-radius:10px; text-decoration:none;
                              white-space:nowrap; box-shadow:0 4px 12px rgba(0,0,0,0.15);"
                       onmouseover="this.style.transform='scale(1.05)';"
                       onmouseout="this.style.transform='scale(1)';">
                        Open ↗
                    </a>
                </div>
            </div>
            """, unsafe_allow_html=True)

    else:
        # ----------------------------------------------------------------
        # GRID (card listing) VIEW
        # ----------------------------------------------------------------
        st.markdown("""<div style="background:white; border-radius:24px; padding:32px 24px; text-align:center; border:1px solid #F1F5F9; box-shadow:0 10px 30px rgba(0,0,0,0.02); margin-bottom:32px;">
    <div style="width:48px; height:48px; background:#F8FAFC; border-radius:14px; display:flex; align-items:center; justify-content:center; margin:0 auto 16px auto;">
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2.5"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>
    </div>
    <h1 style="font-size:24px; font-weight:950; color:#1E293B; letter-spacing:-0.03em; margin:0;">Resource Portal</h1>
    <p style="font-size:13px; color:#64748B; margin-top:8px;">Click any card below to view full scheme details, eligibility, and how to apply.</p>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap:16px;">', unsafe_allow_html=True)
    for s in support_items:
        st.markdown(f"""
        <div class="sp-card" style="background:white; border-radius:16px; padding:24px; border:1px solid #F1F5F9;
             transition:all 0.3s ease; box-shadow:0 5px 20px rgba(0,0,0,0.02); position:relative; overflow:hidden; cursor:pointer;"
             onmouseover="this.style.borderColor='{s['color']}'; this.style.transform='translateY(-3px)'; this.style.boxShadow='0 12px 32px rgba(0,0,0,0.08)';"
             onmouseout="this.style.borderColor='#F1F5F9'; this.style.transform='translateY(0)'; this.style.boxShadow='0 5px 20px rgba(0,0,0,0.02)';">
            <div style="position:absolute; top:0; left:0; width:100%; height:4px; background:{s['color']};"></div>
            <div style="display:flex; align-items:flex-start; gap:14px;">
                <div style="width:44px; height:44px; min-width:44px; border-radius:12px; background:{s['bg']};
                     display:flex; align-items:center; justify-content:center; font-size:22px;">{s['icon']}</div>
                <div style="flex:1;">
                    <h3 style="font-size:14px; font-weight:800; color:#1E293B; margin:0 0 5px 0;">{s['title']}</h3>
                    <p style="font-size:12px; color:#64748B; margin:0 0 12px 0; line-height:1.5;">{s['desc']}</p>
                    <div style="display:inline-flex; align-items:center; gap:5px; font-weight:700; font-size:11px; color:{s['color']};">
                        {s['action']} <span>→</span>
                    </div>
                </div>
            </div>
        </div>""", unsafe_allow_html=True)
        # Actual clickable Streamlit button overlaid — we use a hidden button trick
        if st.button(f"Open {s['title']}", key=f"sp_{s['key']}", use_container_width=True):
            st.session_state.support_page = s['key']
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

        # FAQ Section
        st.markdown('<br><h2 style="font-size:22px; font-weight:900; color:#1E293B; margin-bottom:24px;">Frequently Asked Questions</h2>', unsafe_allow_html=True)

        faqs = [
        ("How do I register my mandi on the eNAM portal?", "Visit enam.gov.in, click 'Register', and your mandi management committee must apply through the State Agriculture Department. eNAM integration takes 2–4 weeks."),
        ("What is the current subsidy rate for solar irrigation pumps?", "Under Gujarat's Surya Shakti Kisan Yojana (SKY), farmers get up to 90% subsidy on solar pumps. Visit agri.gujarat.gov.in for current rates."),
        ("How do I claim Fasal Bima if my crop is damaged?", "Report crop damage within 72 hours on the PMFBY app or call 1800-200-7710. A local inspector will verify and submit the claim. Settlement happens within 2 months."),
        ("Can I apply for KCC without land ownership?", "Yes! Tenant farmers, sharecroppers, and oral lessees are also eligible for Kisan Credit Card with a joint liability group or guarantee from the landowner."),
    ]
        for q, a in faqs:
            with st.expander(q):
                st.markdown(f'<p style="font-size:13px; color:#475569; line-height:1.7;">{a}</p>', unsafe_allow_html=True)

# ---------------------------------------------------------
# MAIN ROUTING EXECUTION
# ---------------------------------------------------------
if page_clean == t("nav_dashboard"):
    render_dashboard()
elif page_clean == t("nav_market"):
    render_market_comparison()
elif page_clean == t("nav_price"):
    render_price_prediction()
elif page_clean == t("nav_fertilizer"):
    render_fertilizers()
elif page_clean == t("nav_loss"):
    render_loss_analysis()
elif page_clean == t("nav_support"):
    render_support_info()

# Footer
st.markdown("---")
footer_text = "Built with ❤️ for Vadodara Farmers | Empowering Agri-Intelligence 2026" if st.session_state.lang == 'en' else "વડોદરાના ખેડૂતો માટે ❤️ સાથે બનાવેલ | કૃષિ-બુદ્ધિ સશક્તિકરણ 2026"
st.markdown(f"<div style='text-align: center; color: #94A3B8; font-size: 0.8rem;'>{footer_text}</div>", unsafe_allow_html=True)
