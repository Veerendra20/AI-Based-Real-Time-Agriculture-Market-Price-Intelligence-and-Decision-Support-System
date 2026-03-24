import re

with open("app.py", "r", encoding="utf-8") as f:
    content = f.read()

start_marker = '# Page 6: Loss Analysis\\n# ---------------------------------------------------------\\nelif page_clean == "Loss Analysis":'
end_marker = '# ---------------------------------------------------------\\n# Page 7: Support & Info'

replacement = '''# Page 6: Loss Analysis
# ---------------------------------------------------------
elif page_clean == "Loss Analysis":
    la_react_css = """
    <style>
    .tw-bg-red-50 { background-color: #fef2f2; }
    .tw-bg-red-100 { background-color: #fee2e2; }
    .tw-text-red-600 { color: #dc2626; }
    .tw-border-red-200 { border-color: #fecaca; border-style: solid; border-width: 2px; }
    .tw-bg-green-50 { background-color: #f0fdf4; }
    .tw-bg-green-100 { background-color: #dcfce7; }
    .tw-text-green-600 { color: #16a34a; }
    .tw-border-green-200 { border-color: #bbf7d0; border-style: solid; border-width: 2px; }
    .tw-bg-green-50-50 { background-color: rgba(240, 253, 244, 0.5); }
    .tw-border-green-100-50 { border-color: rgba(220, 252, 231, 0.5); border-style: solid; }
    .tw-bg-blue-50-50 { background-color: rgba(239, 246, 255, 0.5); }
    .tw-border-blue-100-50 { border-color: rgba(219, 234, 254, 0.5); border-style: solid; }
    .tw-text-green-700 { color: #15803d; }
    .tw-text-green-900 { color: #14532d; }
    .tw-text-blue-700 { color: #1d4ed8; }
    .tw-text-blue-900 { color: #1e3a8a; }
    .tw-text-red-900 { color: #7f1d1d; }
    .tw-text-red-700 { color: #b91c1c; }
    .tw-text-4xl { font-size: 2.25rem; line-height: 2.5rem; }
    .tw-shrink-0 { flex-shrink: 0; }
    .tw-w-24 { width: 6rem; }
    .tw-h-24 { height: 6rem; }
    .tw-px-8 { padding-left: 2rem; padding-right: 2rem; }
    .tw-py-5 { padding-top: 1.25rem; padding-bottom: 1.25rem; }
    .tw-w-10 { width: 2.5rem; }
    .tw-h-10 { height: 2.5rem; }
    
    .stNumberInput > div > div > input { font-size: 20px !important; font-weight: 800 !important; color: #1E293B !important; }
    div[data-testid="stButton"] button { background-color: #16a34a !important; color: white !important; border: none !important; border-radius: 12px !important; padding: 16px 24px !important; font-weight: 700 !important; font-size: 16px !important; height: 54px !important; width: 100% !important; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06) !important; transition: 0.2s !important; }
    div[data-testid="stButton"] button:hover { background-color: #15803d !important; transform: translateY(-2px) !important; }
    </style>
    """
    
    header_html = """
    <div class="tw-mb-8 tw-flex" style="flex-direction: column;">
      <h1 class="tw-text-3xl tw-font-extrabold tw-text-slate-900 tw-flex tw-items-center tw-gap-3" style="margin:0;">
        <span style="color:#2F7D4A;">🧮</span> Farmer Loss Analysis
      </h1>
      <p class="tw-text-slate-500" style="margin-top:0.25rem;">Calculate potential losses and compare your selling price with market rates</p>
    </div>
    """
    st.markdown(react_css + la_react_css + header_html, unsafe_allow_html=True)
    
    # Selectors Section
    st.markdown("""<div class="tw-bg-white tw-p-6 tw-rounded-2xl tw-border tw-border-slate-100 tw-shadow-sm tw-mb-8 tw-flex tw-gap-6 tw-items-end" style="flex-wrap: wrap;">
        <div class="tw-flex-1" style="min-width:200px;">
          <label class="tw-text-xs tw-font-bold tw-text-slate-400 tw-uppercase tw-tracking-wider" style="display:block; margin-bottom:0.5rem;">🌿 Select Crop</label>""", unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    crop_list = sorted(df['Crop Name'].unique())
    with c1:
        sel_comm = st.selectbox("Select Crop", crop_list, key="sel_crop", label_visibility="collapsed")
    with c2:
        current_mkt = st.selectbox("Market Benchmark", sorted(df['Market Name'].unique()), key="sel_market", label_visibility="collapsed")
        
    st.markdown('</div></div>', unsafe_allow_html=True)

    # Fetch stats
    stats = get_current_stats(df, sel_comm, current_mkt)
    mkt_avg = stats['price']
    msp_val = stats['msp']

    # Input Section
    st.markdown('<div class="tw-grid tw-grid-cols-2 tw-gap-8 tw-mb-10 pl-grid-mob" style="grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));">', unsafe_allow_html=True)
    
    i1, i2 = st.columns(2, gap="large")
    with i1:
        st.markdown("""<div class="tw-bg-white tw-p-8 tw-rounded-3xl tw-border tw-border-slate-100 tw-shadow-sm" style="height: 100%;">
           <div class="tw-flex tw-items-center tw-gap-3 tw-mb-8">
              <div class="tw-w-10 tw-h-10 tw-bg-green-50 tw-text-green-700 tw-rounded-full tw-flex tw-items-center tw-justify-center tw-font-bold" style="font-size:18px;">₹</div>
              <h3 class="tw-font-extrabold tw-text-slate-800 tw-text-xl tw-tracking-tight" style="margin:0;">Your Selling Price</h3>
           </div>
           
           <div style="margin-bottom:24px;">
              <label class="tw-text-xxs tw-font-black tw-text-slate-400 tw-uppercase tw-tracking-widest" style="display:block; margin-bottom:0.75rem;">PRICE PER QUINTAL (₹)</label>
        """, unsafe_allow_html=True)
        u_price = st.number_input("Your Selling Price", min_value=1.0, value=float(round(mkt_avg*0.85)) if mkt_avg > 0 else 1000.0, step=10.0, label_visibility="collapsed", key="u_price")
        st.markdown('</div><div><label class="tw-text-xxs tw-font-black tw-text-slate-400 tw-uppercase tw-tracking-widest" style="display:block; margin-bottom:0.75rem;">TOTAL QUANTITY (QUINTALS)</label>', unsafe_allow_html=True)
        qty = st.number_input("Enter quantity", min_value=1.0, value=10.0, step=1.0, label_visibility="collapsed", key="la_qty")
        st.markdown('</div><div style="margin-top:24px;">', unsafe_allow_html=True)
        calc = st.button("Calculate Impact", key="calc_loss_btn", use_container_width=True)
        st.markdown('</div></div>', unsafe_allow_html=True)

    with i2:
        st.markdown(f"""<div class="tw-bg-white tw-p-8 tw-rounded-3xl tw-border tw-border-slate-100 tw-shadow-sm tw-flex" style="flex-direction:column; justify-content:space-between; height: 100%;">
           <div>
              <div class="tw-flex tw-items-center tw-gap-3 tw-mb-8">
                 <div class="tw-w-10 tw-h-10 tw-bg-blue-50 tw-text-blue-600 tw-rounded-full tw-flex tw-items-center tw-justify-center tw-font-bold tw-italic" style="font-size:18px;">M</div>
                 <h3 class="tw-font-extrabold tw-text-slate-800 tw-text-xl tw-tracking-tight" style="margin:0;">Market Benchmarks</h3>
              </div>
              <div style="display:flex; flex-direction:column; gap:1.5rem;">
                 <div class="tw-p-5 tw-bg-green-50-50 tw-rounded-2xl tw-border tw-border-green-100-50">
                    <p class="tw-text-xxs tw-font-black tw-text-green-700 tw-uppercase tw-tracking-widest tw-mb-1 tw-opacity-70" style="margin:0;">Today's Market Price</p>
                    <p class="tw-text-3xl tw-font-black tw-text-green-900" style="margin:0;">₹{mkt_avg:,.0f}<span class="tw-text-sm tw-font-bold tw-opacity-40" style="margin-left:0.25rem;">/q</span></p>
                 </div>
                 <div class="tw-p-5 tw-bg-blue-50-50 tw-rounded-2xl tw-border tw-border-blue-100-50">
                    <p class="tw-text-xxs tw-font-black tw-text-blue-700 tw-uppercase tw-tracking-widest tw-mb-1 tw-opacity-70" style="margin:0;">Government MSP</p>
                    <p class="tw-text-3xl tw-font-black tw-text-blue-900" style="margin:0;">₹{msp_val:,.0f}<span class="tw-text-sm tw-font-bold tw-opacity-40" style="margin-left:0.25rem;">/q</span></p>
                 </div>
              </div>
           </div>
        </div>""", unsafe_allow_html=True)
        
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Results Section
    if calc:
        lossPerQ = mkt_avg - u_price
        totalLoss = lossPerQ * qty
        isLoss = lossPerQ > 0
        
        box_bg = "tw-bg-red-50 tw-border-red-200" if isLoss else "tw-bg-green-50 tw-border-green-200"
        icon_bg = "tw-bg-red-100 tw-text-red-600" if isLoss else "tw-bg-green-100 tw-text-green-600"
        title_col = "tw-text-red-900" if isLoss else "tw-text-green-900"
        sub_col = "tw-text-red-700" if isLoss else "tw-text-green-700"
        val_col = "tw-text-red-600" if isLoss else "tw-text-green-600"
        
        icon = '⚠️' if isLoss else '✅'
        title_msg = f"You are losing ₹{abs(lossPerQ):,.0f} per quintal" if isLoss else f"You are earning ₹{abs(lossPerQ):,.0f} extra! ✨"
        sub_msg = "Strong Advice: Wait for prices to reach MSP or sell at government mandis." if isLoss else "Great Job: Your selling price is excellent compared to the market average."
        sign = "-" if isLoss else "+"
        
        st.markdown(f"""
        <div class="{box_bg} tw-rounded-3xl tw-p-10 tw-shadow-xl tw-mb-10" style="transition:0.5s;">
           <div class="tw-flex tw-items-center tw-gap-10 pl-grid-mob" style="flex-wrap:wrap;">
              <div class="tw-w-24 tw-h-24 tw-rounded-full tw-flex tw-items-center tw-justify-center tw-shadow-md tw-shrink-0 {icon_bg}" style="font-size:40px;">
                 {icon}
              </div>
              <div class="tw-flex-1">
                 <h2 class="tw-text-4xl tw-font-black tw-mb-2 {title_col}" style="margin-top:0;">{title_msg}</h2>
                 <p class="tw-text-xl tw-font-bold {sub_col}" style="margin:0;">{sub_msg}</p>
                 <div style="margin-top:2rem;">
                    <div class="tw-bg-white-60 tw-backdrop-blur tw-px-8 tw-py-5 tw-rounded-2xl tw-shadow-sm tw-border tw-border-white-50" style="display:inline-block;">
                        <p class="tw-text-xxs tw-font-black tw-text-slate-400 tw-uppercase tw-tracking-widest tw-mb-1" style="margin:0 0 0.25rem 0;">Total Impact</p>
                        <p class="tw-text-3xl tw-font-black {val_col}" style="margin:0;">{sign} ₹{abs(totalLoss):,.0f}</p>
                    </div>
                 </div>
              </div>
           </div>
        </div>
        """, unsafe_allow_html=True)
    
'''

pattern = re.compile(re.escape(start_marker) + r".*?" + re.escape(end_marker), re.DOTALL)
new_content = pattern.sub(replacement + '\\n\\n' + end_marker, content)

with open("app.py", "w", encoding="utf-8") as f:
    f.write(new_content)
