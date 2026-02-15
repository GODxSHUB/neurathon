
# import streamlit as st

# def apply_custom_css():
#     st.markdown("""
#     <style>
#         @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
        
#         /* 1. LAYOUT RESET (No Scroll, Full Height) */
#         html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
#             overflow: hidden !important;
#             height: 100vh !important;
#             font-family: 'Inter', sans-serif;
#         }
        
#         .block-container {
#             padding-top: 1.5rem !important;
#             padding-left: 2rem !important;
#             padding-right: 2rem !important;
#             max-width: 100% !important;
#         }
        
#         /* 2. BACKGROUND */
#         .stApp {
#             background: linear-gradient(180deg, #FFF0F5 0%, #F3E8FF 50%, #E0F2FE 100%);
#         }
        
#         /* 3. TEXT COLORS (Dark) */
#         h1, h2, h3, h4, h5, p, span, div, label {
#             color: #1F2937 !important;
#         }
        
#         /* 4. GLASS CARDS FOR COLUMNS 1 & 3 */
#         [data-testid="column"]:nth-of-type(1) > div > div[data-testid="stVerticalBlock"],
#         [data-testid="column"]:nth-of-type(3) > div > div[data-testid="stVerticalBlock"] {
#             background: rgba(255, 255, 255, 0.45);
#             backdrop-filter: blur(10px);
#             border-radius: 20px;
#             padding: 25px;
#             border: 1px solid rgba(255, 255, 255, 0.5);
#             box-shadow: 0 4px 15px rgba(0,0,0,0.05);
#             gap: 1rem;
#         }

#         /* 5. INPUT FIELDS */
#         .stTextArea textarea {
#             background-color: rgba(255, 255, 255, 0.6) !important;
#             border: 1px solid #9CA3AF !important;
#             color: #000000 !important;
#             border-radius: 12px;
#         }
        
#         /* 6. BUTTONS */
#         .stButton > button {
#             border-radius: 12px;
#             font-weight: 600;
#             border: none;
#             padding: 0.8rem;
#             transition: all 0.2s;
#             background: rgba(255, 255, 255, 0.6);
#         }
#         .stButton > button:hover {
#             background: white;
#             transform: translateY(-2px);
#             box-shadow: 0 4px 10px rgba(0,0,0,0.1);
#         }
        
#         /* Primary Action Buttons */
#         div[data-testid="stHorizontalBlock"] .stButton > button, 
#         button[kind="primary"] {
#              background: linear-gradient(135deg, #8B5CF6 0%, #7C3AED 100%) !important;
#              color: white !important;
#         }

#         /* 7. PROGRESS BAR */
#         .stProgress > div > div > div > div {
#             background-color: #8B5CF6;
#         }

#         /* Hide default elements */
#         #MainMenu, footer, header {visibility: hidden;}
        
#         /* Custom Text Classes */
#         .big-stat { font-size: 2.5rem; font-weight: 800; line-height: 1; margin: 0;}
#         .label-stat { font-size: 0.75rem; font-weight: 700; text-transform: uppercase; color: #6B7280 !important; margin-bottom: 5px; }

#     </style>
#     """, unsafe_allow_html=True)



















# import streamlit as st

# def apply_custom_css():
#     st.markdown("""
#     <style>
#         /* IMPORT GOOGLE FONT */
#         @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
        
#         /* GENERAL SETTINGS */
#         .stApp {
#             /* NEW: Vibrant Pink to Blue Gradient */
#             background: linear-gradient(135deg, #fbc2eb 0%, #a6c1ee 100%);
#             background-attachment: fixed; /* Keeps gradient fixed while scrolling */
#             font-family: 'Inter', sans-serif;
#         }
        
#         h1, h2, h3 {
#             color: #1F2937;
#             font-weight: 800;
#         }
        
#         /* GLASSMORPHISM CARDS */
#         .glass-card {
#             background: rgba(255, 255, 255, 0.60); /* Slightly more transparent to show gradient */
#             backdrop-filter: blur(16px);
#             -webkit-backdrop-filter: blur(16px);
#             border: 1px solid rgba(255, 255, 255, 0.6);
#             border-radius: 24px;
#             padding: 25px;
#             box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.1);
#             margin-bottom: 20px;
#             transition: transform 0.2s ease;
#         }
        
#         .glass-card:hover {
#             transform: translateY(-2px);
#             box-shadow: 0 12px 40px 0 rgba(31, 38, 135, 0.15);
#         }

#         /* HERO STATS (Top Row) */
#         .stat-box {
#             text-align: center;
#             padding: 15px;
#             border-radius: 16px;
#             background: rgba(255,255,255,0.4);
#             border: 1px solid rgba(255,255,255,0.6);
#             backdrop-filter: blur(4px);
#         }
#         .stat-val { font-size: 2rem; font-weight: 800; color: #4F46E5; margin: 0; }
#         .stat-label { font-size: 0.8rem; color: #4B5563; letter-spacing: 1px; text-transform: uppercase; font-weight: 600;}

#         /* INPUT AREA */
#         .stTextArea textarea {
#             background-color: rgba(255, 255, 255, 0.6) !important;
#             border: 2px solid rgba(255,255,255,0.8) !important;
#             border-radius: 16px !important;
#             color: #111827 !important;
#             font-size: 1rem;
#         }
#         .stTextArea textarea:focus {
#             border-color: #4F46E5 !important;
#             box-shadow: 0 0 0 2px rgba(79, 70, 229, 0.2) !important;
#         }

#         /* BUTTONS */
#         .stButton button {
#             border-radius: 12px !important;
#             font-weight: 600 !important;
#             border: none !important;
#             transition: all 0.3s ease !important;
#             padding: 0.5rem 1rem !important;
#         }
        
