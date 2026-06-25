# 🍽️ Dashboard Analisis Pola Kandungan Gizi

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://pattern-mining-live.streamlit.app)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Dashboard interaktif untuk menganalisis pola asosiasi kandungan gizi makanan Indonesia menggunakan **Algoritma Apriori** dan **Association Rule Mining**. Proyek ini dikembangkan sebagai Tugas Besar Mata Kuliah Penambangan Data.

---

## 📌 Latar Belakang

Kandungan gizi makanan memiliki hubungan yang saling terkait. Misalnya, makanan tinggi lemak cenderung tinggi kalori, atau makanan tinggi karbohidrat juga tinggi energi. Dengan menggunakan teknik **Association Rule Mining**, kita dapat menemukan pola-pola asosiasi yang menarik dari data kandungan gizi.

Proyek ini menerapkan **Algoritma Apriori** untuk menemukan frequent itemsets dan aturan asosiasi dari dataset nilai gizi makanan Indonesia. Hasilnya divisualisasikan dalam dashboard interaktif yang mudah dipahami.

---

## 🎯 Tujuan

- Mengidentifikasi pola asosiasi antar kandungan gizi (misal: lemak tinggi → kalori tinggi).
- Memberikan wawasan tentang hubungan antar zat gizi dalam makanan.
- Menyediakan alat interaktif untuk eksplorasi data gizi.
- Mendukung pengambilan keputusan dalam bidang gizi dan kesehatan.

---

## ✨ Fitur Utama

| Fitur | Deskripsi |
|-------|-----------|
| **Upload Dataset CSV** | Upload file CSV berisi data kandungan gizi makanan. |
| **Preprocessing Otomatis** | Membersihkan data, menghapus baris kosong, dan diskritisasi menjadi 3 kategori (Rendah, Sedang, Tinggi). |
| **Algoritma Apriori** | Menemukan frequent itemsets dan aturan asosiasi. |
| **Filter Interaktif** | Filter aturan berdasarkan nilai Lift minimum (1.0 - 3.0). |
| **Top 10 Rules** | Menampilkan 10 aturan dengan Lift tertinggi. |
| **Visualisasi Dinamis** | Scatter plot, bar chart, heatmap, boxplot, histogram, dan top items. |
| **Ringkasan Statistik** | Total rules, rules signifikan (Lift > 1.5), rata-rata Lift dan Confidence. |

---

## 🧠 Metodologi

### 1. Preprocessing Data
- **Seleksi Kolom**: Hanya kolom kandungan gizi yang digunakan (`energy_kcal`, `protein_g`, `fat_g`, `carbohydrate_g`, `sodium_mg`, `fiber_g`).
- **Pembersihan Data**: Menghapus baris yang semua nilainya 0.
- **Diskritisasi**: Setiap kolom dikategorikan menjadi 3 bagian berdasarkan kuartil:
  - `Rendah`: ≤ kuartil 33%
  - `Sedang`: > kuartil 33% dan ≤ kuartil 66%
  - `Tinggi`: > kuartil 66%

### 2. Transformasi Data
Data kategorikal diubah menjadi format **one-hot encoding** agar dapat diproses oleh algoritma Apriori.

### 3. Algoritma Apriori
- **Frequent Itemsets**: Mencari kombinasi item yang sering muncul dengan `min_support = 0.05` (5%).
- **Association Rules**: Menghasilkan aturan asosiasi dengan `min_lift = 1.2`.

### 4. Evaluasi Aturan
Aturan dievaluasi menggunakan metrik:
- **Support**: Seberapa sering aturan muncul dalam dataset.
- **Confidence**: Seberapa sering konsekuen terjadi jika anteseden terjadi.
- **Lift**: Seberapa kuat hubungan antara anteseden dan konsekuen (Lift > 1 menunjukkan korelasi positif).

### 5. Visualisasi
Hasil analisis ditampilkan dalam berbagai grafik interaktif untuk memudahkan interpretasi.

---

## ⚙️ Parameter Analisis

| Parameter | Nilai | Keterangan |
|-----------|-------|------------|
| `min_support` | 0.05 | Minimum support untuk frequent itemsets (5%). |
| `min_confidence` | 0.6 | Minimum confidence untuk aturan asosiasi. |
| `min_lift` | 1.2 | Minimum lift untuk aturan yang ditampilkan. |
| **Filter Lift** | 1.0 – 3.0 | Slider untuk memfilter aturan berdasarkan Lift. |

---

## 📊 Interpretasi Visualisasi

| Visualisasi | Interpretasi |
|-------------|--------------|
| **Scatter Plot** | Setiap titik mewakili aturan. Sumbu X = Support, Y = Confidence. Warna menunjukkan Lift. Titik berwarna terang (kuning/hijau) memiliki Lift tinggi → hubungan lebih kuat. |
| **Top 10 Lift (Bar Chart)** | Menampilkan 10 aturan dengan Lift tertinggi. Semakin tinggi Lift, semakin kuat hubungan antar item. |
| **Heatmap Korelasi** | Menunjukkan korelasi antar kandungan gizi. Nilai mendekati +1 (merah) = hubungan positif kuat. Contoh: lemak dan kalori berkorelasi tinggi (0.85). |
| **Boxplot (Kalori vs Lemak)** | Makanan dengan lemak tinggi memiliki median kalori jauh lebih tinggi dibanding lemak rendah. Mendukung aturan `Lemak=Tinggi → Kalori=Tinggi`. |
| **Boxplot (Kalori vs Karbohidrat)** | Makanan dengan karbohidrat tinggi cenderung memiliki kalori tinggi. |
| **Histogram Support & Confidence** | Sebagian besar aturan memiliki support 0.05–0.15 dan confidence 0.6–0.8 → aturan cukup kuat dan tidak terlalu langka. |
| **Top 10 Item Paling Sering Muncul** | Item `Lemak=Tinggi` dan `Kalori=Tinggi` mendominasi → indikator penting dalam pola gizi. |

---

## 🚀 Demo Aplikasi

Aplikasi telah dideploy di Streamlit Cloud:  
🔗 [**https://pattern-mining-live.streamlit.app**](https://pattern-mining-live.streamlit.app)

> **Catatan:** Anda perlu mengupload file CSV dengan format yang sesuai untuk menjalankan analisis.

---

## 📥 Instalasi dan Menjalankan Aplikasi

### 1. Clone Repository

```bash
git clone https://github.com/chevasatrio/pattern_mining_live.git
cd pattern_mining_live
