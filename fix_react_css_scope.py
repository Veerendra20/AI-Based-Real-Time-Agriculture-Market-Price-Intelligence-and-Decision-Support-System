with open("app.py", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace('\r\n', '\n')

# 1) Remove the mis-placed react_css block (between Dashboard if and Market Compare elif)
# It starts right after the Dashboard if block ends at line 612 and goes to line 681
# In the normalized content, find it precisely:
mis_placed_block = '''# ---------------------------------------------------------
# Shared Tailwind CSS (accessible across all page sections)
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
    .tw-p-6 { padding: 1.5rem; }
    .tw-p-8 { padding: 2rem; }
    .tw-px-6 { padding-left: 1.5rem; padding-right: 1.5rem; }
    .tw-px-4 { padding-left: 1rem; padding-right: 1rem; }
    .tw-py-4 { padding-top: 1rem; padding-bottom: 1rem; }
    .tw-px-2 { padding-left: 0.5rem; padding-right: 0.5rem; }
    .tw-py-05 { padding-top: 0.125rem; padding-bottom: 0.125rem; }
    .tw-border { border-width: 1px; }
    .tw-border-b { border-bottom-width: 1px; }
    .tw-border-l-4 { border-left-width: 4px; }
    .tw-font-black { font-weight: 900; }
    .tw-font-extrabold { font-weight: 800; }
    .tw-font-bold { font-weight: 700; }
    .tw-text-3xl { font-size: 1.875rem; line-height: 2.25rem; }
    .tw-text-2xl { font-size: 1.5rem; line-height: 2rem; }
    .tw-text-xl { font-size: 1.25rem; line-height: 1.75rem; }
    .tw-text-lg { font-size: 1.125rem; line-height: 1.75rem; }
    .tw-text-sm { font-size: 0.875rem; line-height: 1.25rem; }
    .tw-text-xs { font-size: 0.75rem; line-height: 1rem; }
    .tw-text-xxs { font-size: 10px; line-height: 1rem; }
    .tw-uppercase { text-transform: uppercase; }
    .tw-tracking-wider { letter-spacing: 0.05em; }
    .tw-tracking-widest { letter-spacing: 0.1em; }
    .tw-tracking-tighter { letter-spacing: -0.05em; }
    .tw-tracking-tight { letter-spacing: -0.025em; }
    .tw-table { width: 100%; border-collapse: collapse; }
    .tw-th { text-align: left; }
    .tw-tr-hover:hover { background-color: #f8fafc; }
    .tw-bg-green-50-30 { background-color: rgba(240, 253, 244, 0.5); }
    </style>
"""

'''

if mis_placed_block in content:
    content = content.replace(mis_placed_block, '', 1)
    print("Removed mis-placed react_css block.")
else:
    print("ERROR: Could not find mis-placed react_css block to remove.")

# 2) Insert react_css correctly - RIGHT BEFORE the if/elif chain starts
# That is, right before "# ---------------------------------------------------------\n# Page 1: Dashboard"
correct_anchor = '# ---------------------------------------------------------\n# Page 1: Dashboard\n# ---------------------------------------------------------\nif page_clean == "Dashboard":'

correct_global = '''# ---------------------------------------------------------
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

'''

if correct_anchor in content:
    content = content.replace(correct_anchor, correct_global + correct_anchor, 1)
    print("Injected global react_css correctly before if/elif chain.")
else:
    print("ERROR: Could not find anchor to inject react_css before page routing.")

with open("app.py", "w", encoding="utf-8") as f:
    f.write(content)

import py_compile
try:
    py_compile.compile("app.py", doraise=True)
    print("SUCCESS: app.py compiles cleanly!")
except py_compile.PyCompileError as e:
    print(f"COMPILE ERROR: {e}")
