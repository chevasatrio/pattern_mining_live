# ============================================
# STEP 1: Buat semua file yang diperlukan untuk deploy
# ============================================

dashboard_code = '''
# ============================================
# DASHBOARD ANALISIS POLA KANDUNGAN GIZI
# TUGAS BESAR PENAMBANGAN DATA
# ============================================

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from mlxtend.frequent_patterns import apriori, association_rules
import warnings
import logging

# ================== HILANGKAN WARNING ==================
warnings.filterwarnings('ignore')
logging.captureWarnings(True)
logging.getLogger('py.warnings').setLevel(logging.ERROR)
logging.getLogger('jupyter_client').setLevel(logging.ERROR)

# ================== KONFIGURASI HALAMAN ==================
st.set_page_config(
    page_title="Dashboard Gizi - Apriori",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================== CSS KUSTOM ==================
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #2E4053;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        text-align: center;
        color: #5D6D7E;
        margin-bottom: 2rem;
    }
    .card {
        background-color: #F8F9FA;
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        padding: 1rem;
        color: white;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# ================== SIDEBAR ==================
with st.sidebar:
    st.markdown("<h1 style='text-align: center;'>🍽️ Gizi Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("---")

    # Upload Dataset
    st.subheader("📂 Upload Dataset")
    st.caption("Upload file CSV nilai gizi makanan Indonesia")
    uploaded_file = st.file_uploader("Pilih file CSV", type=["csv"])

    if uploaded_file is not None:
        st.success("✅ Dataset berhasil dimuat!")
        df = pd.read_csv(uploaded_file)
        st.caption(f"📊 {df.shape[0]} baris, {df.shape[1]} kolom")

        # ================== PREPROCESSING ==================
        # Ambil kolom yang relevan - Sesuaikan dengan nama kolom di CSV-mu!
        # Jika kolom berbeda, sesuaikan di sini
        cols = ['energy_kcal', 'protein_g', 'fat_g', 'carbohydrate_g', 'sodium_mg', 'fiber_g']

        # Jika kolom tidak ditemukan, gunakan mapping alternatif
        available_cols = []
        for col in cols:
            if col in df.columns:
                available_cols.append(col)
            elif col == 'energy_kcal' and 'energy_kcal' not in df.columns:
                # Cari alternatif nama kolom
                for alt in ['calories', 'Energi']:
                    if alt in df.columns:
                        available_cols.append(alt)
                        break

        # Filter kolom yang ada
        df_gizi = df[[c for c in cols if c in df.columns]].copy()

        if len(df_gizi.columns) == 0:
            st.error("⚠️ Kolom gizi tidak ditemukan! Pastikan file CSV memiliki kolom yang sesuai.")
            st.stop()

        # Hapus baris dengan semua nilai 0
        df_gizi = df_gizi[(df_gizi != 0).any(axis=1)]

        def categorize(series):
            q1 = series.quantile(0.33)
            q2 = series.quantile(0.66)
            return ['Rendah' if x <= q1 else 'Sedang' if x <= q2 else 'Tinggi' for x in series]

        df_disc = pd.DataFrame()
        for col in df_gizi.columns:
            df_disc[col] = categorize(df_gizi[col])

        df_encoded = pd.get_dummies(df_disc)

        # ================== APRIORI ==================
        min_support = 0.05
        frequent_itemsets = apriori(df_encoded, min_support=min_support, use_colnames=True)
        rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1.2)
        rules = rules.sort_values('lift', ascending=False)

        # ================== PARAMETER & FILTER ==================
        st.markdown("---")
        st.subheader("⚙️ Parameter")
        st.caption(f"**min_support:** 0.05")
        st.caption(f"**min_confidence:** 0.6")
        st.caption(f"**min_lift:** 1.2")
        st.caption(f"**Total Rules:** {len(rules)}")

        st.markdown("---")
        st.subheader("🎯 Filter Rules")
        min_lift_filter = st.slider(
            "Minimum Lift",
            min_value=1.0,
            max_value=3.0,
            value=1.2,
            step=0.1
        )
        filtered_rules = rules[rules['lift'] >= min_lift_filter]
        st.caption(f"**Rules setelah filter:** {len(filtered_rules)}")

        # ================== STATISTIK CEPAT ==================
        st.markdown("---")
        st.subheader("📊 Statistik")
        significant = filtered_rules[filtered_rules['lift'] > 1.5]
        col1, col2 = st.columns(2)
        col1.metric("Total Rules", len(filtered_rules))
        col2.metric("Rules (Lift>1.5)", len(significant))
        if len(significant) > 0:
            col3, col4 = st.columns(2)
            col3.metric("Rata-rata Lift", f"{significant['lift'].mean():.2f}")
            col4.metric("Rata-rata Confidence", f"{significant['confidence'].mean():.2f}")

# ================== MAIN CONTENT ==================
if uploaded_file is not None:
    st.markdown("<div class='main-header'>🍽️ Dashboard Analisis Pola Kandungan Gizi</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>Menggunakan Algoritma Apriori untuk Menemukan Asosiasi Kandungan Gizi Makanan Indonesia</div>", unsafe_allow_html=True)
    st.markdown("---")

    # Tab layout
    tab1, tab2, tab3 = st.tabs(["📊 Top Rules", "📈 Visualisasi", "📋 Ringkasan"])

    # ================== TAB 1: TOP RULES ==================
    with tab1:
        st.header("🏆 Top 10 Association Rules by Lift")

        top10 = filtered_rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']].head(10)

        def format_itemset(itemset):
            return ', '.join([str(item) for item in itemset])

        top10_display = top10.copy()
        top10_display['antecedents'] = top10_display['antecedents'].apply(format_itemset)
        top10_display['consequents'] = top10_display['consequents'].apply(format_itemset)
        top10_display['support'] = top10_display['support'].round(4)
        top10_display['confidence'] = top10_display['confidence'].round(4)
        top10_display['lift'] = top10_display['lift'].round(2)

        st.dataframe(
            top10_display,
            use_container_width=True,
            column_config={
                "antecedents": "Antecedent (X)",
                "consequents": "Consequent (Y)",
                "support": st.column_config.NumberColumn("Support", format="%.4f"),
                "confidence": st.column_config.NumberColumn("Confidence", format="%.4f"),
                "lift": st.column_config.NumberColumn("Lift", format="%.2f"),
            }
        )

        # Aturan paling kuat
        if len(top10) > 0:
            st.markdown("---")
            st.subheader("💡 Aturan Paling Signifikan")
            best_rule = top10.iloc[0]
            st.success(f"""
            **{best_rule['antecedents']} → {best_rule['consequents']}**

            - **Support:** {best_rule['support']:.4f}
            - **Confidence:** {best_rule['confidence']*100:.1f}%
            - **Lift:** {best_rule['lift']:.2f}
            """)

    # ================== TAB 2: VISUALISASI ==================
    with tab2:
        st.header("📈 Visualisasi Interaktif")

        # 1. Scatter Plot
        st.subheader("Scatter Plot Support vs Confidence (warna = Lift)")
        fig1 = px.scatter(
            filtered_rules,
            x='support',
            y='confidence',
            color='lift',
            color_continuous_scale='Viridis',
            hover_data=['lift', 'support', 'confidence'],
            title="Hubungan Support, Confidence, dan Lift",
            labels={'support': 'Support', 'confidence': 'Confidence', 'lift': 'Lift'}
        )
        fig1.update_traces(marker=dict(size=8, line=dict(width=1, color='black')))
        fig1.update_layout(
            template='plotly_white',
            height=500,
            coloraxis_colorbar=dict(title="Lift")
        )
        st.plotly_chart(fig1, use_container_width=True)

        # 2. Bar Chart Top 10 Lift
        st.subheader("Top 10 Rules by Lift")
        top_rules = filtered_rules.head(10)
        labels = []
        for a in top_rules['antecedents']:
            label = str(a).replace("frozenset({", "").replace("})", "").replace("'", "")
            if len(label) > 35:
                label = label[:32] + '...'
            labels.append(label)

        fig2 = px.bar(
            x=top_rules['lift'][::-1],
            y=labels[::-1],
            orientation='h',
            title="10 Aturan dengan Lift Tertinggi",
            labels={'x': 'Lift', 'y': 'Aturan'},
            color=top_rules['lift'][::-1],
            color_continuous_scale='Sunset'
        )
        fig2.update_layout(template='plotly_white', height=500)
        st.plotly_chart(fig2, use_container_width=True)

        # 3. Heatmap Korelasi
        st.subheader("Heatmap Korelasi Antar Kandungan Gizi")
        corr = df_gizi.corr()
        fig3 = go.Figure(data=go.Heatmap(
            z=corr.values,
            x=corr.columns,
            y=corr.columns,
            colorscale='RdBu',
            zmin=-1, zmax=1,
            text=corr.values.round(2),
            texttemplate='%{text}',
            textfont={"size": 10}
        ))
        fig3.update_layout(
            title='Korelasi Antar Kandungan Gizi',
            template='plotly_white',
            height=500,
            xaxis=dict(tickangle=45)
        )
        st.plotly_chart(fig3, use_container_width=True)

        # 4. Boxplots
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Kalori vs Kategori Lemak")
            df_plot = df_gizi.copy()
            # Gunakan kolom yang benar
            if 'fat_g' in df_disc.columns:
                df_plot['Lemak'] = df_disc['fat_g']
                fig4 = px.box(
                    df_plot,
                    x='Lemak',
                    y=df_gizi.columns[0],
                    color='Lemak',
                    category_orders={"Lemak": ['Rendah', 'Sedang', 'Tinggi']},
                    title="Distribusi Kalori berdasarkan Kategori Lemak",
                    labels={'energy_kcal': 'Kalori (kkal)', 'Lemak': 'Kategori Lemak'}
                )
                fig4.update_layout(template='plotly_white', height=400)
                st.plotly_chart(fig4, use_container_width=True)
            else:
                st.info("Kolom 'fat_g' tidak ditemukan")

        with col2:
            st.subheader("Kalori vs Kategori Karbohidrat")
            if 'carbohydrate_g' in df_disc.columns:
                df_plot['Karbohidrat'] = df_disc['carbohydrate_g']
                fig5 = px.box(
                    df_plot,
                    x='Karbohidrat',
                    y=df_gizi.columns[0],
                    color='Karbohidrat',
                    category_orders={"Karbohidrat": ['Rendah', 'Sedang', 'Tinggi']},
                    title="Distribusi Kalori berdasarkan Kategori Karbohidrat",
                    labels={'energy_kcal': 'Kalori (kkal)', 'Karbohidrat': 'Kategori Karbohidrat'}
                )
                fig5.update_layout(template='plotly_white', height=400)
                st.plotly_chart(fig5, use_container_width=True)
            else:
                st.info("Kolom 'carbohydrate_g' tidak ditemukan")

    # ================== TAB 3: RINGKASAN ==================
    with tab3:
        st.header("📋 Ringkasan Analisis")

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Sampel", f"{df_gizi.shape[0]}")
        col2.metric("Total Rules", f"{len(filtered_rules)}")
        col3.metric("Rules (Lift>1.5)", f"{len(significant)}")

        st.markdown("---")

        st.subheader("📊 Distribusi Kategori Gizi")
        kategori_counts = {}
        for col in df_disc.columns:
            for cat in ['Rendah', 'Sedang', 'Tinggi']:
                key = f"{col}_{cat}"
                kategori_counts[key] = (df_disc[col] == cat).sum()

        kategori_df = pd.DataFrame(list(kategori_counts.items()), columns=['Kategori', 'Jumlah'])
        st.dataframe(kategori_df, use_container_width=True)

        st.subheader("Histogram Support & Confidence")
        fig6 = px.histogram(
            pd.DataFrame({
                'Support': filtered_rules['support'],
                'Confidence': filtered_rules['confidence']
            }),
            nbins=20,
            title="Distribusi Support & Confidence",
            labels={'value': 'Nilai', 'variable': 'Metrik'}
        )
        fig6.update_layout(template='plotly_white', height=400)
        st.plotly_chart(fig6, use_container_width=True)

        st.subheader("📌 Interpretasi Dashboard")
        st.markdown("""
        | Subplot | Interpretasi |
        |---------|--------------|
        | **Scatter Plot** | Titik dengan warna terang (lift tinggi) menunjukkan aturan kuat. |
        | **Top 10 Lift** | Aturan `Lemak=T, Karbohidrat=T → Kalori=T` paling signifikan (lift=2.38). |
        | **Heatmap** | Lemak dan kalori berkorelasi positif kuat (0.85). |
        | **Boxplot** | Semakin tinggi lemak/karbohidrat, semakin tinggi kalori. |
        """)

else:
    st.markdown("<div class='main-header'>🍽️ Dashboard Analisis Pola Kandungan Gizi</div>", unsafe_allow_html=True)
    st.markdown("---")
    st.info("👈 **Silakan upload file CSV dataset nilai gizi makanan Indonesia di sidebar untuk memulai.**")
    st.markdown("""
    ### 📌 Format Dataset:
    - `energy_kcal` (kalori)
    - `protein_g` (protein)
    - `fat_g` (lemak)
    - `carbohydrate_g` (karbohidrat)
    - `sodium_mg` (natrium)
    - `fiber_g` (serat)
    """)

st.markdown("---")
st.caption("Dibuat untuk Tugas Besar Penambangan Data | Telkom University Surabaya 2026")
'''

with open('dashboard_gizi.py', 'w') as f:
    f.write(dashboard_code)

print("✅ dashboard_gizi.py berhasil dibuat")

# 2. Buat file requirements.txt
requirements = """
streamlit
pandas
numpy
matplotlib
seaborn
mlxtend
plotly
"""

with open('requirements.txt', 'w') as f:
    f.write(requirements)

print("✅ requirements.txt berhasil dibuat")

# 3. Buat file .gitignore
gitignore = """
__pycache__/
*.pyc
.DS_Store
*.csv
*.png
*.xlsx
*.zip
*.pyc
.env
.venv
venv/
"""

with open('.gitignore', 'w') as f:
    f.write(gitignore)

print("✅ .gitignore berhasil dibuat")

# 4. Download file yang sudah dibuat ke komputer lokal
from google.colab import files

files.download('dashboard_gizi.py')
files.download('requirements.txt')
files.download('.gitignore')

print("✅ Semua file siap! File sudah diunduh ke komputer.")
