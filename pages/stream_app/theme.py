import streamlit as st

def setup_theme():
    st.markdown("""
        <style>
        :root {
            --primary-color: #ffffff;         /* White background */
            --secondary-color: #f8f9fa;       /* Very light gray for hover */
            --accent-color: #0066cc;          /* Blue accent for interactive elements */
            --text-color: #000000;            /* Black text */
            --border-color: #000000;          /* Black borders */
        }
        
        /* Force white background and black text everywhere */
        .stMarkdown, 
        .stText,
        .stExpander,
        [data-testid="stExpander"],
        [data-testid="stExpander"] .streamlit-expanderContent,
        [data-testid="stExpander"] .stMarkdown p,
        .source-panel-content,
        .element-container,
        .stMarkdown > div,
        div[data-testid="stExpander"] > details,
        div[data-testid="stExpander"] > details > summary,
        div[data-testid="stExpander"] > details[open] > summary,
        div[data-testid="stExpander"] > details > summary:hover {
            color: var(--text-color) !important;
            background-color: var(--primary-color) !important;
        }
        
        /* Expander styling */
        .streamlit-expanderHeader,
        .streamlit-expanderHeader:hover {
            background-color: var(--primary-color) !important;
            color: var(--text-color) !important;
            border: 1px solid var(--border-color) !important;
        }
        
        /* Button styling */
        .stButton > button {
            color: var(--text-color) !important;
            background-color: var(--primary-color) !important;
            border: 1px solid var(--border-color) !important;
            border-radius: 4px !important;
            padding: 6px 12px !important;
            font-size: 0.95em !important;
            transition: all 0.2s ease !important;
        }
        
        /* Button hover state */
        .stButton > button:hover {
            background-color: var(--secondary-color) !important;
            border-color: var(--accent-color) !important;
            transform: translateY(-1px) !important;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
        }
        
        /* Sidebar styling */
        [data-testid="stSidebar"],
        [data-testid="stSidebar"] .stMarkdown {
            background-color: var(--primary-color) !important;
            color: var(--text-color) !important;
        }
        
        /* Input fields with black borders */
        .stTextInput > div > div > input,
        .stSelectbox > div > div > div,
        .stTextArea > div > div > textarea {
            color: var(--text-color) !important;
            background-color: var(--primary-color) !important;
            border: 1px solid var(--border-color) !important;
            border-radius: 4px !important;
        }

        /* Style for focused input fields */
        .stTextInput > div > div > input:focus,
        .stSelectbox > div > div > div:focus,
        .stTextArea > div > div > textarea:focus {
            border: 2px solid var(--border-color) !important;
            box-shadow: none !important;
        }

        /* Style for select box arrow */
        .stSelectbox > div > div > div > div {
            color: var(--text-color) !important;
        }
        </style>
    """, unsafe_allow_html=True)
