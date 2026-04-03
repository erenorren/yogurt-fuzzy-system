import streamlit as st
import pandas as pd

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="YoguCheck - Tim 1 UNTAN",
    page_icon="🍦",
    layout="centered"
)

# --- STYLE CSS (Agar Tampilan Seperti Game & Cantik) ---
st.markdown("""
    <style>
    .main {
        background-color: #fdfaf5;
    }
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        height: 3em;
        background-color: #ffb7c5;
        color: white;
        font-weight: bold;
        border: none;
    }
    .stButton>button:hover {
        background-color: #ff8fab;
        color: white;
    }
    .reportview-container .main .block-container {
        padding-top: 2rem;
    }
    .card {
        padding: 20px;
        border-radius: 15px;
        background-color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LOGIKA FUZZY MAMDANI (SESUAI LAPORAN) ---
def mu_suhu_dingin(x):
    if x <= 5: return 1.0
    if 5 < x < 10: return (10 - x) / (10 - 5)
    return 0.0

def mu_suhu_normal(x):
    if 8 < x <= 15: return (x - 8) / (15 - 8)
    if 15 < x < 22: return (22 - x) / (22 - 15)
    if x == 15: return 1.0
    return 0.0

def mu_suhu_panas(x):
    if x <= 20: return 0.0
    if 20 < x < 25: return (x - 20) / (25 - 20)
    return 1.0

def mu_hari_sedikit(x):
    if x <= 2: return 1.0
    if 2 < x < 4: return (4 - x) / (4 - 2)
    return 0.0

def mu_hari_sedang(x):
    if 2 < x <= 7: return (x - 2) / (7 - 2)
    if 7 < x < 12: return (12 - x) / (12 - 7)
    if x == 7: return 1.0
    return 0.0

def mu_hari_banyak(x):
    if x <= 10: return 0.0
    if 10 < x < 14: return (x - 10) / (14 - 10)
    return 1.0

def hitung_kelayakan(suhu, hari):
    # Fuzzifikasi
    s_dingin = mu_suhu_dingin(suhu)
    s_normal = mu_suhu_normal(suhu)
    s_panas = mu_suhu_panas(suhu)
    
    h_sedikit = mu_hari_sedikit(hari)
    h_sedang = mu_hari_sedang(hari)
    h_banyak = mu_hari_banyak(hari)

    # Rule Evaluation (AND menggunakan MIN)
    # Skor z: Layak=10, Hampir Basi=50, Basi=100
    rules = [
        (min(h_sedikit, s_panas), 100), # R1
        (min(h_sedikit, s_normal), 50),  # R2
        (min(h_sedikit, s_dingin), 50),  # R3
        (min(h_sedang, s_panas), 50),    # R4
        (min(h_sedang, s_normal), 10),   # R5
        (min(h_sedang, s_dingin), 10),   # R6
        (min(h_banyak, s_panas), 50),    # R7
        (min(h_banyak, s_normal), 10),   # R8
        (min(h_banyak, s_dingin), 10)    # R9
    ]

    # Defuzzifikasi (Weighted Average)
    nominator = sum(a * z for a, z in rules)
    denominator = sum(a for a, z in rules)

    if denominator == 0:
        return 10.0, "Layak Konsumsi", "🍦"
    
    z_result = nominator / denominator
    
    if z_result <= 30:
        return z_result, "Layak Konsumsi", "😋"
    elif z_result <= 70:
        return z_result, "Hampir Basi", "😟"
    else:
        return z_result, "Sudah Basi", "🤮"

# --- UI APLIKASI ---
st.title("🍦 YoguCheck")
st.caption("Sistem Kelayakan Yogurt Berbasis Fuzzy Logic - Tim 1 Sistem Informasi UNTAN")

# Sidebar untuk Profile Tim
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/0/00/Logo_Universitas_Tanjungpura.png", width=100)
    st.header("Profile Tim 1")
    st.markdown("""
    - **Regisha Sheren** (H1101241036)
    - **Florecita Wenny** (H1101241039)
    - **Aurellya Y. P.** (H1101241043)
    - **Aisyah** (H1101241044)
    """)
    st.divider()
    st.info("Project Kecerdasan Buatan 2026")

# Main Content
tabs = st.tabs(["🎮 Cek Yogurt", "📊 Data Uji", "📝 Tentang"])

with tabs[0]:
    st.subheader("Berapa suhu penyimpananmu?")
    input_suhu = st.slider("Suhu (°C)", 0, 30, 15)
    
    st.subheader("Berapa hari sisa kadaluarsa?")
    input_hari = st.slider("Sisa Hari", 0, 14, 7)
    
    st.divider()
    
    if st.button("Analisis Kelayakan"):
        z, status, emoji = hitung_kelayakan(input_suhu, input_hari)
        
        # Animasi hasil sederhana
        st.balloons()
        
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown(f"<h1 style='font-size: 100px; text-align: center;'>{emoji}</h1>", unsafe_allow_html=True)
        with col2:
            st.metric("Skor Kelayakan (z*)", f"{z:.2f}")
            st.subheader(f"Status: {status}")
            
        if status == "Layak Konsumsi":
            st.success("Yogurt segar! Aman untuk dikonsumsi.")
        elif status == "Hampir Basi":
            st.warning("Hati-hati, kualitas yogurt mulai menurun.")
        else:
            st.error("Jangan dimakan! Yogurt sudah rusak.")

with tabs[1]:
    st.write("Daftar sampel data uji dari laporan[cite: 106]:")
    data_uji = {
        "Data": ["D1", "D2", "D11", "D13", "D30"],
        "Suhu": [5, 5, 22, 25, 27],
        "Sisa Hari": [12, 8, 7, 3, 1],
        "Status": ["Layak", "Layak", "Hampir Basi", "Sudah Basi", "Sudah Basi"]
    }
    st.table(pd.DataFrame(data_uji))

with tabs[2]:
    st.markdown("""
    ### Tentang Project
    Aplikasi ini menggunakan **Metode Fuzzy Logic Mamdani** untuk menentukan apakah yogurt masih layak dimakan berdasarkan kondisi lingkungan (suhu) dan waktu (kadaluarsa)[cite: 21, 33].
    
    **Variabel Input:**
    - Suhu (0-30°C) [cite: 34]
    - Sisa Hari (0-14 Hari) [cite: 34]
    
    **Variabel Output:**
    - Status (Layak, Hampir Basi, Basi) [cite: 34]
    """)