#         /* Primary Button (Generate, Complete) */
#         div[data-testid="stButton"] button[kind="primary"] {
#             background: linear-gradient(90deg, #4F46E5 0%, #7C3AED 100%);
#             box-shadow: 0 4px 14px 0 rgba(124, 58, 237, 0.3);
#             color: white;
#         }
#         div[data-testid="stButton"] button[kind="primary"]:hover {
#             transform: scale(1.02);
#             box-shadow: 0 6px 20px 0 rgba(124, 58, 237, 0.5);
#         }

#         /* Secondary Button (Record, Back) */
#         div[data-testid="stButton"] button[kind="secondary"] {
#             background: rgba(255,255,255,0.8);
#             color: #4B5563;
#             border: 1px solid #E5E7EB !important;
#         }
#         div[data-testid="stButton"] button[kind="secondary"]:hover {
#             background: #ffffff;
#         }

#         /* PROGRESS BAR */
#         .stProgress > div > div > div > div {
#             background: linear-gradient(90deg, #10B981 0%, #34D399 100%);
#             border-radius: 10px;
#         }

#         /* ACTIVE STEP CARD HIGHLIGHT */
#         .active-step-box {
#             background: rgba(255, 255, 255, 0.9);
#             border-left: 8px solid #4F46E5;
#             padding: 30px;
#             border-radius: 20px;
#             box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1);
#         }

#         /* HIDE DEFAULT STREAMLIT ELEMENTS */
#         #MainMenu {visibility: hidden;}
#         footer {visibility: hidden;}
#         header {visibility: hidden;}
        
#     </style>
#     """, unsafe_allow_html=True)























import streamlit as st

def apply_custom_css():
    st.markdown("""
    <style>
        /* IMPORT GOOGLE FONT */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
        
        /* GENERAL SETTINGS */
        .stApp {
            /* Pink to Blue Gradient */
            background: linear-gradient(135deg, #fbc2eb 0%, #a6c1ee 100%);
            background-attachment: fixed;
            font-family: 'Inter', sans-serif;
            color: #000000 !important;
        }
        
        /* REMOVE EXTRA TOP SPACE */
        .block-container {
            padding-top: 1rem !important;
            padding-bottom: 5rem !important;
        }
        
        /* HEADERS & TEXT */
        h1, h2, h3, h4, h5, h6, p, div, span, label {
            color: #000000 !important;
        }
        
        h1, h2, h3 {
            font-weight: 800;
        }
        
        /* GLASSMORPHISM CARDS */
        .glass-card {
            background: rgba(255, 255, 255, 0.60);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.6);
            border-radius: 24px;
            padding: 25px;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.1);
            margin-bottom: 20px;
        }

        /* STAT BOXES */
        .stat-box {
            text-align: center;
            padding: 15px;
            border-radius: 16px;
            background: rgba(255,255,255,0.5);
            border: 1px solid rgba(255,255,255,0.6);
            backdrop-filter: blur(4px);
        }
        .stat-val { font-size: 2rem; font-weight: 800; color: #000000 !important; margin: 0; }
        .stat-label { font-size: 0.8rem; color: #000000 !important; letter-spacing: 1px; text-transform: uppercase; font-weight: 700;}

        /* INPUT AREA */
        .stTextArea textarea {
            background-color: rgba(255, 255, 255, 0.7) !important;
            border: 2px solid rgba(0,0,0,0.1) !important;
            border-radius: 16px !important;
            color: #000000 !important;
            font-size: 1rem;
            font-weight: 500;
        }
        .stTextArea textarea:focus {
            border-color: #000000 !important;
            box-shadow: 0 0 0 2px rgba(0, 0, 0, 0.2) !important;
        }

        /* --- BUTTON STYLES FIXED FOR VISIBILITY --- */
        .stButton button {
            border-radius: 12px !important;
            font-weight: 700 !important;
            border: none !important;
            transition: all 0.3s ease !important;
            padding: 0.6rem 1.2rem !important;
        }
        
        /* Primary Button (Generate - Page 2) */
        /* Made it Indigo/Purple to pop against background */
        div[data-testid="stButton"] button[kind="primary"] {
            background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%) !important;
            color: #ffffff !important;
            box-shadow: 0 4px 14px 0 rgba(79, 70, 229, 0.4);
            border: 1px solid rgba(255,255,255,0.2) !important;
        }
        div[data-testid="stButton"] button[kind="primary"]:hover {
            transform: scale(1.02);
            box-shadow: 0 6px 20px 0 rgba(79, 70, 229, 0.6);
            color: #ffffff !important;
        }

        /* Secondary Button (Moods - Page 1) */
        /* Made it White with Black Text so it is clearly visible */
        div[data-testid="stButton"] button[kind="secondary"] {
            background: #ffffff !important;
            color: #000000 !important;
            border: 1px solid #e5e7eb !important;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        }
        div[data-testid="stButton"] button[kind="secondary"]:hover {
            background: #f9fafb !important;
            border-color: #000000 !important;
            transform: translateY(-2px);
        }
        
        /* ------------------------------------------ */

        /* PROGRESS BAR */
        .stProgress > div > div > div > div {
            background: #000000;
            border-radius: 10px;
        }

        /* ACTIVE STEP HIGHLIGHT */
        .active-step-box {
            background: rgba(255, 255, 255, 0.9);
            border-left: 8px solid #000000;
            padding: 30px;
            border-radius: 20px;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1);
        }

        /* JSON EXPANDER TEXT */
        .streamlit-expanderHeader {
            color: #000000 !important;
            font-weight: 600;
        }

        /* HIDE DEFAULT ELEMENTS */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
    </style>
    """, unsafe_allow_html=True)
