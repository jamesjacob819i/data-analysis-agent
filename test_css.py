import re

with open('app.py', 'r') as f:
    orig = f.read()

# Try to insert CSS injection seamlessly after page_config
replacement = """def main():
    st.set_page_config(
        page_title="🤖 Autonomous Data Analysis System",
        page_icon="🤖",
        layout="wide"
    )
    
    # --- Modernizing UI ---
    st.markdown('''
    <style>
    /* Sleek gradient background for app */
    .stApp {
        background: radial-gradient(circle at center, #1b263b 0%, #0d1321 100%);
    }

    /* Style the sidebar cleanly */
    div[data-testid="stSidebar"] {
        background: rgba(22, 27, 34, 0.5);
        border-right: 1px solid rgba(255,255,255,0.05);
    }

    /* Primary buttons with sleek gradients */
    button[kind="primary"] {
        background: linear-gradient(90deg, #3b82f6 0%, #8b5cf6 100%);
        border: none;
        color: white;
        font-weight: 600;
        border-radius: 6px;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    button[kind="primary"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(139, 92, 246, 0.4);
    }
    
    /* Elegant metric displays */
    div[data-testid="stMetricValue"] {
        font-size: 2.2rem;
        font-weight: 800;
        background: -webkit-linear-gradient(45deg, #60a5fa, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Clean inputs */
    .stTextInput input, .stSelectbox > div > div {
        border-radius: 6px;
        background: rgba(255,255,255,0.02);
        border: 1px solid rgba(255,255,255,0.1);
        color: white;
    }
    
    /* Sleek expanders */
    .streamlit-expanderHeader {
        background-color: transparent !important;
        font-weight: 600;
        border-bottom: 1px solid rgba(255,255,255,0.05);
    }
    </style>
    ''', unsafe_allow_html=True)
"""

if 'def main():\n    st.set_page_config' in orig:
    content = orig.replace('def main():\n    st.set_page_config(\n        page_title="🤖 Autonomous Data Analysis System",\n        page_icon="🤖",\n        layout="wide"\n    )', replacement)
    with open('app.py', 'w') as f:
        f.write(content)
    print("Success: CSS applied.")
else:
    print("Error: Could not find main() to inject.")
