import py_compile

with open("app.py", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace('\r\n', '\n')

# The broken section: else: with no indented block
# Lines 1496-1548 need the non-detail view code to be inside the else block
# Find the else: line and indent everything from the grid down to the FAQ end

old_grid = '''    else:
    # ----------------------------------------------------------------
    # GRID (card listing) VIEW
    # ----------------------------------------------------------------
    st.markdown("""<div style="background:white; border-radius:24px; padding:32px 24px; text-align:center; border:1px solid #F1F5F9; box-shadow:0 10px 30px rgba(0,0,0,0.02); margin-bottom:32px;">
<div style="width:48px; height:48px; background:#F8FAFC; border-radius:14px; display:flex; align-items:center; justify-content:center; margin:0 auto 16px auto;">
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2.5"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>
</div>
<h1 style="font-size:24px; font-weight:950; color:#1E293B; letter-spacing:-0.03em; margin:0;">Resource Portal</h1>
<p style="font-size:13px; color:#64748B; margin-top:8px;">Click any card below to view full scheme details, eligibility, and how to apply.</p>
</div>""", unsafe_allow_html=True)'''

new_grid = '''    else:
        # ----------------------------------------------------------------
        # GRID (card listing) VIEW
        # ----------------------------------------------------------------
        st.markdown("""<div style="background:white; border-radius:24px; padding:32px 24px; text-align:center; border:1px solid #F1F5F9; box-shadow:0 10px 30px rgba(0,0,0,0.02); margin-bottom:32px;">
<div style="width:48px; height:48px; background:#F8FAFC; border-radius:14px; display:flex; align-items:center; justify-content:center; margin:0 auto 16px auto;">
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2.5"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>
</div>
<h1 style="font-size:24px; font-weight:950; color:#1E293B; letter-spacing:-0.03em; margin:0;">Resource Portal</h1>
<p style="font-size:13px; color:#64748B; margin-top:8px;">Click any card below to view full scheme details, eligibility, and how to apply.</p>
</div>""", unsafe_allow_html=True)'''

if old_grid in content:
    content = content.replace(old_grid, new_grid, 1)
    print("Replaced grid header.")
else:
    print("ERROR: Could not find grid header.")

# Now fix the rest of the else block - the st.markdown for grid and the for loop
old_rest = """        st.markdown('<div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap:16px;">', unsafe_allow_html=True)
    for s in support_items:"""

new_rest = """        st.markdown('<div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap:16px;">', unsafe_allow_html=True)
        for s in support_items:"""

if old_rest in content:
    content = content.replace(old_rest, new_rest, 1)
    print("Fixed for loop indent.")
else:
    print("ERROR: Could not find for loop block.")

# Fix st.markdown for FAQ section
old_faq_header = """    st.markdown('</div>', unsafe_allow_html=True)

    # FAQ Section
    st.markdown('<br><h2 style="font-size:22px; font-weight:900; color:#1E293B; margin-bottom:24px;">Frequently Asked Questions</h2>', unsafe_allow_html=True)

    faqs = ["""

new_faq_header = """        st.markdown('</div>', unsafe_allow_html=True)

        # FAQ Section
        st.markdown('<br><h2 style="font-size:22px; font-weight:900; color:#1E293B; margin-bottom:24px;">Frequently Asked Questions</h2>', unsafe_allow_html=True)

        faqs = ["""

if old_faq_header in content:
    content = content.replace(old_faq_header, new_faq_header, 1)
    print("Fixed FAQ section indent.")
else:
    print("ERROR: Could not find FAQ header.")

old_faq_loop = """    for q, a in faqs:
        with st.expander(q):
            st.markdown(f'<p style="font-size:13px; color:#475569; line-height:1.7;">{a}</p>', unsafe_allow_html=True)"""

new_faq_loop = """        for q, a in faqs:
            with st.expander(q):
                st.markdown(f'<p style="font-size:13px; color:#475569; line-height:1.7;">{a}</p>', unsafe_allow_html=True)"""

if old_faq_loop in content:
    content = content.replace(old_faq_loop, new_faq_loop, 1)
    print("Fixed FAQ loop indent.")
else:
    print("ERROR: Could not find FAQ loop.")

with open("app.py", "w", encoding="utf-8") as f:
    f.write(content)

try:
    py_compile.compile("app.py", doraise=True)
    print("SUCCESS: app.py compiles cleanly!")
except py_compile.PyCompileError as e:
    print(f"COMPILE ERROR: {e}")
