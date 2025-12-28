import streamlit as st
import pandas as pd
import re
from collections import Counter
import unicodedata
import string

# ---------------- 1. PAGE CONFIGURATION ----------------
st.set_page_config(
    page_title="e-Bhruhat Trayi Exploration by PraKul",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- 2. SESSION STATE INITIALIZATION ----------------
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False
if "font_size" not in st.session_state:
    st.session_state.font_size = "Medium"
if "main_query" not in st.session_state:
    st.session_state.main_query = ""
if "strict_mode" not in st.session_state:
    st.session_state.strict_mode = False
if "filter_mode" not in st.session_state:
    st.session_state.filter_mode = "all"
if "read_pos" not in st.session_state:
    st.session_state.read_pos = 1
if "search_page" not in st.session_state:
    st.session_state.search_page = 0

# ---------------- 3. THEME AND FONT CONFIGURATION ----------------
font_sizes = {
    "Small": {"sloka": "1.1em", "iast": "0.85em", "ref": "0.7em", "body": "0.9em"},
    "Medium": {"sloka": "1.4em", "iast": "1em", "ref": "0.8em", "body": "1em"},
    "Large": {"sloka": "1.7em", "iast": "1.15em", "ref": "0.9em", "body": "1.1em"},
    "Extra Large": {"sloka": "2em", "iast": "1.3em", "ref": "1em", "body": "1.2em"}
}

current_font = font_sizes[st.session_state.font_size]

# Dynamic theme colors
if st.session_state.dark_mode:
    theme = {
        "bg_primary": "#0d1117",
        "bg_secondary": "#161b22",
        "bg_card": "#21262d",
        "text_primary": "#f0f6fc",
        "text_secondary": "#c9d1d9",
        "accent": "#ff7b72",
        "accent_secondary": "#79c0ff",
        "border": "#30363d",
        "highlight_exact": "#ffa657",
        "highlight_compound": "#d29922",
        "success": "#3fb950",
        "sloka_bg": "#161b22",
        "card_border": "#ff7b72",
        "highlight_exact_bg": "#5a3e00",
        "highlight_compound_bg": "#3d3000",
        "table_header": "#238636",
        "metric_text": "#f0f6fc"
    }
else:
    theme = {
        "bg_primary": "#ffffff",
        "bg_secondary": "#f8f9fa",
        "bg_card": "#ffffff",
        "text_primary": "#2c3e50",
        "text_secondary": "#555555",
        "accent": "#d35400",
        "accent_secondary": "#2980b9",
        "border": "#e0e0e0",
        "highlight_exact": "#e65100",
        "highlight_compound": "#f57f17",
        "success": "#27ae60",
        "sloka_bg": "#fffef5",
        "card_border": "#d35400",
        "highlight_exact_bg": "#ffcc80",
        "highlight_compound_bg": "#fff9c4",
        "table_header": "#d35400",
        "metric_text": "#2c3e50"
    }

# ---------------- 4. DYNAMIC CSS ----------------
st.markdown(f"""
<style>
    /* Base Theme */
    .main {{
        background-color: {theme['bg_primary']};
        color: {theme['text_primary']};
    }}
    
    .stApp {{
        background-color: {theme['bg_primary']};
    }}
    
    /* Mobile Responsive */
    @media (max-width: 768px) {{
        .main {{ padding: 5px !important; }}
        .sloka-text {{ font-size: calc({current_font['sloka']} * 0.85) !important; }}
        .stButton>button {{ padding: 6px 8px !important; font-size: 0.85em !important; }}
        .stTabs [data-baseweb="tab"] {{ font-size: 0.75em !important; padding: 6px 10px !important; }}
    }}
    
    @media (max-width: 480px) {{
        .sloka-text {{ font-size: calc({current_font['sloka']} * 0.75) !important; }}
        h1 {{ font-size: 1.2em !important; }}
        h3 {{ font-size: 1em !important; }}
    }}
    
    /* Sloka Cards */
    .sloka-card {{
        background-color: {theme['bg_card']};
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid {theme['card_border']}; 
        margin-bottom: 12px;
        border: 1px solid {theme['border']};
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }}
    
    .sloka-ref {{ 
        color: {theme['text_secondary']}; 
        font-size: {current_font['ref']}; 
        font-weight: 700; 
        text-transform: uppercase; 
        margin-bottom: 8px;
        letter-spacing: 0.5px;
    }}
    
    .sloka-text {{ 
        font-size: {current_font['sloka']}; 
        line-height: 1.8; 
        color: {theme['text_primary']}; 
        font-family: 'Noto Sans Devanagari', 'Adobe Devanagari', 'Mangal', serif;
    }}
    
    .sloka-iast {{ 
        font-size: {current_font['iast']}; 
        color: {theme['text_secondary']}; 
        font-style: italic; 
        margin-top: 8px;
        padding-top: 8px;
        border-top: 1px dashed {theme['border']};
    }}
    
    /* Pure Read Mode */
    .pure-sloka {{
        background-color: {theme['sloka_bg']};
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 15px;
        border: 1px solid {theme['border']};
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
    }}
    
    .sloka-devanagari {{
        font-size: {current_font['sloka']};
        line-height: 2;
        font-family: 'Noto Sans Devanagari', 'Adobe Devanagari', serif;
        color: {theme['text_primary']};
    }}
    
    .sloka-iast-display {{
        font-size: {current_font['iast']};
        color: {theme['text_secondary']};
        font-style: italic;
        margin-top: 12px;
        padding-top: 12px;
        border-top: 1px dashed {theme['border']};
    }}
    
    /* Highlights */
    .highlight-exact {{ 
        background-color: {theme['highlight_exact_bg']}; 
        color: {theme['highlight_exact']}; 
        padding: 2px 5px; 
        border-radius: 4px; 
        font-weight: bold;
    }}
    
    .highlight-compound {{ 
        background-color: {theme['highlight_compound_bg']}; 
        color: {theme['highlight_compound']}; 
        padding: 2px 5px; 
        border-radius: 4px;
    }}
    
    /* Stats Container */
    .stats-container {{ 
        padding: 12px 15px; 
        background-color: {theme['bg_secondary']}; 
        border: 1px solid {theme['border']}; 
        border-radius: 8px; 
        color: {theme['success']}; 
        font-weight: bold; 
        text-align: center; 
        margin-bottom: 15px;
        font-size: {current_font['body']};
    }}
    
    .section-header {{ 
        padding: 10px 12px; 
        background-color: {theme['bg_secondary']}; 
        border-radius: 6px; 
        margin: 20px 0 12px 0; 
        font-weight: bold; 
        font-size: {current_font['body']};
        color: {theme['text_primary']}; 
        border-left: 4px solid {theme['accent_secondary']}; 
    }}
    
    /* Progress Bar */
    .progress-container {{
        background-color: {theme['bg_secondary']};
        padding: 10px 15px;
        border-radius: 8px;
        margin-bottom: 15px;
        border: 1px solid {theme['border']};
        color: {theme['text_primary']};
    }}
    
    .progress-bar {{
        background-color: {theme['border']};
        border-radius: 10px;
        height: 8px;
        overflow: hidden;
    }}
    
    .progress-fill {{
        background: linear-gradient(90deg, {theme['accent']}, {theme['accent_secondary']});
        height: 100%;
        border-radius: 10px;
        transition: width 0.3s ease;
    }}
    
    /* Compare columns */
    .compare-header {{
        font-weight: bold;
        font-size: 1.1em;
        color: {theme['text_primary']};
        padding-bottom: 10px;
        border-bottom: 3px solid {theme['accent']};
        margin-bottom: 15px;
        text-align: center;
    }}
    
    /* Buttons */
    .stButton>button {{ 
        width: 100%; 
        border-radius: 6px; 
        font-size: {current_font['body']}; 
    }}
    
    /* Tables */
    .trans-table {{
        width: 100%;
        border-collapse: collapse;
        margin: 15px 0;
        font-size: {current_font['body']};
    }}
    
    .trans-table th {{
        background-color: {theme['table_header']};
        color: #ffffff;
        padding: 10px;
        text-align: center;
        font-weight: bold;
    }}
    
    .trans-table td {{
        padding: 8px 10px;
        border: 1px solid {theme['border']};
        text-align: center;
        background-color: {theme['bg_card']};
        color: {theme['text_primary']};
    }}
    
    .trans-table tr:nth-child(even) td {{
        background-color: {theme['bg_secondary']};
    }}
    
    /* Chapter Index */
    .chapter-card {{
        background-color: {theme['bg_secondary']};
        padding: 12px 15px;
        border-radius: 8px;
        margin-bottom: 8px;
        border-left: 4px solid {theme['accent']};
        cursor: pointer;
        transition: all 0.2s ease;
    }}
    
    .chapter-card:hover {{
        background-color: {theme['border']};
        transform: translateX(5px);
    }}
    
    /* Frequency Analysis */
    .freq-bar {{
        background-color: {theme['border']};
        border-radius: 4px;
        height: 24px;
        overflow: hidden;
        margin: 5px 0;
    }}
    
    .freq-fill {{
        background: linear-gradient(90deg, {theme['accent']}, {theme['accent_secondary']});
        height: 100%;
        display: flex;
        align-items: center;
        padding-left: 10px;
        color: white;
        font-size: 0.85em;
        font-weight: bold;
    }}
    
    /* Settings panel */
    .settings-info {{
        background-color: {theme['bg_secondary']};
        padding: 12px;
        border-radius: 8px;
        margin: 10px 0;
        font-size: 0.9em;
        color: {theme['text_secondary']};
    }}
    
    /* Streamlit native overrides for dark mode */
    .stMarkdown, .stMarkdown p, .stMarkdown li {{
        color: {theme['text_primary']} !important;
    }}
    
    .stExpander {{
        background-color: {theme['bg_secondary']};
        border: 1px solid {theme['border']};
        border-radius: 8px;
    }}
    
    .stExpander summary {{
        color: {theme['text_primary']} !important;
    }}
    
    .stMetric label {{
        color: {theme['text_secondary']} !important;
    }}
    
    .stMetric [data-testid="stMetricValue"] {{
        color: {theme['text_primary']} !important;
    }}
    
    .stMetric [data-testid="stMetricDelta"] {{
        color: {theme['text_secondary']} !important;
    }}
    
    .stSelectbox label, .stTextInput label, .stMultiSelect label {{
        color: {theme['text_primary']} !important;
    }}
    
    .stCaption {{
        color: {theme['text_secondary']} !important;
    }}
    
    /* Info/Warning/Success boxes */
    .stAlert {{
        color: {theme['text_primary']} !important;
    }}
    
    /* Sidebar text */
    [data-testid="stSidebar"] {{
        background-color: {theme['bg_secondary']};
    }}
    
    [data-testid="stSidebar"] .stMarkdown {{
        color: {theme['text_primary']} !important;
    }}
    
    [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {{
        color: {theme['text_primary']} !important;
    }}
</style>
""", unsafe_allow_html=True)

# ---------------- 5. DATA LOADING ----------------
DATA_FILE = "all3_cleaned.xlsx"

# Samhita and Sthana ordering
SAMHITA_ORDER = {
    'charaka': 1, 'caraka': 1,
    'sushruta': 2, 'susruta': 2, 'suśruta': 2,
    'astanga': 3, 'ashtanga': 3, 'aṣṭāṅga': 3, 'astangahrdaya': 3, 'ashtangahridaya': 3
}

STHANA_ORDER = {
    'sutra': 1, 'sūtra': 1, 'sutrasthana': 1,
    'nidana': 2, 'nidāna': 2, 'nidanasthana': 2,
    'vimana': 3, 'vimāna': 3, 'vimanasthana': 3,
    'sharira': 4, 'śārīra': 4, 'sharirasthana': 4,
    'indriya': 5, 'indriyasthana': 5,
    'chikitsa': 6, 'cikitsā': 6, 'cikitsa': 6, 'chikitsasthana': 6,
    'kalpa': 7, 'kalpasthana': 7,
    'siddhi': 8, 'siddhisthana': 8,
    'uttara': 9, 'uttarasthana': 9, 'uttaratantra': 9
}

def get_samhita_order(name):
    name_lower = str(name).lower().replace('_', '').replace(' ', '')
    for key, order in SAMHITA_ORDER.items():
        if key in name_lower:
            return order
    return 99

def get_sthana_order(name):
    name_lower = str(name).lower().replace('_', '').replace(' ', '')
    for key, order in STHANA_ORDER.items():
        if key in name_lower:
            return order
    return 99

def sort_samhitas(samhita_list):
    return sorted(samhita_list, key=get_samhita_order)

def sort_sthanas(sthana_list):
    return sorted(sthana_list, key=get_sthana_order)

@st.cache_data(show_spinner="Loading Bhruhat Trayi corpus...", ttl=3600)
def load_data():
    try:
        df = pd.read_excel(DATA_FILE, engine='openpyxl')
        
        required_cols = ["Sloka Text", "IAST", "Roman", "ASCII", "File Name", "Sthana", "Chapter", "Sloka_Number_Int"]
        
        for c in required_cols:
            if c not in df.columns:
                df[c] = ""
        
        for c in ["Sloka Text", "IAST", "Roman", "ASCII", "File Name", "Sthana", "Chapter"]:
            df[c] = df[c].astype(str).fillna("")
            df[c] = df[c].apply(lambda x: unicodedata.normalize('NFC', str(x)))
        
        df["Sloka_Number_Int"] = pd.to_numeric(df["Sloka_Number_Int"], errors="coerce").fillna(0).astype(int)
        
        # Add unique index for tracking
        df = df.reset_index(drop=True)
        df['_idx'] = df.index
        
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

df = load_data()

# ---------------- 6. CORE FUNCTIONS ----------------

def get_clean_tokens(text):
    if not text: return []
    for char in string.punctuation + "।॥|":
        text = text.replace(char, " ")
    return [t.strip().lower() for t in text.split() if len(t.strip()) > 1]

def count_occurrences(text, query):
    """Count how many times a query appears in text (case-insensitive)"""
    if not text or not query:
        return 0
    text_lower = str(text).lower()
    query_lower = query.lower()
    return text_lower.count(query_lower)

def count_total_occurrences(row, query):
    """Count total occurrences across all searchable columns"""
    total = 0
    for col in ["Sloka Text", "IAST", "Roman", "ASCII"]:
        total += count_occurrences(row.get(col, ""), query)
    return total

@st.cache_data(show_spinner=False)
def get_suggestions_cached(query, corpus_hash):
    query_lower = query.lower().strip()
    suggestions = {}
    
    sample_df = df.head(10000)
    
    for col in ["IAST", "Sloka Text"]:
        tokens = get_clean_tokens(" ".join(sample_df[col].tolist()))
        
        for token in tokens:
            if query_lower in token.lower() and len(token) >= 2:
                if token not in suggestions:
                    suggestions[token] = {'count': 0, 'type': 'exact'}
                suggestions[token]['count'] += 1
                
                if token.lower() == query_lower:
                    suggestions[token]['type'] = 'exact'
                else:
                    suggestions[token]['type'] = 'compound'
    
    sorted_sugg = sorted(
        suggestions.items(),
        key=lambda x: (0 if x[1]['type'] == 'exact' else 1, -x[1]['count'])
    )
    
    return [{'term': t, 'freq': d['count'], 'type': d['type']} for t, d in sorted_sugg[:30]]

def highlight_text(text, query, h_type='partial'):
    if not text or not query: return text
    css_map = {'exact': 'highlight-exact', 'compound': 'highlight-compound', 'partial': 'highlight-partial'}
    css = css_map.get(h_type, 'highlight-partial')
    try:
        return re.sub(re.escape(query), lambda m: f"<span class='{css}'>{m.group(0)}</span>", str(text), flags=re.IGNORECASE)
    except:
        return str(text)

def display_samhita(name):
    return name.replace("_", " ").title() if isinstance(name, str) else name

def check_match_type(text, query):
    if not text or not query: return False, 'none'
    text_lower = str(text).lower()
    query_lower = query.lower()
    
    if query_lower not in text_lower:
        return False, 'none'
    
    tokens = get_clean_tokens(text)
    if query_lower in [t.lower() for t in tokens]:
        return True, 'exact'
    
    return True, 'compound'

def find_cross_references(sloka_text, current_samhita, df):
    """Find similar content in other Samhitas - only return if matches found"""
    keywords = get_clean_tokens(sloka_text)[:5]
    if not keywords:
        return {}
    
    cross_refs = {}
    other_samhitas = [s for s in df["File Name"].unique() if s != current_samhita]
    
    for sam in sort_samhitas(other_samhitas):
        sam_df = df[df["File Name"] == sam]
        matches = []
        
        for _, row in sam_df.head(2000).iterrows():
            row_text = f"{row['Sloka Text']} {row['IAST']}".lower()
            match_count = sum(1 for kw in keywords if kw in row_text)
            if match_count >= 2:
                matches.append({
                    'sthana': row['Sthana'],
                    'chapter': row['Chapter'],
                    'sloka_num': int(row['Sloka_Number_Int']),
                    'text': str(row['Sloka Text'])[:100],
                    'match_score': match_count
                })
        
        matches.sort(key=lambda x: -x['match_score'])
        if matches:
            cross_refs[sam] = matches[:3]
    
    return cross_refs

@st.cache_data(show_spinner=False)
def get_chapter_index(df):
    """Generate chapter index for all samhitas"""
    index = {}
    
    for sam in sort_samhitas(df["File Name"].unique().tolist()):
        sam_df = df[df["File Name"] == sam]
        index[sam] = {}
        
        for sthana in sort_sthanas(sam_df["Sthana"].unique().tolist()):
            sthana_df = sam_df[sam_df["Sthana"] == sthana]
            chapters = []
            
            for chap in sorted(sthana_df["Chapter"].unique(), key=str):
                chap_df = sthana_df[sthana_df["Chapter"] == chap]
                chapters.append({
                    'name': chap,
                    'sloka_count': len(chap_df),
                    'start': int(chap_df["Sloka_Number_Int"].min()) if len(chap_df) > 0 else 1,
                    'end': int(chap_df["Sloka_Number_Int"].max()) if len(chap_df) > 0 else 1
                })
            
            index[sam][sthana] = chapters
    
    return index

@st.cache_data(show_spinner=False)
def get_word_frequency_analysis(query, df):
    """Analyze word frequency across the corpus"""
    query_lower = query.lower().strip()
    
    results = {
        'total_occurrences': 0,
        'total_slokas': 0,
        'by_samhita': {},
        'by_sthana': {},
        'top_chapters': []
    }
    
    chapter_counts = []
    
    for sam in sort_samhitas(df["File Name"].unique().tolist()):
        sam_df = df[df["File Name"] == sam]
        sam_occurrences = 0
        sam_slokas = 0
        
        for _, row in sam_df.iterrows():
            search_text = f"{row['Sloka Text']} {row['IAST']} {row['Roman']} {row['ASCII']}".lower()
            occ_count = search_text.count(query_lower)
            
            if occ_count > 0:
                sam_occurrences += occ_count
                sam_slokas += 1
                
                chapter_counts.append({
                    'samhita': sam,
                    'sthana': row['Sthana'],
                    'chapter': row['Chapter'],
                    'occurrences': occ_count
                })
        
        results['by_samhita'][sam] = {
            'occurrences': sam_occurrences,
            'slokas': sam_slokas
        }
        results['total_occurrences'] += sam_occurrences
        results['total_slokas'] += sam_slokas
    
    # Aggregate by chapter
    chapter_agg = {}
    for item in chapter_counts:
        key = f"{item['samhita']}|{item['sthana']}|{item['chapter']}"
        if key not in chapter_agg:
            chapter_agg[key] = {
                'samhita': item['samhita'],
                'sthana': item['sthana'],
                'chapter': item['chapter'],
                'occurrences': 0,
                'slokas': 0
            }
        chapter_agg[key]['occurrences'] += item['occurrences']
        chapter_agg[key]['slokas'] += 1
    
    # Sort by occurrences
    results['top_chapters'] = sorted(chapter_agg.values(), key=lambda x: -x['occurrences'])[:10]
    
    return results

# ---------------- 7. SIDEBAR SETTINGS ----------------
with st.sidebar:
    st.markdown("## ⚙️ Settings")
    
    st.markdown("---")
    
    # Dark Mode Toggle
    st.markdown("### 🌓 Display Mode")
    dark_mode = st.toggle("Dark Mode", value=st.session_state.dark_mode, key="dark_toggle")
    if dark_mode != st.session_state.dark_mode:
        st.session_state.dark_mode = dark_mode
        st.rerun()
    
    st.markdown("---")
    
    # Font Size
    st.markdown("### 🔤 Font Size")
    font_choice = st.select_slider(
        "Adjust text size:",
        options=["Small", "Medium", "Large", "Extra Large"],
        value=st.session_state.font_size,
        key="font_slider"
    )
    if font_choice != st.session_state.font_size:
        st.session_state.font_size = font_choice
        st.rerun()
    
    st.markdown("---")
    
    st.markdown("""
    <div class="settings-info">
        <strong>💡 Tips:</strong><br>
        • Dark mode reduces eye strain<br>
        • Larger fonts help with Devanagari<br>
        • Settings persist during session
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### 📊 Corpus Statistics")
    if not df.empty:
        total_slokas = len(df)
        samhita_counts = df["File Name"].value_counts()
        
        st.metric("Total Ślokas", f"{total_slokas:,}")
        
        for sam in sort_samhitas(samhita_counts.index.tolist()):
            st.caption(f"{display_samhita(sam)}: {samhita_counts[sam]:,}")

# ---------------- 8. MAIN UI ----------------

st.title("📜 e-Bhruhat Trayi Exploration by PraKul")
st.caption("Advanced Bhruhat Trayī Exploration — A Technological Contribution from Prof. (Dr.) Prasanna Kulkarni")

# Create tabs
tab_read, tab_search, tab_compare, tab_index, tab_frequency, tab_guide = st.tabs([
    "📖 Read Samhita",
    "🔍 Search",
    "⚖️ Compare Texts",
    "📑 Chapter Index",
    "📊 Word Frequency",
    "ℹ️ Guide"
])

# ============================================================================
# TAB 1: READ SAMHITA
# ============================================================================
with tab_read:
    st.markdown("### 📖 Read Samhita")
    
    sorted_samhitas = sort_samhitas(df["File Name"].unique().tolist())
    
    # Selection row
    col1, col2, col3 = st.columns(3)
    
    with col1:
        r_sam = st.selectbox("Samhita", sorted_samhitas, format_func=display_samhita, key="read_sam")
    
    with col2:
        available_sthanas = sort_sthanas(df[df["File Name"]==r_sam]["Sthana"].unique().tolist())
        r_sth = st.selectbox("Sthana", available_sthanas, key="read_sth")
    
    with col3:
        available_chapters = sorted(df[(df["File Name"]==r_sam)&(df["Sthana"]==r_sth)]["Chapter"].unique(), key=str)
        r_chap = st.selectbox("Chapter", available_chapters, key="read_chap")
    
    # Get chapter data
    chapter_data = df[(df["File Name"]==r_sam)&(df["Sthana"]==r_sth)&(df["Chapter"]==r_chap)].sort_values("Sloka_Number_Int")
    total_slokas_in_chapter = len(chapter_data)
    
    if total_slokas_in_chapter > 0:
        min_sloka = int(chapter_data["Sloka_Number_Int"].min())
        max_sloka = int(chapter_data["Sloka_Number_Int"].max())
        
        # Chapter Statistics
        st.markdown(f"""
        <div class="progress-container">
            <strong>📊 Chapter Statistics:</strong> {total_slokas_in_chapter} ślokas (#{min_sloka} to #{max_sloka})
        </div>
        """, unsafe_allow_html=True)
        
        # Quick Jump
        st.markdown("**🚀 Quick Jump:**")
        col_jump1, col_jump2, col_jump3, col_jump4 = st.columns(4)
        
        with col_jump1:
            if st.button("⏮️ Start", use_container_width=True, key="jump_start"):
                st.session_state.read_pos = min_sloka
                st.rerun()
        
        with col_jump2:
            jump_options = list(range(min_sloka, max_sloka + 1, 20))
            if jump_options:
                jump_to = st.selectbox("Go to śloka:", jump_options, key="jump_select", label_visibility="collapsed")
        
        with col_jump3:
            if st.button("📍 Jump", use_container_width=True, key="jump_go"):
                st.session_state.read_pos = jump_to
                st.rerun()
        
        with col_jump4:
            if st.button("⏭️ End", use_container_width=True, key="jump_end"):
                st.session_state.read_pos = max(min_sloka, max_sloka - 19)
                st.rerun()
        
        # Ensure read_pos is valid
        if st.session_state.read_pos < min_sloka:
            st.session_state.read_pos = min_sloka
        
        # Progress bar
        current_pos = st.session_state.read_pos
        progress_pct = min(100, ((current_pos - min_sloka) / max(1, max_sloka - min_sloka)) * 100)
        
        st.markdown(f"""
        <div class="progress-container">
            <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                <span>Viewing from #{current_pos}</span>
                <span>{progress_pct:.0f}% through chapter</span>
            </div>
            <div class="progress-bar">
                <div class="progress-fill" style="width: {progress_pct}%;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Display 20 slokas
        view = chapter_data[chapter_data["Sloka_Number_Int"] >= st.session_state.read_pos].head(20)
        
        if not view.empty:
            for idx, (_, r) in enumerate(view.iterrows()):
                sloka_num = int(r['Sloka_Number_Int'])
                
                st.markdown(f"""
                <div class="pure-sloka">
                    <div class="sloka-devanagari">{r['Sloka Text']}</div>
                    <div class="sloka-iast-display">{r['IAST']} ॥{sloka_num}॥</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Cross-reference - ONLY show if there are matches
                cross_refs = find_cross_references(str(r['Sloka Text']), r_sam, df)
                
                if cross_refs:
                    with st.expander(f"🔗 Found similar in other Samhitas (Śloka {sloka_num})"):
                        for sam_name, refs in cross_refs.items():
                            st.markdown(f"**{display_samhita(sam_name)}:** {len(refs)} reference(s)")
                            for ref in refs:
                                st.caption(f"  → {ref['sthana']} | {ref['chapter']} | #{ref['sloka_num']}")
            
            # Navigation
            st.markdown("---")
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col1:
                if current_pos > min_sloka:
                    if st.button("⬅️ Previous 20", use_container_width=True):
                        st.session_state.read_pos = max(min_sloka, current_pos - 20)
                        st.rerun()
            
            with col2:
                end_sloka = int(view.iloc[-1]['Sloka_Number_Int'])
                st.markdown(f"<div style='text-align:center; padding:10px;'>Showing #{current_pos} - #{end_sloka} of {total_slokas_in_chapter}</div>", unsafe_allow_html=True)
            
            with col3:
                if end_sloka < max_sloka:
                    if st.button("Next 20 ➡️", use_container_width=True):
                        st.session_state.read_pos = end_sloka + 1
                        st.rerun()
        else:
            st.info("No ślokas found for the selected position.")
    else:
        st.warning("No ślokas found for the selected chapter.")

# ============================================================================
# TAB 2: SEARCH
# ============================================================================
with tab_search:
    st.markdown("### 🔍 Search Across Texts")
    
    col1, col2 = st.columns([4, 1])
    with col1:
        search_input = st.text_input(
            "Search term:",
            value=st.session_state.main_query,
            placeholder="vata / agni / pitta / आत्रेय / prasanna...",
            key="search_input"
        )
    with col2:
        st.write("")
        if st.button("🔍", type="primary", use_container_width=True):
            st.session_state.strict_mode = False
            st.session_state.filter_mode = "all"
            st.session_state.search_page = 0

    if search_input != st.session_state.main_query:
        st.session_state.main_query = search_input
        st.session_state.strict_mode = False
        st.session_state.search_page = 0

    query = st.session_state.main_query.strip()
    
    # Suggestions
    if query and not st.session_state.strict_mode:
        with st.expander("✨ Suggestions", expanded=True):
            corpus_hash = hash(tuple(df["File Name"].unique()))
            suggestions = get_suggestions_cached(query, corpus_hash)
            
            if suggestions:
                total_freq = sum(s['freq'] for s in suggestions)
                exact_cnt = sum(1 for s in suggestions if s['type'] == 'exact')
                
                st.info(f"📊 {len(suggestions)} forms | {total_freq} occurrences | {exact_cnt} exact matches")
                
                cols = st.columns(4)
                for i, item in enumerate(suggestions[:16]):
                    emoji = "🎯" if item['type'] == 'exact' else "📦"
                    with cols[i % 4]:
                        if st.button(f"{emoji} {item['term']} ({item['freq']})", key=f"s_{i}", use_container_width=True):
                            st.session_state.main_query = item['term']
                            st.session_state.strict_mode = True
                            st.session_state.search_page = 0
                            st.rerun()

    # Execute search
    if query:
        st.markdown("---")
        
        sorted_samhitas = sort_samhitas(df["File Name"].unique().tolist())
        selected_sam = st.multiselect(
            "Filter by Samhita:",
            sorted_samhitas,
            default=sorted_samhitas,
            format_func=display_samhita
        )
        
        corpus = df[df["File Name"].isin(selected_sam)]
        exact_results = []
        compound_results = []
        total_occurrences = 0
        
        with st.spinner("Searching corpus..."):
            for _, row in corpus.iterrows():
                found = False
                m_type = 'none'
                row_occurrences = 0
                
                # Search across all relevant columns and count occurrences
                for col in ["Sloka Text", "IAST", "Roman", "ASCII"]:
                    col_text = str(row[col])
                    occ_count = count_occurrences(col_text, query)
                    row_occurrences += occ_count
                    
                    if occ_count > 0:
                        found = True
                        is_match, mt = check_match_type(col_text, query)
                        if mt == 'exact':
                            m_type = 'exact'
                        elif mt == 'compound' and m_type != 'exact':
                            m_type = 'compound'
                
                if found:
                    total_occurrences += row_occurrences
                    row_dict = row.to_dict()
                    row_dict['_match_type'] = m_type
                    row_dict['_occurrences'] = row_occurrences
                    
                    if m_type == 'exact':
                        exact_results.append(row_dict)
                    else:
                        compound_results.append(row_dict)
        
        total_slokas = len(exact_results) + len(compound_results)
        
        if total_slokas == 0:
            st.warning(f"No results for '{query}'.")
        else:
            # Show occurrences AND slokas count (like old version)
            st.markdown(
                f"""<div class="stats-container">
                ✅ Total occurrences: <strong>{total_occurrences}</strong> in <strong>{total_slokas}</strong> ślokas | 
                🎯 {len(exact_results)} exact | 📦 {len(compound_results)} compound
                </div>""",
                unsafe_allow_html=True
            )
            
            # Filter buttons
            c1, c2, c3 = st.columns(3)
            with c1:
                if st.button(f"All ({total_slokas})", use_container_width=True):
                    st.session_state.filter_mode = "all"
                    st.session_state.search_page = 0
                    st.rerun()
            with c2:
                if st.button(f"Exact ({len(exact_results)})", use_container_width=True):
                    st.session_state.filter_mode = "exact"
                    st.session_state.search_page = 0
                    st.rerun()
            with c3:
                if st.button(f"Compound ({len(compound_results)})", use_container_width=True):
                    st.session_state.filter_mode = "compound"
                    st.session_state.search_page = 0
                    st.rerun()
            
            st.markdown("---")
            
            mode = st.session_state.filter_mode
            
            # Combine results based on filter
            if mode == "exact":
                all_results = exact_results
            elif mode == "compound":
                all_results = compound_results
            else:
                all_results = exact_results + compound_results
            
            # Pagination (50 per page)
            RESULTS_PER_PAGE = 50
            total_results = len(all_results)
            total_pages = max(1, (total_results + RESULTS_PER_PAGE - 1) // RESULTS_PER_PAGE)
            current_page = min(st.session_state.search_page, total_pages - 1)
            
            start_idx = current_page * RESULTS_PER_PAGE
            end_idx = min(start_idx + RESULTS_PER_PAGE, total_results)
            
            # Page info
            st.markdown(f"**Showing {start_idx + 1} - {end_idx} of {total_results} results**")
            
            # Display results
            for row_dict in all_results[start_idx:end_idx]:
                match_type = row_dict.get('_match_type', 'compound')
                occ = row_dict.get('_occurrences', 1)
                
                st.markdown(
                    f"""<div class="sloka-card">
                    <div class="sloka-ref">{display_samhita(row_dict['File Name'])} | {row_dict['Sthana']} | {row_dict['Chapter']} | #{int(row_dict['Sloka_Number_Int'])} | <span style="color:{theme['accent']};">{occ} occurrence(s)</span></div>
                    <div class="sloka-text">{highlight_text(row_dict['Sloka Text'], query, match_type)}</div>
                    <div class="sloka-iast">{highlight_text(row_dict['IAST'], query, match_type)}</div>
                    </div>""",
                    unsafe_allow_html=True
                )
            
            # Pagination controls
            if total_pages > 1:
                st.markdown("---")
                col1, col2, col3, col4, col5 = st.columns([1, 1, 2, 1, 1])
                
                with col1:
                    if current_page > 0:
                        if st.button("⏮️ First", use_container_width=True):
                            st.session_state.search_page = 0
                            st.rerun()
                
                with col2:
                    if current_page > 0:
                        if st.button("◀️ Prev", use_container_width=True):
                            st.session_state.search_page = current_page - 1
                            st.rerun()
                
                with col3:
                    st.markdown(f"<div style='text-align:center; padding:10px;'>Page {current_page + 1} of {total_pages}</div>", unsafe_allow_html=True)
                
                with col4:
                    if current_page < total_pages - 1:
                        if st.button("Next ▶️", use_container_width=True):
                            st.session_state.search_page = current_page + 1
                            st.rerun()
                
                with col5:
                    if current_page < total_pages - 1:
                        if st.button("Last ⏭️", use_container_width=True):
                            st.session_state.search_page = total_pages - 1
                            st.rerun()

# ============================================================================
# TAB 3: COMPARE
# ============================================================================
with tab_compare:
    st.markdown("### ⚖️ Compare Texts Across Samhitas")
    st.markdown("*Side-by-side comparison: Charaka | Sushruta | Astanga*")
    
    comp_term = st.text_input("Term to compare:", placeholder="e.g., vata, agni, dosha, prasanna...", key="comp_input")
    
    if st.button("🔍 Compare", type="primary", key="compare_btn") and comp_term:
        
        samhitas = sort_samhitas(df["File Name"].unique().tolist())
        
        results = {}
        total_occ_by_sam = {}
        
        for sam in samhitas:
            sam_df = df[df["File Name"] == sam]
            matches = []
            sam_total_occ = 0
            
            for _, row in sam_df.iterrows():
                search_text = f"{row['Sloka Text']} {row['IAST']} {row['Roman']} {row['ASCII']}".lower()
                occ_count = search_text.count(comp_term.lower())
                
                if occ_count > 0:
                    sam_total_occ += occ_count
                    matches.append({
                        'sthana': row['Sthana'],
                        'chapter': row['Chapter'],
                        'sloka_num': int(row['Sloka_Number_Int']),
                        'text': str(row['Sloka Text']),
                        'occurrences': occ_count
                    })
            
            results[sam] = matches
            total_occ_by_sam[sam] = sam_total_occ
        
        # Summary metrics
        st.markdown("---")
        st.markdown("#### 📊 Summary")
        summary_cols = st.columns(len(samhitas))
        for i, sam in enumerate(samhitas):
            with summary_cols[i]:
                st.metric(
                    display_samhita(sam), 
                    f"{total_occ_by_sam[sam]} occ",
                    f"in {len(results[sam])} ślokas"
                )
        
        st.markdown("---")
        st.markdown("#### 📜 Side-by-Side Comparison")
        
        # Side-by-side columns
        compare_cols = st.columns(len(samhitas))
        
        for i, sam in enumerate(samhitas):
            with compare_cols[i]:
                st.markdown(f"""<div class="compare-header">{display_samhita(sam)}</div>""", unsafe_allow_html=True)
                
                matches = results[sam]
                
                if matches:
                    for j, r in enumerate(matches[:5]):
                        st.markdown(f"""
                        <div style="background-color: {theme['bg_secondary']}; padding: 10px; border-radius: 5px; margin-bottom: 8px; border-left: 3px solid {theme['accent']}; font-size: 0.9em;">
                            <small style="color: {theme['text_secondary']};">{r['sthana']} | {r['chapter']} | #{r['sloka_num']} ({r['occurrences']} occ)</small><br>
                            <span style="color: {theme['text_primary']};">{highlight_text(r['text'][:120], comp_term, 'exact')}...</span>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    if len(matches) > 5:
                        with st.expander(f"See {len(matches) - 5} more"):
                            for r in matches[5:20]:
                                st.caption(f"{r['sthana']} | {r['chapter']} | #{r['sloka_num']} ({r['occurrences']} occ)")
                                st.markdown(f"{r['text'][:80]}...")
                                st.markdown("---")
                else:
                    st.info("No references found")

# ============================================================================
# TAB 4: CHAPTER INDEX
# ============================================================================
with tab_index:
    st.markdown("### 📑 Chapter Index")
    st.markdown("*Quick navigation to any chapter in the corpus*")
    
    chapter_index = get_chapter_index(df)
    
    # Samhita selection
    idx_sam = st.selectbox(
        "Select Samhita:",
        sort_samhitas(list(chapter_index.keys())),
        format_func=display_samhita,
        key="idx_sam"
    )
    
    if idx_sam in chapter_index:
        st.markdown("---")
        
        # Display sthanas and chapters
        for sthana, chapters in chapter_index[idx_sam].items():
            with st.expander(f"📚 **{sthana}** ({len(chapters)} chapters, {sum(c['sloka_count'] for c in chapters)} ślokas)", expanded=False):
                
                for chap in chapters:
                    col1, col2, col3 = st.columns([3, 1, 1])
                    
                    with col1:
                        st.markdown(f"**{chap['name']}**")
                    
                    with col2:
                        st.caption(f"{chap['sloka_count']} ślokas")
                    
                    with col3:
                        if st.button("📖 Read", key=f"idx_{idx_sam}_{sthana}_{chap['name']}", use_container_width=True):
                            # Set read state and switch to Read tab
                            st.session_state.read_pos = chap['start']
                            st.success(f"Go to **Read Samhita** tab → Select {sthana} → {chap['name']}")
        
        # Summary
        st.markdown("---")
        total_chapters = sum(len(chapters) for chapters in chapter_index[idx_sam].values())
        total_slokas = sum(sum(c['sloka_count'] for c in chapters) for chapters in chapter_index[idx_sam].values())
        
        st.markdown(f"""
        <div class="stats-container">
            📊 <strong>{display_samhita(idx_sam)}</strong>: {len(chapter_index[idx_sam])} Sthānas | {total_chapters} Chapters | {total_slokas:,} Ślokas
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# TAB 5: WORD FREQUENCY ANALYSIS
# ============================================================================
with tab_frequency:
    st.markdown("### 📊 Word Frequency Analysis")
    st.markdown("*Analyze distribution of any term across the corpus*")
    
    freq_term = st.text_input("Enter term to analyze:", placeholder="e.g., vata, agni, dosha, prasanna...", key="freq_input")
    
    if st.button("📊 Analyze Frequency", type="primary", key="freq_btn") and freq_term:
        
        with st.spinner("Analyzing corpus..."):
            freq_data = get_word_frequency_analysis(freq_term, df)
        
        if freq_data['total_occurrences'] == 0:
            st.warning(f"No occurrences of '{freq_term}' found in the corpus.")
        else:
            # Overall stats
            st.markdown("---")
            st.markdown("#### 📈 Overall Statistics")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Occurrences", f"{freq_data['total_occurrences']:,}")
            with col2:
                st.metric("Found in Ślokas", f"{freq_data['total_slokas']:,}")
            
            # Distribution by Samhita
            st.markdown("---")
            st.markdown("#### 📚 Distribution by Samhita")
            
            max_occ = max(d['occurrences'] for d in freq_data['by_samhita'].values()) if freq_data['by_samhita'] else 1
            
            for sam in sort_samhitas(list(freq_data['by_samhita'].keys())):
                data = freq_data['by_samhita'][sam]
                pct = (data['occurrences'] / max_occ) * 100
                
                st.markdown(f"**{display_samhita(sam)}**")
                st.markdown(f"""
                <div class="freq-bar">
                    <div class="freq-fill" style="width: {pct}%;">{data['occurrences']} occurrences in {data['slokas']} ślokas</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Top chapters
            st.markdown("---")
            st.markdown("#### 🏆 Top Chapters by Frequency")
            
            if freq_data['top_chapters']:
                for i, chap in enumerate(freq_data['top_chapters'][:10], 1):
                    col1, col2, col3 = st.columns([3, 1, 1])
                    
                    with col1:
                        st.markdown(f"**{i}. {display_samhita(chap['samhita'])}** → {chap['sthana']} → {chap['chapter']}")
                    
                    with col2:
                        st.markdown(f"🔢 {chap['occurrences']} occ")
                    
                    with col3:
                        st.markdown(f"📄 {chap['slokas']} ślokas")

# ============================================================================
# TAB 6: GUIDE
# ============================================================================
with tab_guide:
    st.markdown("""
    # 📘 User Guide
    
    Welcome to **e-Bhruhat Trayi Exploration by PraKul** — your digital companion for exploring classical Āyurvedic literature.
    
    ---
    
    ## ⚙️ Settings (Sidebar)
    
    Access settings from the **sidebar** (click `>` on mobile):
    
    | Setting | Options | Description |
    |---------|---------|-------------|
    | **Display Mode** | Light / Dark | Dark mode reduces eye strain during extended reading |
    | **Font Size** | Small / Medium / Large / Extra Large | Adjust for comfortable Devanagari reading |
    
    ---
    
    ## 📖 Read Samhita
    
    **Sequential reading with navigation features:**
    
    - **Chapter Statistics:** See total ślokas in selected chapter
    - **Quick Jump:** Jump to any position instantly
    - **Progress Bar:** Track your reading progress
    - **Cross-References:** Find similar content in other Samhitas (shown only when matches exist)
    - **20 ślokas per page** for comfortable reading
    
    ---
    
    ## 🔍 Search
    
    **Comprehensive search across all texts:**
    
    - **Total Occurrences:** Shows how many times the word appears (e.g., "74 occurrences in 29 ślokas")
    - **🎯 Exact matches:** Term as standalone word
    - **📦 Compound matches:** Term within compounds
    - **Suggestions:** Click to search exact forms
    - **Pagination:** Navigate through all results (50 per page)
    - **Filter:** By Samhita or match type
    
    ---
    
    ## ⚖️ Compare Texts
    
    **Side-by-side comparison in columns:**
    
    | Charaka | Sushruta | Astanga |
    |---------|----------|---------|
    | Results | Results  | Results |
    
    Shows occurrence counts per Samhita for easy comparison.
    
    ---
    
    ## 📑 Chapter Index
    
    **Quick navigation to any chapter:**
    
    - Browse all Sthānas and Chapters
    - See śloka counts per chapter
    - One-click navigation to start reading
    - Summary statistics for each Samhita
    
    ---
    
    ## 📊 Word Frequency Analysis
    
    **Deep analysis of term distribution:**
    
    - Total occurrences across corpus
    - Visual distribution by Samhita
    - Top 10 chapters with highest frequency
    - Useful for research and comparative studies
    
    ---
    
    ## 🔤 Sanskrit Transliteration Reference
    
    ### Vowels (Svara)
    """)
    
    st.markdown("""
    <table class="trans-table">
        <tr>
            <th>Devanagari</th><th>IAST</th><th>ASCII</th><th>Common Roman</th>
        </tr>
        <tr><td>अ</td><td>a</td><td>a</td><td>a</td></tr>
        <tr><td>आ</td><td>ā</td><td>aa / A</td><td>aa</td></tr>
        <tr><td>इ</td><td>i</td><td>i</td><td>i</td></tr>
        <tr><td>ई</td><td>ī</td><td>ii / I</td><td>ee</td></tr>
        <tr><td>उ</td><td>u</td><td>u</td><td>u</td></tr>
        <tr><td>ऊ</td><td>ū</td><td>uu / U</td><td>oo</td></tr>
        <tr><td>ऋ</td><td>ṛ</td><td>RRi / R^i</td><td>ri</td></tr>
        <tr><td>ॠ</td><td>ṝ</td><td>RRI / R^I</td><td>ree</td></tr>
        <tr><td>ऌ</td><td>ḷ</td><td>LLi / L^i</td><td>lri</td></tr>
        <tr><td>ए</td><td>e</td><td>e</td><td>e</td></tr>
        <tr><td>ऐ</td><td>ai</td><td>ai</td><td>ai</td></tr>
        <tr><td>ओ</td><td>o</td><td>o</td><td>o</td></tr>
        <tr><td>औ</td><td>au</td><td>au</td><td>au</td></tr>
    </table>
    """, unsafe_allow_html=True)
    
    st.markdown("### Consonants (Vyañjana) - Varga")
    
    st.markdown("""
    <table class="trans-table">
        <tr>
            <th>Devanagari</th><th>IAST</th><th>ASCII</th><th>Common Roman</th>
        </tr>
        <tr><td>क</td><td>ka</td><td>ka</td><td>ka</td></tr>
        <tr><td>ख</td><td>kha</td><td>kha</td><td>kha</td></tr>
        <tr><td>ग</td><td>ga</td><td>ga</td><td>ga</td></tr>
        <tr><td>घ</td><td>gha</td><td>gha</td><td>gha</td></tr>
        <tr><td>ङ</td><td>ṅa</td><td>~Na / N^a</td><td>nga</td></tr>
        <tr><td>च</td><td>ca</td><td>ca / cha</td><td>cha</td></tr>
        <tr><td>छ</td><td>cha</td><td>Cha</td><td>chha</td></tr>
        <tr><td>ज</td><td>ja</td><td>ja</td><td>ja</td></tr>
        <tr><td>झ</td><td>jha</td><td>jha</td><td>jha</td></tr>
        <tr><td>ञ</td><td>ña</td><td>~na / JNa</td><td>nya</td></tr>
        <tr><td>ट</td><td>ṭa</td><td>Ta</td><td>ta (retroflex)</td></tr>
        <tr><td>ठ</td><td>ṭha</td><td>Tha</td><td>tha (retroflex)</td></tr>
        <tr><td>ड</td><td>ḍa</td><td>Da</td><td>da (retroflex)</td></tr>
        <tr><td>ढ</td><td>ḍha</td><td>Dha</td><td>dha (retroflex)</td></tr>
        <tr><td>ण</td><td>ṇa</td><td>Na</td><td>na (retroflex)</td></tr>
        <tr><td>त</td><td>ta</td><td>ta</td><td>ta (dental)</td></tr>
        <tr><td>थ</td><td>tha</td><td>tha</td><td>tha (dental)</td></tr>
        <tr><td>द</td><td>da</td><td>da</td><td>da (dental)</td></tr>
        <tr><td>ध</td><td>dha</td><td>dha</td><td>dha (dental)</td></tr>
        <tr><td>न</td><td>na</td><td>na</td><td>na (dental)</td></tr>
        <tr><td>प</td><td>pa</td><td>pa</td><td>pa</td></tr>
        <tr><td>फ</td><td>pha</td><td>pha</td><td>pha</td></tr>
        <tr><td>ब</td><td>ba</td><td>ba</td><td>ba</td></tr>
        <tr><td>भ</td><td>bha</td><td>bha</td><td>bha</td></tr>
        <tr><td>म</td><td>ma</td><td>ma</td><td>ma</td></tr>
    </table>
    """, unsafe_allow_html=True)
    
    st.markdown("### Consonants (Vyañjana) - Avarga")
    
    st.markdown("""
    <table class="trans-table">
        <tr>
            <th>Devanagari</th><th>IAST</th><th>ASCII</th><th>Common Roman</th>
        </tr>
        <tr><td>य</td><td>ya</td><td>ya</td><td>ya</td></tr>
        <tr><td>र</td><td>ra</td><td>ra</td><td>ra</td></tr>
        <tr><td>ल</td><td>la</td><td>la</td><td>la</td></tr>
        <tr><td>व</td><td>va</td><td>va / wa</td><td>va / wa</td></tr>
        <tr><td>श</td><td>śa</td><td>sha / Sa</td><td>sha (palatal)</td></tr>
        <tr><td>ष</td><td>ṣa</td><td>Sha / shha</td><td>sha (retroflex)</td></tr>
        <tr><td>स</td><td>sa</td><td>sa</td><td>sa (dental)</td></tr>
        <tr><td>ह</td><td>ha</td><td>ha</td><td>ha</td></tr>
    </table>
    """, unsafe_allow_html=True)
    
    st.markdown("### Special Characters (Anusvāra, Visarga, etc.)")
    
    st.markdown("""
    <table class="trans-table">
        <tr>
            <th>Devanagari</th><th>IAST</th><th>ASCII</th><th>Common Roman</th>
        </tr>
        <tr><td>ं (Anusvāra)</td><td>ṃ</td><td>M / .m</td><td>m</td></tr>
        <tr><td>ः (Visarga)</td><td>ḥ</td><td>H / .h</td><td>h</td></tr>
        <tr><td>ँ (Candrabindu)</td><td>m̐</td><td>.N</td><td>n (nasal)</td></tr>
        <tr><td>् (Halanta/Virāma)</td><td>(none)</td><td>(none)</td><td>(suppresses vowel)</td></tr>
        <tr><td>ऽ (Avagraha)</td><td>'</td><td>'</td><td>(elision marker)</td></tr>
        <tr><td>। (Daṇḍa)</td><td>|</td><td>|</td><td>. (period)</td></tr>
        <tr><td>॥ (Double Daṇḍa)</td><td>||</td><td>||</td><td>|| (verse end)</td></tr>
    </table>
    """, unsafe_allow_html=True)
    
    st.markdown("### Conjuncts & Special Forms")
    
    st.markdown("""
    <table class="trans-table">
        <tr>
            <th>Devanagari</th><th>IAST</th><th>ASCII</th><th>Common Roman</th>
        </tr>
        <tr><td>क्ष</td><td>kṣa</td><td>kSha / xa</td><td>ksha</td></tr>
        <tr><td>त्र</td><td>tra</td><td>tra</td><td>tra</td></tr>
        <tr><td>ज्ञ</td><td>jña</td><td>GYa / j~na</td><td>gya / jna</td></tr>
        <tr><td>श्र</td><td>śra</td><td>shra</td><td>shra</td></tr>
    </table>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    ---
    
    ## 💡 Tips for Best Results
    
    1. **Use Word Frequency** to understand term distribution before deep-diving
    2. **Chapter Index** helps navigate large texts efficiently
    3. **Compare across texts** for comprehensive understanding  
    4. **Adjust font size** for comfortable Devanagari reading
    5. **Use Dark Mode** for extended study sessions
    6. **Check Cross-References** to find related content in other Samhitas
    
    ---
    
    ## 👨‍🏫 About
    
    **Prof. (Dr.) Prasanna Kulkarni**
    
    This application represents a technological contribution to making classical Āyurvedic literature accessible for research, education, and practice.
    
    🔗 [LinkedIn](https://linkedin.com/in/drprasannakulkarni) | 🌐 [Atharva AyurTech](https://atharvaayurtech.com)
    
    ---
    
    *"यत्र विद्या तत्र मुक्तिः" — Where there is knowledge, there is liberation.*
    """)
    
    st.markdown("---")
    st.caption("**Version 20.1** | e-Bhruhat Trayi Exploration by PraKul")